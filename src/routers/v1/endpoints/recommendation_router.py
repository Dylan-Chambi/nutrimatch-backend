from fastapi import APIRouter, status, Depends
from typing import Annotated
from src.controller.recommendation_controller import get_recommendations, get_recommendation_by_id, delete_recommendation_by_id
from src.model.general_database import GeneralDatabase
from src.service.firebase.firestore_service import FirestoreService
from src.service.mongodb.mongodb_service import MongoDBService
from src.service.firebase.firebase_storage_service import FirebaseStorageService
from src.middleware.auth_middleware import authentication_jwt_middleware
from firebase_admin.auth import UserRecord
from src.config.logger import logger



recommendation_router = APIRouter()

def get_database_service():
    firebase_storage_service = FirebaseStorageService()
    return MongoDBService(firebase_storage_service)

@recommendation_router.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    """
    logger.info({"route": "/health_check", "message": "Health check endpoint is healthy!"})
    return {"message": "Recommendation endpoint is healthy!"}


@recommendation_router.get("/get-recommendations")
async def recommendations(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], firestore_service: GeneralDatabase = Depends(get_database_service)):
    """
    Get user recommendations
    """
    logger.info({"route": "/get-recommendations", "message": f"Getting recommendations for user {user_info.uid}"})
    return get_recommendations(user_info, firestore_service)


@recommendation_router.get("/get-recommendation/{recommendation_id}")
async def recommendation_by_id(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], recommendation_id: str, firestore_service: GeneralDatabase = Depends(get_database_service)):
    """
    Get recommendation by id
    """
    logger.info({"route": "/get-recommendation/{recommendation_id}", "message": f"Getting recommendation for user {user_info.uid} with recommendation id {recommendation_id}"})
    return get_recommendation_by_id(user_info, recommendation_id, firestore_service)


@recommendation_router.delete("/delete-recommendation/{recommendation_id}")
async def delete_recommendation(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], recommendation_id: str, firestore_service: GeneralDatabase = Depends(get_database_service)):
    """
    Delete recommendation by id
    """
    logger.info({"route": "/delete-recommendation/{recommendation_id}", "message": f"Deleting recommendation for user {user_info.uid} with recommendation id {recommendation_id}"})
    return delete_recommendation_by_id(user_info, recommendation_id, firestore_service)
