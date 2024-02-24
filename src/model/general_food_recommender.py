from abc import ABC
from src.schema.food_detection import FoodDetection

class GeneralFoodRecommender(ABC):
    def __init__(self, model, model_name):
        self.model_name = model_name
        self.model = model

    def get_recommendation(self, food_detection: FoodDetection, recommender_context_template: str):
        pass