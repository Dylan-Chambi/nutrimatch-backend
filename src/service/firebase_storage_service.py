import datetime
from firebase_admin import storage

class FirebaseStorageService:
    def __init__(self):
        self.bucket = storage.bucket()

    def upload_image(self, image_bytes: bytes, file_path: str):
        """
        Upload image to firebase storage
        """
        if image_bytes is None or file_path is None:
            return None
        blob = self.bucket.blob(file_path)
        blob.upload_from_string(image_bytes, content_type='image/webp')

        download_url = blob.generate_signed_url(datetime.timedelta(days=1), method='GET')
        return download_url
    
    def delete_image(self, file_path: str):
        """
        Delete image from firebase storage
        """
        if file_path is None:
            return False
        blob = self.bucket.blob(file_path)
        blob.delete()
        return True
    
    def get_image_url(self, file_path: str):
        """
        Get image url from firebase storage
        """
        if file_path is None:
            return None
        blob = self.bucket.blob(file_path)
        download_url = blob.generate_signed_url(datetime.timedelta(days=1), method='GET')
        return download_url