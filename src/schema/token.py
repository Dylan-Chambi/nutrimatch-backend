from datetime import datetime
from langchain_core.pydantic_v1 import BaseModel, Field

class Token(BaseModel):
    email: str
    token: str
    tokensInputUsage: int = Field(0, ge=0)
    tokensOutputUsage: int = Field(0, ge=0)
    totalTokensUsage: int = Field(0, ge=0)
    isTokenActive: bool = Field(True)
    dateCreated: datetime = Field(datetime.now())
    dateUpdated: datetime = Field(datetime.now())