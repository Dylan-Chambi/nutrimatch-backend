from fastapi import APIRouter, UploadFile, status, Depends
from typing import Annotated
from src.controller.prediction_controller import image_detect_food, get_recomendation_by_image
from src.middleware.image_middleware import ImageValidationMiddleware
from src.service.image_pred_service import ImagePredictionService
from src.model.general_database import GeneralDatabase
from src.service.mongodb.mongodb_service import MongoDBService
from src.service.firebase.firebase_storage_service import FirebaseStorageService
from src.service.recomendation_service import RecommendationService
from src.middleware.auth_middleware import authentication_jwt_middleware
from firebase_admin.auth import UserRecord
from src.predictor.gpt_food_detector import GPTFoodDetector
from src.predictor.gpt_food_recommender import GPTFoodRecommender
from src.config.logger import logger



prediction_router = APIRouter()



def get_image_pred_service():
    gpt_food_detector = GPTFoodDetector()
    return ImagePredictionService(gpt_food_detector)


def get_recommendation_service():
    gpt_food_recommender = GPTFoodRecommender()
    return RecommendationService(gpt_food_recommender)

def get_database_service():
    firebase_storage_service = FirebaseStorageService()
    return MongoDBService(firebase_storage_service)


@prediction_router.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    """
    logger.info({"route": "/health_check", "message": "Health check endpoint is healthy!"})
    return {"message": "Food detection endpoint is healthy!"}


@prediction_router.post('/food-detection')
def detect_food(
        user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)],
        file: UploadFile = Depends(ImageValidationMiddleware()), 
        img_pred_service: ImagePredictionService = Depends(get_image_pred_service)
    ):
    """
    Detect food in an image
    """
    logger.info({"route": "/image", "message": f"Detecting food in image for file {file.filename}"})
    return image_detect_food(file, img_pred_service)


@prediction_router.post('/recommendation')
def recommend_food(
        user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)],
        file: UploadFile = Depends(ImageValidationMiddleware()), 
        img_pred_service: ImagePredictionService = Depends(get_image_pred_service), 
        recommender_service: RecommendationService = Depends(get_recommendation_service),
        database_service: GeneralDatabase = Depends(get_database_service)
    ):
    """
    Recommend food in an image
    """
    logger.info({"route": "/recommendation", "message": f"Recommending food in image for user {user_info.uid} and file {file.filename}"})
    return get_recomendation_by_image(user_info, file, img_pred_service, recommender_service, database_service)
