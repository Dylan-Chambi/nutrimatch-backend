from fastapi import APIRouter, status, Depends
from typing import Annotated
from src.controller.recommendation_controller import get_recommendations, get_recommendation_by_id, delete_recommendation_by_id
from src.service.firestore_service import FirestoreService
from src.service.firebase_storage_service import FirebaseStorageService
from src.middleware.auth_middleware import authentication_jwt_middleware
from firebase_admin.auth import UserRecord



recommendation_router = APIRouter()

def get_firestore_service():
    firebase_storage_service = FirebaseStorageService()
    return FirestoreService(firebase_storage_service)

@recommendation_router.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    """
    return {"message": "Recommendation endpoint is healthy!"}


@recommendation_router.get("/get-recommendations")
async def recommendations(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], firestore_service: FirestoreService = Depends(get_firestore_service)):
    """
    Get user recommendations
    """
    return get_recommendations(user_info, firestore_service)


@recommendation_router.get("/get-recommendation/{recommendation_id}")
async def recommendation_by_id(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], recommendation_id: str, firestore_service: FirestoreService = Depends(get_firestore_service)):
    """
    Get recommendation by id
    """
    return get_recommendation_by_id(user_info, recommendation_id, firestore_service)


@recommendation_router.delete("/delete-recommendation/{recommendation_id}")
async def delete_recommendation(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], recommendation_id: str, firestore_service: FirestoreService = Depends(get_firestore_service)):
    """
    Delete recommendation by id
    """
    return delete_recommendation_by_id(user_info, recommendation_id, firestore_service)
