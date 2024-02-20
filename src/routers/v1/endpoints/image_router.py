from fastapi import APIRouter, UploadFile, status, Depends
from src.controller.image_controller import image_detect_food, get_recomendation_by_image
from src.middleware.image_middleware import ImageValidationMiddleware
from src.service.image_pred_service import ImagePredictionService
from src.trulens.detector_tracking import DetectorTracking
from src.trulens.recommender_tracking import RecommenderTracking
from src.service.recomendation_service import RecommendationService


food_detec_router = APIRouter()



def get_image_pred_service():
    detector_tracking = DetectorTracking()
    return ImagePredictionService(detector_tracking)


def get_recommendation_service():
    recommender_tracking = RecommenderTracking()
    return RecommendationService(recommender_tracking)

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
        file: UploadFile = Depends(ImageValidationMiddleware()), 
        img_pred_service: ImagePredictionService = Depends(get_image_pred_service), 
        recommender_service: RecommendationService = Depends(get_recommendation_service)
    ):
    """
    Recommend food in an image
    """
    
    return get_recomendation_by_image(file, img_pred_service, recommender_service)