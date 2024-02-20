import base64
from fastapi import UploadFile
from src.service.image_pred_service import ImagePredictionService


def image_detect_food(file: UploadFile, img_pred_service: ImagePredictionService):
    """
    Controller to detect food in an image
    """
    
    image_b64 = base64.b64encode(file.file.read()).decode("utf-8")
    
    image_b64 = f"data:{file.content_type};base64,{image_b64}"
    
    res = img_pred_service.detect_food(image_b64)
    
    return res
