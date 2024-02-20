from langchain_core.pydantic_v1 import BaseModel
from typing import Optional

class FoodItem(BaseModel):
    name: str
    size: int
    size_unit: str
    amount: int
    seasonings: str
    confidence: float
    ingredients: list[str]

class FoodDetection(BaseModel):
    valid_food_image: bool
    error_reason: Optional[str]
    general_description: Optional[str]
    food_items: Optional[list[FoodItem]]
    
    
