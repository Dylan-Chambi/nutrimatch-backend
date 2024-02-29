from fastapi import HTTPException
from src.config.config import get_settings
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.model.general_food_detector import GeneralFoodDetector
from src.schema.food_detection import FoodDetection
from src.template.food_detection_template import FOOD_DETECTION_TEMPLATE
from langchain.schema.messages import HumanMessage, SystemMessage
from src.config.logger import logger
from src.service.mongodb.keys_service import KeysService
from openai import OpenAIError

SETTINGS = get_settings()

class GPTFoodDetector(GeneralFoodDetector):
    def __init__(self, keys_service: KeysService):
        self.keys_service = keys_service
        self.tier = 1
        self.valid_token = self.keys_service.get_last_key_active(tier=self.tier)
        super().__init__(
            model_name=SETTINGS.OPENAI_VISION_MODEL, 
            model=ChatOpenAI(model_name=SETTINGS.OPENAI_VISION_MODEL,
                             openai_api_key=self.valid_token.token,
                             max_tokens=300,
                             )
            )
        
    def detect_food(self, image_b64: str, detector_context_template: str = FOOD_DETECTION_TEMPLATE) -> FoodDetection:
        """
        Detect food in an image using the GPT Vision model
        """
        logger.info({"method": "detect_food", "message": f"Detecting food in image with image_b64: {image_b64[:100]}... and detector_context_template: {detector_context_template[:100]}..."})
        out_parser = PydanticOutputParser(pydantic_object=FoodDetection)
        
        prompt = PromptTemplate(
            template=detector_context_template,
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
                            "type": "image_url",
                            "image_url":{
                                "url": image_b64,
                                "detail": "low",
                                "resize": 512
                            }
                        }
                    ]
                )
            ]
        
        prediction = self.try_make_prediction(messages)

        food_detection: FoodDetection = out_parser.invoke(prediction)
        
        logger.info({"method": "detect_food", "message": f"Detected food in image: {str(food_detection)[:100]}..."})
        return food_detection
        
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