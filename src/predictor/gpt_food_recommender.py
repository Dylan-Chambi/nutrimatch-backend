from src.config.config import get_settings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.model.general_food_recommender import GeneralFoodRecommender
from src.schema.food_detection import FoodDetection
from src.template.food_recomendation_template import FOOD_RECOMMENDATION_TEMPLATE
from src.schema.food_recommendation import FoodRecommendation
from langchain.schema.messages import HumanMessage, SystemMessage
from src.config.logger import logger


SETTINGS = get_settings()

class GPTFoodRecommender(GeneralFoodRecommender):
    def __init__(self):
        super().__init__(
            model_name=SETTINGS.OPENAI_CHAT_MODEL, 
            model=ChatOpenAI(
                    model_name=SETTINGS.OPENAI_CHAT_MODEL,
                    openai_api_key=SETTINGS.OPENAI_KEY,
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
        
        prediction = self.model.invoke(messages)

        food_recommendation: FoodRecommendation = out_parser.invoke(prediction)

        logger.info({"method": "get_recommendation", "message": f"Got recommendation: {str(food_recommendation)[:100]}..."})
        return food_recommendation
        