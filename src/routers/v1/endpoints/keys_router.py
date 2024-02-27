from fastapi import APIRouter, status, Depends
from typing import Annotated
from src.controller.keys_controller import get_keys, add_new_key, deactivate_key, get_last_valid_key
from src.service.mongodb.keys_service import KeysService
from src.middleware.auth_middleware import authentication_jwt_middleware
from firebase_admin.auth import UserRecord
from src.config.logger import logger



keys_router = APIRouter()

def get_keys_service():
    return KeysService()

@keys_router.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    """
    logger.info({"route": "/health_check", "message": "Health check endpoint is healthy!"})
    return {"message": "Keys endpoint is healthy!"}


@keys_router.get("/get-keys")
async def keys(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], key_service: KeysService = Depends(get_keys_service)):
    """
    Get all keys
    """
    logger.info({"route": "/keys", "message": f"Getting keys for user {user_info.uid}"})
    return get_keys(user_info, key_service)

@keys_router.post("/add-key")
async def post_key(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], token: str, email: str, key_service: KeysService = Depends(get_keys_service)):
    """
    Add key
    """
    logger.info({"route": "/add-key", "message": f"Adding key for user {user_info.uid}"})
    return add_new_key(user_info, token, email, key_service)

@keys_router.patch("/deactivate-key")
async def modify_key(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], token: str, key_service: KeysService = Depends(get_keys_service)):
    """
    Deactivate key
    """
    logger.info({"route": "/deactivate-key", "message": f"Deactivating key for user {user_info.uid}"})
    return deactivate_key(user_info, token, key_service)

@keys_router.get("/get-last-active-key")
async def get_active_key(user_info: Annotated[UserRecord, Depends(authentication_jwt_middleware)], key_service: KeysService = Depends(get_keys_service)):
    """
    Get last active key
    """
    logger.info({"route": "/get-last-active-key", "message": f"Getting last active key for user {user_info.uid}"})
    return get_last_valid_key(user_info, key_service)


