import uuid
from pymongo import MongoClient
from fastapi import UploadFile, HTTPException
from src.model.general_database import GeneralDatabase
from src.schema.food_recommendation import FoodRecommendation
from src.schema.food_recommendation_document import FoodRecommendationDocument
from src.service.firebase.firebase_storage_service import FirebaseStorageService
from firebase_admin.auth import UserRecord
from src.util.image_util import convet_file_webp
import concurrent.futures
from datetime import datetime
from src.config.logger import logger
from src.config.config import get_settings

SETTINGS = get_settings()

class MongoDBService(GeneralDatabase):
    def __init__(self, firebase_storage_service: FirebaseStorageService):
        self.client = MongoClient(SETTINGS.MONGODB_URI)
        self.firebase_storage_service = firebase_storage_service
        self.client['nutrimatch']['recommendations'].create_index([("id", 1)], unique=True)

    def save_recommendation_by_user(self, recommendation: FoodRecommendation, user_info: UserRecord, image: UploadFile) -> FoodRecommendationDocument:
        logger.info({"method": "save_recommendation_by_user", "message": f"Saving recommendation by user {user_info.uid} with recommendation {str(recommendation)[:100]}... and image {image.filename}"})
        if not recommendation.valid_user_input:
            raise HTTPException(status_code=400, detail=recommendation.error_message)
        db = self.client['nutrimatch']
        col = db['recommendations']
        recommendation_id = str(uuid.uuid4())

        image_webp = convet_file_webp(image)
        image_path = f"users/{user_info.uid}/recommendations/{recommendation_id}.webp"
        image_url = self.firebase_storage_service.upload_image(image_webp, image_path)

        data = recommendation.dict()
        data_with_timestamp = {**data, "id": recommendation_id, "timestamp": datetime.now(), "image_path": image_path}
        col.update_one({ "_id": user_info.uid}, {"$push": {"recommendations": data_with_timestamp}}, upsert=True)

        saved = col.find_one({"_id": user_info.uid, "recommendations.id": recommendation_id})
        if not saved:
            raise HTTPException(status_code=404, detail="Failed to save recommendation")
        saved = next(filter(lambda x: x['id'] == recommendation_id, saved['recommendations']), None)

        logger.info({"method": "save_recommendation_by_user", "message": f"Saved recommendation by user {user_info.uid} with recommendation {str(saved)[:100]}... and image {image.filename} and image path {image_path} and image url {image_url[:50]}..."})
        return FoodRecommendationDocument(**saved, image_url=image_url)
    
    def get_user_recommendations(self, user_info: UserRecord) -> list[FoodRecommendationDocument]:
        """
        Get user recommendations
        """
        logger.info({"method": "get_user_recommendations", "message": f"Getting recommendations for user {user_info.uid}"})
        db = self.client['nutrimatch']
        col = db['recommendations']
        docs = col.find_one({"_id": user_info.uid})
        recommendations = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_doc = {executor.submit(self.get_image_url, doc): doc for doc in (docs['recommendations'] if docs else [])}
            for future in concurrent.futures.as_completed(future_to_doc):
                doc = future_to_doc[future]
                try:
                    image_url = future.result()
                    rec = FoodRecommendationDocument(**doc, image_url=image_url)
                    recommendations.append(rec)
                except Exception as e:
                    print(f"Error retrieving image URL: {e}")

        recommendations.sort(key=lambda x: x.timestamp, reverse=True)
        logger.info({"method": "get_user_recommendations", "message": f"Got recommendations for user {user_info.uid}, recommendations size: {len(recommendations)} and recommendations: {str(recommendations)[:100]}"})
        return recommendations
         
    def get_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str) -> FoodRecommendationDocument:
        """
        Get recommendation by id
        """
        logger.info({"method": "get_recommendation_by_id", "message": f"Getting recommendation for user {user_info.uid} with recommendation id {recommendation_id}"})
        db = self.client['nutrimatch']
        col = db['recommendations']
        rec = col.find_one({"_id": user_info.uid, "recommendations.id": recommendation_id})
        if not rec:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        rec = next(filter(lambda x: x['id'] == recommendation_id, rec['recommendations']), None)
        image_url = self.firebase_storage_service.get_image_url(rec['image_path'])
        food_rec_doc = FoodRecommendationDocument(**rec, image_url=image_url)
        logger.info({"method": "get_recommendation_by_id", "message": f"Got recommendation for user {user_info.uid} with recommendation id {recommendation_id} and recommendation {str(food_rec_doc)[:100]}..."})
        return food_rec_doc
    
    def delete_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str):
        """
        Delete recommendation by id
        """
        logger.info({"method": "delete_recommendation_by_id", "message": f"Deleting recommendation for user {user_info.uid} with recommendation id {recommendation_id}"})
        db = self.client['nutrimatch']
        col = db['recommendations']
        rec = col.find_one({"_id": user_info.uid, "recommendations.id": recommendation_id})
        if not rec:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        
        self.firebase_storage_service.delete_image(rec['image_path'] if 'image_path' in rec else None)
        
        col.update_one({"_id": user_info.uid}, {"$pull": {"recommendations": {"id": recommendation_id}}})
        logger.info({"method": "delete_recommendation_by_id", "message": f"Deleted recommendation for user {user_info.uid} with recommendation id {recommendation_id}"})
        return rec
        

    def get_image_url(self, doc) -> str:
        """
        Get image URL for a document
        """
        logger.info({"method": "get_image_url", "message": f"Getting image URL for document {str(doc)[:100]}..."})
        image_path = doc.get('image_path')
        if image_path:
            logger.info({"method": "get_image_url", "message": f"Got image URL for document {str(doc)[:100]} with image path {image_path[:50]}..."})
            return self.firebase_storage_service.get_image_url(image_path)
        logger.info({"method": "get_image_url", "message": f"Document {str(doc)[:100]} does not have an image path"})
        return None