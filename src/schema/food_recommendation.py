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


class FoodRecommendation(BaseModel):
    valid_user_input: bool
    error_message: Optional[str]
    general_description: Optional[str]
    general_recommendation: Optional[str]
    general_nutritional_score: Optional[int] = Field(ge=0, le=100)
    nutritional_info_unit: Optional[str]
    food_recommendations: Optional[list[FoodRecommendationItem]]


    
    
