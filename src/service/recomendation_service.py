from fastapi import UploadFile
from src.template.food_recomendation_template import FOOD_RECOMMENDATION_TEMPLATE
from src.config.config import get_settings
from src.schema.food_detection import FoodDetection
from src.trulens.recommender_tracking import RecommenderTracking
from src.service.image_pred_service import ImagePredictionService

SETTINGS = get_settings()

class RecommendationService():
    def __init__(self, trulens_tracker):
        self.trulens_tracker: RecommenderTracking = trulens_tracker
        

    def make_recommendation(self, image: UploadFile, img_pred_service: ImagePredictionService):
        """
        Service to detect food in an image
        """
        food_detection: FoodDetection = img_pred_service.detect_food(image)
        
        # Make prediction with trulens recorder
        with self.trulens_tracker.tru_llm_recorder as recording:
            return self.trulens_tracker.food_recommender.get_recommendation(food_detection.json())