from fastapi import HTTPException, UploadFile
from firebase_admin import firestore
from firebase_admin.auth import UserRecord
from src.service.firebase_storage_service import FirebaseStorageService
from src.schema.food_recommendation import FoodRecommendation
from src.schema.food_recommendation_document import FoodRecommendationDocument
from src.util.image_util import convet_file_webp
import concurrent
from src.config.logger import logger

class FirestoreService:
    def __init__(self, firebase_storage_service: FirebaseStorageService):
        self.db = firestore.client()
        self.firebase_storage_service = firebase_storage_service

    def save_recommendation_by_user(
            self, 
            recommendation: FoodRecommendation, 
            user_info: UserRecord, 
            image: UploadFile
        ) -> FoodRecommendationDocument:
        """
        Save recommendation by user
        """
        # logger.info({"method": "save_recommendation_by_user", "message": f"Saving recommendation by user {user_info.uid} with recommendation {recommendation} and image {image.filename}"})
        logger.info({"method": "save_recommendation_by_user", "message": f"Saving recommendation by user {user_info.uid} with recommendation {str(recommendation)[:100]}... and image {image.filename}"})
        if not recommendation.valid_user_input:
            raise HTTPException(status_code=400, detail=recommendation.error_message)
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        data = recommendation.dict()
        data_with_timestamp = {**data, "timestamp": firestore.SERVER_TIMESTAMP}
        saved = col_ref.add(data_with_timestamp)

        # Save image to firebase storage
        image_webp = convet_file_webp(image)
        image_path = f"users/{user_info.uid}/recommendations/{saved[1].id}.webp"
        image_url = self.firebase_storage_service.upload_image(image_webp, image_path)

        # Update the recommendation with the image path
        col_ref.document(saved[1].id).update({"image_path": image_path})

        logger.info({"method": "save_recommendation_by_user", "message": f"Saved recommendation by user {user_info.uid} with recommendation {str(recommendation)[:100]}... and image {image.filename} and image path {image_path} and image url {image_url[:50]}..."})
        return FoodRecommendationDocument(**saved[1].get().to_dict(), id=saved[1].id, image_url=image_url)
        

    def get_user_recommendations(self, user_info: UserRecord) -> list[FoodRecommendationDocument]:
        """
        Get user recommendations
        """
        logger.info({"method": "get_user_recommendations", "message": f"Getting recommendations for user {user_info.uid}"})
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        docs = col_ref.stream()
        recommendations = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_doc = {executor.submit(self.get_image_url, doc): doc for doc in docs}
            for future in concurrent.futures.as_completed(future_to_doc):
                doc: firestore.DocumentSnapshot = future_to_doc[future]
                try:
                    image_url = future.result()
                    doc_dict = doc.to_dict()
                    rec = FoodRecommendationDocument(**doc_dict, id=doc.id, image_url=image_url)
                    recommendations.append(rec)
                except Exception as e:
                    # Handle exception if the retrieval of image URL fails
                    print(f"Error retrieving image URL: {e}")

        recommendations.sort(key=lambda x: x.timestamp, reverse=True)
        logger.info({"method": "get_user_recommendations", "message": f"Got recommendations for user {user_info.uid}, recommendations size: {len(recommendations)} and recommendations: {str(recommendations)[:100]}"})
        return recommendations

    def get_image_url(self, doc) -> str:
        """
        Get image URL for a document
        """
        doc_dict = doc.to_dict()
        logger.info({"method": "get_image_url", "message": f"Getting image URL for document {str(doc_dict)[:100]}..."})
        image_path = doc_dict.get('image_path')
        if image_path:
            logger.info({"method": "get_image_url", "message": f"Got image URL for document {str(doc_dict)[:100]} with image path {image_path[:50]}..."})
            return self.firebase_storage_service.get_image_url(image_path)
        logger.info({"method": "get_image_url", "message": f"Document {str(doc_dict)[:100]} does not have an image path"})
        return None
    

    def get_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str) -> FoodRecommendationDocument:
        """
        Get recommendation by id
        """
        logger.info({"method": "get_recommendation_by_id", "message": f"Getting recommendation for user {user_info.uid} with recommendation id {recommendation_id}"})
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        data = col_ref.document(recommendation_id).get()
        if not data.exists:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        data_dict = data.to_dict()
        food_rec_doc = FoodRecommendationDocument(**data_dict, id=data.id, image_url=self.firebase_storage_service.get_image_url(data_dict['image_path'] if 'image_path' in data_dict else None))
        logger.info({"method": "get_recommendation_by_id", "message": f"Got recommendation for user {user_info.uid} with recommendation id {recommendation_id} and recommendation {str(food_rec_doc)[:100]}..."})
        return food_rec_doc
    
    
    def delete_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str):
        """
        Delete recommendation by id
        """
        logger.info({"method": "delete_recommendation_by_id", "message": f"Deleting recommendation for user {user_info.uid} with recommendation id {recommendation_id}"})
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        data_dict = col_ref.document(recommendation_id).get().to_dict()
        if not data_dict:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        self.firebase_storage_service.delete_image(data_dict['image_path'] if 'image_path' in data_dict else None)
        deleted = col_ref.document(recommendation_id).delete()
        logger.info({"method": "delete_recommendation_by_id", "message": f"Deleted recommendation for user {user_info.uid} with recommendation id {recommendation_id}"})
        return deleted