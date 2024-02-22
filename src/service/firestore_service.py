from fastapi import HTTPException, UploadFile
from firebase_admin import firestore
from firebase_admin.auth import UserRecord
from src.service.firebase_storage_service import FirebaseStorageService
from src.schema.food_recommendation import FoodRecommendation
from src.schema.food_recommendation_document import FoodRecommendationDocument
from src.util.image_util import convet_file_webp

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

        return FoodRecommendationDocument(**saved[1].get().to_dict(), id=saved[1].id, image_url=image_url)
        

    def get_user_recommendations(self, user_info: UserRecord) -> list[FoodRecommendationDocument]:
        """
        Get user recommendations
        """
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        docs = col_ref.stream()
        recommendations = []
        for doc in docs:
            doc_dict = doc.to_dict()
            rec = FoodRecommendationDocument(**doc_dict, id=doc.id, image_url=self.firebase_storage_service.get_image_url(doc_dict['image_path'] if 'image_path' in doc_dict else None))
            recommendations.append(rec)

        recommendations.sort(key=lambda x: x.timestamp, reverse=True)
        return recommendations
    

    def get_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str) -> FoodRecommendationDocument:
        """
        Get recommendation by id
        """
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        data = col_ref.document(recommendation_id).get()
        if not data.exists:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        data_dict = data.to_dict()
        return FoodRecommendationDocument(**data_dict, id=data.id, image_url=self.firebase_storage_service.get_image_url(data_dict['image_path'] if 'image_path' in data_dict else None))
    
    
    def delete_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str):
        """
        Delete recommendation by id
        """
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        data_dict = col_ref.document(recommendation_id).get().to_dict()
        if not data_dict:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        self.firebase_storage_service.delete_image(data_dict['image_path'] if 'image_path' in data_dict else None)
        deleted = col_ref.document(recommendation_id).delete()
        return deleted