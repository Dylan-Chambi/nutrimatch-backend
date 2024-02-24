import base64
import io
from PIL import Image
from fastapi import UploadFile
from src.template.food_detection_template import FOOD_DETECTION_TEMPLATE
from src.predictor.gpt_food_detector import GeneralFoodDetector
from src.config.config import get_settings

SETTINGS = get_settings()

class ImagePredictionService():
    def __init__(self, gpt_food_detector: GeneralFoodDetector):
        self.gpt_food_detector = gpt_food_detector
        

    def detect_food(self, image: UploadFile):
        """
        Service to detect food in an image
        """
        
          # Read the image and convert it to webp format with 80% quality and 256x256 size
        img_stream = io.BytesIO(image.file.read())
        img_obj = Image.open(img_stream)
        img_obj = img_obj.resize((256, 256))
        webp_stream = io.BytesIO()
        img_obj.save(webp_stream, format='WebP', quality=80)
        
        # Convert the image to base64
        image_b64 = base64.b64encode(webp_stream.getvalue()).decode('utf-8')
        image_b64 = f"data:image/webp;base64,{image_b64}"

        image.file.seek(0)
        
        return self.gpt_food_detector.detect_food(image_b64, FOOD_DETECTION_TEMPLATE)