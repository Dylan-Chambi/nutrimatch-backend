from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional
from src.schema.food_detection import FoodItem


class FoodRecommendationItem(FoodItem):
    recommendation: str
    nutritional_score: int = Field(ge=0, le=100)
    calories: Optional[int] = Field(ge=0)
    carbohydrates: Optional[int] = Field(ge=0)
    fat: Optional[int] = Field(ge=0)
    protein: Optional[int] = Field(ge=0)
    fiber: Optional[int] = Field(ge=0)
    sugar: Optional[int] = Field(ge=0)
    sodium: Optional[int] = Field(ge=0)
    vitamin_a: Optional[int] = Field(ge=0)
    vitamin_c: Optional[int] = Field(ge=0)
    calcium: Optional[int] = Field(ge=0)
    iron: Optional[int] = Field(ge=0)
    cholesterol: Optional[int] = Field(ge=0)
    potassium: Optional[int] = Field(ge=0)
    warning: Optional[str]
    alternative_recommendation: Optional[str]
    alternative_nutritional_score: Optional[int] = Field(ge=0, le=100)

    def __str__(self):
        return f"FoodRecommendationItem(recommendation={self.recommendation}, nutritional_score={self.nutritional_score}, calories={self.calories}, carbohydrates={self.carbohydrates}, fat={self.fat}, protein={self.protein}, fiber={self.fiber}, sugar={self.sugar}, sodium={self.sodium}, vitamin_a={self.vitamin_a}, vitamin_c={self.vitamin_c}, calcium={self.calcium}, iron={self.iron}, cholesterol={self.cholesterol}, potassium={self.potassium}, warning={self.warning}, alternative_recommendation={self.alternative_recommendation}, alternative_nutritional_score={self.alternative_nutritional_score})"


class FoodRecommendation(BaseModel):
    valid_user_input: bool
    error_message: Optional[str]
    short_food_name: Optional[str] = Field(max_length=50)
    general_description: Optional[str]
    general_recommendation: Optional[str]
    general_nutritional_score: Optional[int] = Field(ge=0, le=100)
    nutritional_info_unit: Optional[str]
    food_recommendations: Optional[list[FoodRecommendationItem]]

    def __str__(self):
        return f"FoodRecommendation(valid_user_input={self.valid_user_input}, error_message={self.error_message}, short_food_name={self.short_food_name}, general_description={self.general_description}, general_recommendation={self.general_recommendation}, general_nutritional_score={self.general_nutritional_score}, nutritional_info_unit={self.nutritional_info_unit}, food_recommendations={self.food_recommendations})"


    
    
