from langchain_core.pydantic_v1 import BaseModel
from typing import Optional

class FoodItem(BaseModel):
    name: str
    size: int
    size_unit: str
    amount: int
    confidence: float
    seasonings: Optional[list[str]]
    ingredients: Optional[list[str]]

    def __str__(self):
        return f"FoodItem(name={self.name}, size={self.size}, size_unit={self.size_unit}, amount={self.amount}, confidence={self.confidence}, seasonings={self.seasonings}, ingredients={self.ingredients})"

class FoodDetection(BaseModel):
    valid_food_image: bool
    error_reason: Optional[str]
    general_description: Optional[str]
    food_items: Optional[list[FoodItem]]

    def __str__(self):
        return f"FoodDetection(valid_food_image={self.valid_food_image}, error_reason={self.error_reason}, general_description={self.general_description}, food_items={self.food_items})"
    
    
