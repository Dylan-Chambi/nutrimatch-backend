import uuid
from pymongo import MongoClient
from fastapi import HTTPException
from datetime import datetime
from src.config.logger import logger
from src.config.config import get_settings
from src.schema.token import Token

SETTINGS = get_settings()

class KeysService:
    def __init__(self):
        self.client = MongoClient(SETTINGS.MONGODB_URI)
        self.client['keys']['tokens_data'].create_index([("id", 1)], unique=True)


    def get_all_keys(self) -> list[Token]:
        """
        Get all keys
        """
        logger.info({"method": "get_all_keys", "message": "Getting all keys"})
        db = self.client['keys']
        col = db['tokens_data']
        keys = col.find({})
        return [Token(**key) for key in keys]
    
    def add_key(self, key: Token) -> Token:
        """
        Add key
        """
        logger.info({"method": "add_key", "message": f"Adding key {key}"})
        db = self.client['keys']
        col = db['tokens_data']
        col.insert_one(key.dict())
        return key
    

    def update_key_by_token(self, token: str, email: str = None, tokensInputUsage: int = None, tokensOutputUsage: int = None, totalTokensUsage: int = None, isTokenActive: bool = None) -> Token:
        """
        Update key by token
        """
        logger.info({"method": "update_key_by_token", "message": f"Updating key by token {token}"})
        db = self.client['keys']
        col = db['tokens_data']
        update_dict = {}
        if email is not None:
            update_dict["email"] = email
        if tokensInputUsage is not None:
            update_dict["tokensInputUsage"] = tokensInputUsage
        if tokensOutputUsage is not None:
            update_dict["tokensOutputUsage"] = tokensOutputUsage
        if totalTokensUsage is not None:
            update_dict["totalTokensUsage"] = totalTokensUsage
        if isTokenActive is not None:
            update_dict["isTokenActive"] = isTokenActive
        update_dict["dateUpdated"] = datetime.now()
        col.update_one({"token": token}, {"$set": update_dict})
        data =  col.find_one({"token": token})
        return Token(**data)
        
    
    def deactivate_key_by_token(self, token: str) -> Token:
        """
        Deactivate key by token
        """
        logger.info({"method": "deactivate_key_by_token", "message": f"Deactivating key by token {token}"})
        return self.update_key_by_token(token, isTokenActive=False)
    

    def get_last_key_active(self) -> Token:
        """
        Get last active key
        """
        logger.info({"method": "get_last_key_active", "message": "Getting last active key"})
        db = self.client['keys']
        col = db['tokens_data']
        keys = col.find({"isTokenActive": True}).sort("dateCreated", -1)
        if keys and len(list(keys)) > 0:
            return Token(**keys[0])
        else:
            raise HTTPException(status_code=404, detail="No active keys found")

    