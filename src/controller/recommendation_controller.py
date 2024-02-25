import traceback
from fastapi import HTTPException
from src.service.firestore_service import FirestoreService
from src.schema.food_recommendation_document import FoodRecommendationDocument
from firebase_admin.auth import UserRecord
from src.config.logger import logger


def get_recommendations(user_info: UserRecord, firestore_service: FirestoreService) -> list[FoodRecommendationDocument]:
    """
    Get user recommendations
    """
    try:
        return firestore_service.get_user_recommendations(user_info)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error getting recommendations for user {user_info.uid}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
    

def get_recommendation_by_id(user_info: UserRecord, recommendation_id: str, firestore_service: FirestoreService) -> FoodRecommendationDocument:
    """
    Get recommendation by id
    """
    try:
        return firestore_service.get_recommendation_by_id(user_info, recommendation_id)
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error getting recommendation for user {user_info.uid} with recommendation id {recommendation_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
    

def delete_recommendation_by_id(user_info: UserRecord, recommendation_id: str, firestore_service: FirestoreService):
    """
    Delete recommendation by id
    """
    try:
        return firestore_service.delete_recommendation_by_id(user_info, recommendation_id)
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error deleting recommendation for user {user_info.uid} with recommendation id {recommendation_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e