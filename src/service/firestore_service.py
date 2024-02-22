from fastapi import HTTPException
from firebase_admin import firestore
from firebase_admin.auth import UserRecord
from src.schema.food_recommendation import FoodRecommendation
from src.schema.food_recommendation_document import FoodRecommendationDocument

class FirestoreService:
    def __init__(self):
        self.db = firestore.client()

    def save_recommendation_by_user(self, recommendation: FoodRecommendation, user_info: UserRecord) -> FoodRecommendationDocument:
        """
        Save recommendation by user
        """
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        data = recommendation.dict()
        data_with_timestamp = {**data, "timestamp": firestore.SERVER_TIMESTAMP}
        saved = col_ref.add(data_with_timestamp)
        return FoodRecommendationDocument(**saved[1].get().to_dict(), id=saved[1].id)
        

    def get_user_recommendations(self, user_info: UserRecord) -> list[FoodRecommendationDocument]:
        """
        Get user recommendations
        """
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        docs = col_ref.stream()
        recommendations = []
        for doc in docs:
            rec = FoodRecommendationDocument(**doc.to_dict(), id=doc.id)
            recommendations.append(rec)

        recommendations.sort(key=lambda x: x.timestamp, reverse=True)
        return recommendations
    

    def get_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str) -> FoodRecommendationDocument:
        """
        Get recommendation by id
        """
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        doc = col_ref.document(recommendation_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        return FoodRecommendationDocument(**doc.to_dict(), id=doc.id)
    
    
    def delete_recommendation_by_id(self, user_info: UserRecord, recommendation_id: str):
        """
        Delete recommendation by id
        """
        col_ref = self.db.collection('users').document(user_info.uid).collection('recommendations')
        if not col_ref.document(recommendation_id).get().exists:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        deleted = col_ref.document(recommendation_id).delete()
        return deleted