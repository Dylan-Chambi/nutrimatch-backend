from openai import OpenAIError
from fastapi import HTTPException
from src.config.config import get_settings
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.model.general_food_recommender import GeneralFoodRecommender
from src.template.food_recomendation_template import FOOD_RECOMMENDATION_TEMPLATE
from src.schema.food_recommendation import FoodRecommendation
from langchain.schema.messages import HumanMessage, SystemMessage
from src.config.logger import logger
from src.service.mongodb.keys_service import KeysService


SETTINGS = get_settings()

class GPTFoodRecommender(GeneralFoodRecommender):
    def __init__(self, keys_service: KeysService):
        self.keys_service = keys_service
        self.tier = 0
        self.valid_token = self.keys_service.get_last_key_active(tier=self.tier)
        super().__init__(
            model_name=SETTINGS.OPENAI_CHAT_MODEL, 
            model=ChatOpenAI(
                    model_name=SETTINGS.OPENAI_CHAT_MODEL,
                    openai_api_key=self.valid_token.token,
                    max_tokens=1000,
                    model_kwargs={"response_format": { "type": "json_object" }}
                )
            )
        
    def get_recommendation(self, food_detection: str, recommender_context_template: str = FOOD_RECOMMENDATION_TEMPLATE) -> FoodRecommendation:
        """
        Detect food in an image using the GPT Vision model
        """
        logger.info({"method": "get_recommendation", "message": f"Getting recommendation for food_detection: {food_detection} and recommender_context_template: {recommender_context_template[:100]}..."})
        out_parser = PydanticOutputParser(pydantic_object=FoodRecommendation)
        
        prompt = PromptTemplate(
            template=recommender_context_template,
            input_variables=[],
            partial_variables={"format_instructions": out_parser.get_format_instructions()}
        )
        
        messages = [
                SystemMessage(
                    content=[
                        {
                            "type": "text",
                            "text": prompt.format()
                        },
                    ]
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": food_detection
                        }
                    ]
                )
            ]
        
        prediction = self.try_make_prediction(messages)

        food_recommendation: FoodRecommendation = out_parser.invoke(prediction)

        logger.info({"method": "get_recommendation", "message": f"Got recommendation: {str(food_recommendation)[:100]}..."})
        return food_recommendation
    

    def try_make_prediction(self, messages: list, max_tries: int = 5) -> dict:
        """
        Try to make a prediction with the given messages and output parser
        """
        for _ in range(max_tries):
            try:
                with get_openai_callback() as cb:
                    prediction = self.model.invoke(messages)
                    self.keys_service.add_tokens_usage_by_token(self.valid_token.token, cb.prompt_tokens, cb.completion_tokens, cb.total_tokens, self.model.model_name)
                return prediction
            except OpenAIError as e:
                if e.body.get("code") == "insufficient_quota":
                    self.keys_service.deactivate_key_by_token(self.valid_token.token)
                    self.valid_token = self.keys_service.get_last_key_active(self.tier)
                    print(f"Got new token: {self.valid_token.token}")
                    self.model = ChatOpenAI(model_name=self.model.model_name,
                             openai_api_key=self.valid_token.token,
                             max_tokens=self.model.max_tokens,
                             )
                else:
                    logger.error({"method": "try_make_prediction", "message": f"Error making prediction with messages: {str(messages)[:100]}: {e}"})
                    raise e
            except Exception as e:
                logger.error({"method": "try_make_prediction", "message": f"Error making prediction with messages: {str(messages)[:100]}: {e}"})
                raise e
        raise HTTPException(status_code=500, detail="Could not make prediction after {max_tries} tries")
        