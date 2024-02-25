from datetime import datetime
from src.schema.food_recommendation import FoodRecommendation


class FoodRecommendationDocument(FoodRecommendation):
    id: str
    timestamp: datetime
    image_url: str | None

    def __str__(self):
        return f"FoodRecommendationDocument(id={self.id}, timestamp={self.timestamp}, image_url={self.image_url}, valid_user_input={self.valid_user_input}, error_message={self.error_message}, short_food_name={self.short_food_name}, general_description={self.general_description}, general_recommendation={self.general_recommendation}, general_nutritional_score={self.general_nutritional_score}, nutritional_info_unit={self.nutritional_info_unit}, food_recommendations={self.food_recommendations})"