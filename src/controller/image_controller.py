import traceback
from fastapi import UploadFile, HTTPException
from src.service.image_pred_service import ImagePredictionService
from src.service.firestore_service import FirestoreService
from src.service.recomendation_service import RecommendationService
from src.schema.food_recommendation import FoodRecommendation
from src.schema.food_recommendation_document import FoodRecommendationDocument
from firebase_admin.auth import UserRecord


def image_detect_food(file: UploadFile, img_pred_service: ImagePredictionService):
    """
    Controller to detect food in an image
    """   
    try:
        res = img_pred_service.detect_food(file)
        return res
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error") from e

def get_recomendation_by_image(
        user_info: UserRecord, 
        file: UploadFile, 
        img_pred_service: ImagePredictionService, 
        recommender_service: RecommendationService, 
        firestore_service: FirestoreService
    ) -> FoodRecommendationDocument:
    """
    Controller to recommend food in an image
    """
    try:
        recommendation: FoodRecommendation = recommender_service.make_recommendation(file, img_pred_service)
        saved_recommendation: FoodRecommendationDocument = firestore_service.save_recommendation_by_user(recommendation, user_info, file)
        return saved_recommendation
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error") from e