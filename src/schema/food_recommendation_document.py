from datetime import datetime
from src.schema.food_recommendation import FoodRecommendation


class FoodRecommendationDocument(FoodRecommendation):
    id: str
    timestamp: datetime
    image_url: str | None