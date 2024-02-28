import traceback
from fastapi import HTTPException
from src.model.general_database import GeneralDatabase
from src.schema.food_recommendation_document import FoodRecommendationDocument
from firebase_admin.auth import UserRecord
from src.config.logger import logger
from src.service.mongodb.keys_service import KeysService
from src.schema.token import Token


def get_keys(user_info: UserRecord, key_service: KeysService) -> list[Token]:
    """
    Get user recommendations
    """
    try:
        return key_service.get_all_keys()
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error getting keys for user {user_info.uid}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
    

def add_new_key(user_info: UserRecord, token: str, email: str, tier: int, key_service: KeysService) -> Token:
    """
    Add key
    """
    try:
        key = Token(email=email, token=token, tier=tier)
        return key_service.add_key(key)
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error adding key for user {user_info.uid} with key {token}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
    

def deactivate_key(user_info: UserRecord, token: str, key_service: KeysService) -> Token:
    """
    Deactivate key
    """
    try:
        return key_service.deactivate_key_by_token(token)
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error deactivating key for user {user_info.uid} with key {token}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
    

def get_last_valid_key(user_info: UserRecord, tier: int, key_service: KeysService) -> Token:
    """
    Get last active key
    """
    try:
        return key_service.get_last_key_active(tier)
    except HTTPException as e:
        traceback.print_exc()
        raise e
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error getting last active key for user {user_info.uid}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e