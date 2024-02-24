from fastapi import APIRouter, UploadFile, status, Depends
from typing import Annotated
from src.controller.image_controller import image_detect_food, get_recomendation_by_image
from src.middleware.image_middleware import ImageValidationMiddleware
from src.service.image_pred_service import ImagePredictionService
from src.service.firestore_service import FirestoreService
from src.service.firebase_storage_service import FirebaseStorageService
from src.service.recomendation_service import RecommendationService
from src.middleware.auth_middleware import authentication_jwt_middleware
from firebase_admin.auth import UserRecord
from src.predictor.gpt_food_detector import GPTFoodDetector
from src.predictor.gpt_food_recommender import GPTFoodRecommender



food_detec_router = APIRouter()



def get_image_pred_service():
    gpt_food_detector = GPTFoodDetector()
    return ImagePredictionService(gpt_food_detector)


def get_recommendation_service():
    gpt_food_recommender = GPTFoodRecommender()
    return RecommendationService(gpt_food_recommender)

def get_firestore_service():
    firebase_storage_service = FirebaseStorageService()
    return FirestoreService(firebase_storage_service)


@food_detec_router.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    """
    return {"message": "Food detection endpoint is healthy!"}


@food_detec_router.post('/image')
def detect_food(file: UploadFile = Depends(ImageValidationMiddleware()), img_pred_service: ImagePredictionService = Depends(get_image_pred_service)):
    """
    Detect food in an image
    """
    
    return image_detect_food(file, img_pred_service)


@food_detec_router.post('/recommendation')
def recommend_food(
        user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)],
        file: UploadFile = Depends(ImageValidationMiddleware()), 
        img_pred_service: ImagePredictionService = Depends(get_image_pred_service), 
        recommender_service: RecommendationService = Depends(get_recommendation_service),
        firestore_service: FirestoreService = Depends(get_firestore_service)
    ):
    """
    Recommend food in an image
    """
    
    return get_recomendation_by_image(user_info, file, img_pred_service, recommender_service, firestore_service)
