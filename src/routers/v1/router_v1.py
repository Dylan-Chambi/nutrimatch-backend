from fastapi import APIRouter
from src.routers.v1.endpoints import prediction_router
from src.routers.v1.endpoints import recommendation_router

api_router = APIRouter()

api_router.include_router(prediction_router.prediction_router, prefix="/prediction", tags=["prediction"])
api_router.include_router(recommendation_router.recommendation_router, prefix="/recommendation", tags=["recommendation"])