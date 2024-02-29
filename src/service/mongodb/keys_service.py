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
    

    def get_last_key_active(self, tier: int) -> Token:
        """
        Get last active key
        """
        logger.info({"method": "get_last_key_active", "message": "Getting last active key"})
        db = self.client['keys']
        col = db['tokens_data']
        keys = col.find({"isTokenActive": True, "tier": tier}).sort("dateCreated", -1).limit(1)
        keys_arr = list(keys)
        if keys and len(keys_arr) > 0:
            return Token(**keys_arr[0])
        else:
            logger.error({"method": "get_last_key_active", "message": f"No active keys found: {keys_arr}"})
            raise HTTPException(status_code=404, detail="No active keys found")
        

    def add_tokens_usage_by_token(self, token: str, tokensInputUsage: int, tokensOutputUsage: int, totalTokensUsage: int, model_name: str) -> Token:
        """
        Add tokens usage by token
        """
        logger.info({"method": "add_tokens_usage_by_token", "message": f"Adding tokens usage by token {token}, tokensInputUsage: {tokensInputUsage}, tokensOutputUsage: {tokensOutputUsage}, totalTokensUsage: {totalTokensUsage}, model_name: {model_name}"})
        db = self.client['keys']
        col = db['tokens_data']
        input_price, output_price = self.token_to_usd(tokensInputUsage, tokensOutputUsage, model_name)
        data =  col.find_one({"token": token})
        if data:
            data["tokensInputUsage"] += tokensInputUsage
            data["tokensOutputUsage"] += tokensOutputUsage
            data["totalTokensUsage"] += totalTokensUsage
            data["inputPricing"] += input_price
            data["outputPricing"] += output_price
            data["totalPricing"] += input_price + output_price
            data["totalUsages"] += 1
            data["dateUpdated"] = datetime.now()
            col.update_one({"token": token}, {"$set": data})
            updated_data =  col.find_one({"token": token})
            logger.info({"method": "add_tokens_usage_by_token", "message": f"Added tokens usage by token {token}, tokensInputUsage: {tokensInputUsage}, tokensOutputUsage: {tokensOutputUsage}, totalTokensUsage: {totalTokensUsage}, InputPricing: {input_price}, OutputPricing: {output_price}, TotalPricing: {input_price + output_price}"})
            return Token(**updated_data)
        else:
            logger.error({"method": "add_tokens_usage_by_token", "message": f"No key found for token {token}"})
            raise HTTPException(status_code=404, detail=f"No key found for token {token}")
    
    def token_to_usd(self, input_tokens: int, output_tokens: int, model_name: str) -> tuple[float, float]:
        """
        Calculate the price of the tokens
        """
        match = {
            "gpt-4-0125-preview": {"input": 0.01, "output": 0.03},
            "gpt-4-1106-preview": {"input": 0.01, "output": 0.03},
            "gpt-4-1106-vision-preview": {"input": 0.01, "output": 0.03},
            "gpt-4-vision-preview": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo-0125": {"input": 0.0005, "output": 0.0015},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        }
        input_price = input_tokens * match[model_name]["input"] / 1000
        output_price = output_tokens * match[model_name]["output"] / 1000


        logger.info({"method": "token_to_usd", "message": f"Converting input_tokens: {input_tokens}, output_tokens: {output_tokens}, model_name: {model_name} to input_price: {input_price}, output_price: {output_price}"})
        return input_price, output_price

    