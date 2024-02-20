import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", ".env"))
    
    API_V1_STR: str = "/api/v1"
    API_NAME: str = "NutriMatch API"
    REVISION: str = "local"
    OPENAI_CHAT_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_VISION_MODEL: str = "gpt-4-vision-preview"
    TRULENS_DB_URL: str = "sqlite:///trulens.db"
    OPENAI_KEY: str

@cache
def get_settings() -> Settings:
    return Settings()