from fastapi import UploadFile
from src.template.food_recomendation_template import FOOD_RECOMMENDATION_TEMPLATE
from src.config.config import get_settings
from src.schema.food_detection import FoodDetection
from src.service.image_pred_service import ImagePredictionService
from src.schema.food_recommendation import FoodRecommendation
from src.predictor.gpt_food_recommender import GeneralFoodRecommender

SETTINGS = get_settings()

class RecommendationService():
    def __init__(self, gpt_food_recommender: GeneralFoodRecommender):
        self.gpt_food_recommender = gpt_food_recommender
        

    def make_recommendation(self, image: UploadFile, img_pred_service: ImagePredictionService) -> FoodRecommendation:
        """
        Service to detect food in an image
        """
        food_detection: FoodDetection = img_pred_service.detect_food(image)
        return self.gpt_food_recommender.get_recommendation(food_detection.json(), FOOD_RECOMMENDATION_TEMPLATE)