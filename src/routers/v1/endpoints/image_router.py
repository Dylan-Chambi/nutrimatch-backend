from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, FileResponse
from fastapi import HTTPException, status


food_detec_router = APIRouter()

@food_detec_router.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    return {"message": "Food detection endpoint is healthy!"}