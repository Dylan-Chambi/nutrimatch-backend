from fastapi import APIRouter
from src.routers.v1.endpoints import image_router, recommendation_router

api_router = APIRouter()

api_router.include_router(image_router.food_detec_router, prefix="/food-detection", tags=["food-detection"])
api_router.include_router(recommendation_router.recommendation_router, prefix="/recommendation", tags=["recommendation"])