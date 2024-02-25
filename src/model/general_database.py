from abc import ABC, abstractmethod
from fastapi import UploadFile
from src.schema.food_recommendation import FoodRecommendation
from src.schema.food_recommendation_document import FoodRecommendationDocument
from firebase_admin.auth import UserRecord


class GeneralDatabase(ABC):
    @abstractmethod
    def save_recommendation_by_user(self, recommendation: FoodRecommendation, user_info: UserRecord, image: UploadFile) -> FoodRecommendationDocument:
        pass

    @abstractmethod
    def get_user_recommendations(self, user_info: UserRecord) -> list[FoodRecommendationDocument]:
        pass

    @abstractmethod
    def get_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str) -> FoodRecommendationDocument:
        pass

    @abstractmethod
    def delete_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str):
        pass

    @abstractmethod
    def get_image_url(self, doc) -> str:
        pass