from datetime import datetime
from src.schema.food_recommendation import FoodRecommendation


class FoodRecommendationDocument(FoodRecommendation):
    timestamp: datetime