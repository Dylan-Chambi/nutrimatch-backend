from src.model.general_food_detector import GeneralFoodDetector

class ImagePredictionService():
    def __init__(self, food_detector):
        self.food_detector: GeneralFoodDetector = food_detector
        

    def detect_food(self, image_b64: str) -> str:
        """
        Service to detect food in an image
        """
        
        return self.food_detector.detect_food(image_b64)