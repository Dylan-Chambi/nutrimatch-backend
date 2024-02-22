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
        return FoodRecommendationDocument(**saved[1].get().to_dict())