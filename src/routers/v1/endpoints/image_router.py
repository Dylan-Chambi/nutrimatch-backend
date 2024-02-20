from fastapi import APIRouter, UploadFile, status, Depends
from src.controller.image_controller import image_detect_food
from src.middleware.image_middleware import ImageValidationMiddleware
from src.service.image_pred_service import ImagePredictionService
from src.predictor.gpt_food_detector import GPTFoodDetector


food_detec_router = APIRouter()



def get_image_pred_service():
    food_detector = GPTFoodDetector()
    return ImagePredictionService(food_detector)

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