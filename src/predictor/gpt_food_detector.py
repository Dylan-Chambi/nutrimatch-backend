import numpy as np
from src.config.config import get_settings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.model.general_food_detector import GeneralFoodDetector
from src.schema.food_detection import FoodDetection
from src.template.food_detection_template import FOOD_DETECTION_TEMPLATE
from langchain.schema.messages import HumanMessage, SystemMessage
from src.config.logger import logger

SETTINGS = get_settings()

class GPTFoodDetector(GeneralFoodDetector):
    def __init__(self):
        super().__init__(
            model_name=SETTINGS.OPENAI_VISION_MODEL, 
            model=ChatOpenAI(model_name=SETTINGS.OPENAI_VISION_MODEL,
                             openai_api_key=SETTINGS.OPENAI_KEY,
                             max_tokens=1000,
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
        
        prediction = self.model.invoke(messages)     
        
        food_detection: FoodDetection = out_parser.invoke(prediction)
        
        logger.info({"method": "detect_food", "message": f"Detected food in image: {str(food_detection)[:100]}..."})
        return food_detection
        