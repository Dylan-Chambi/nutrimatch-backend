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
    OPENAI_KEY: str
    FIREBASE_TYPE: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: str
    FIREBASE_AUTH_URI: str
    FIREBASE_TOKEN_URI: str
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str
    FIREBASE_CLIENT_X509_CERT_URL: str
    FIREBASE_UNIVERSE_DOMAIN: str
    FIREBASE_STORAGE_BUCKET: str


@cache
def get_settings() -> Settings:
    return Settings()