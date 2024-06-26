from datetime import datetime
from langchain_core.pydantic_v1 import BaseModel, Field

class Token(BaseModel):
    email: str
    token: str
    tier: int = Field(0, ge=0, le=2) # Ge = greater than or equal to, le = less than or equal to
    tokensInputUsage: int = Field(0, ge=0)
    tokensOutputUsage: int = Field(0, ge=0)
    totalTokensUsage: int = Field(0, ge=0)
    inputPricing: float = Field(0.0, ge=0.0)
    outputPricing: float = Field(0.0, ge=0.0)
    totalPricing: float = Field(0.0, ge=0.0)
    totalUsages: int = Field(0, ge=0)
    isTokenActive: bool = Field(True)
    dateCreated: datetime = Field(datetime.now())
    dateUpdated: datetime = Field(datetime.now())