from src.config.config import get_settings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.model.general_food_detector import GeneralFoodDetector
from src.schema.food_detection import FoodDetection
from src.template.food_detection_template import FOOD_DETECTION_TEMPLATE
from langchain.schema.messages import HumanMessage, SystemMessage

SETTINGS = get_settings()


class GPTFoodDetector(GeneralFoodDetector):
    def __init__(self):
        super().__init__(
            model_name=SETTINGS.OPENAI_VISION_MODEL, 
            model=ChatOpenAI(model_name=SETTINGS.OPENAI_VISION_MODEL,
                             openai_api_key=SETTINGS.OPENAI_KEY,
                             max_tokens=500,
                             )
            )
        
    def detect_food(self, image_b64: str) -> FoodDetection:
        """
        Detect food in an image using the GPT Vision model
        """
        out_parser = PydanticOutputParser(pydantic_object=FoodDetection)
        
        prompt = PromptTemplate(
            template=FOOD_DETECTION_TEMPLATE,
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
                            "image_url": image_b64
                        }
                    ]
                )
            ]
        
        prediction = self.model.invoke(messages)     
        
        food_detection: FoodDetection = out_parser.invoke(prediction)
        
        return food_detection
        