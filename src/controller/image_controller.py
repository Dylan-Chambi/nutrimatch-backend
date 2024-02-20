from fastapi import UploadFile, HTTPException
from src.service.image_pred_service import ImagePredictionService


def image_detect_food(file: UploadFile, img_pred_service: ImagePredictionService):
    """
    Controller to detect food in an image
    """   
    try:
        res = img_pred_service.detect_food(file)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e
