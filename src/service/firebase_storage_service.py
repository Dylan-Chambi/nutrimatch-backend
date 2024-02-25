import datetime
from firebase_admin import storage
from src.config.logger import logger

class FirebaseStorageService:
    def __init__(self):
        self.bucket = storage.bucket()

    def upload_image(self, image_bytes: bytes, file_path: str):
        """
        Upload image to firebase storage
        """
        logger.info({"method": "upload_image", "message": f"Uploading image to firebase storage to file path {file_path}"})
        if image_bytes is None or file_path is None:
            return None
        blob = self.bucket.blob(file_path)
        blob.upload_from_string(image_bytes, content_type='image/webp')

        download_url = blob.generate_signed_url(datetime.timedelta(days=1), method='GET')
        logger.info({"method": "upload_image", "message": f"Uploaded image to firebase storage to file path {file_path} with download url {download_url[:50]}..."})
        return download_url
    
    def delete_image(self, file_path: str):
        """
        Delete image from firebase storage
        """
        logger.info({"method": "delete_image", "message": f"Deleting image from firebase storage from file path {file_path}"})
        if file_path is None:
            return False
        blob = self.bucket.blob(file_path)
        blob.delete()
        logger.info({"method": "delete_image", "message": f"Deleted image from firebase storage from file path {file_path}"})
        return True
    
    def get_image_url(self, file_path: str):
        """
        Get image url from firebase storage
        """
        logger.info({"method": "get_image_url", "message": f"Getting image url from firebase storage from file path {file_path}"})
        if file_path is None:
            return None
        blob = self.bucket.blob(file_path)
        download_url = blob.generate_signed_url(datetime.timedelta(days=1), method='GET')
        logger.info({"method": "get_image_url", "message": f"Got image url from firebase storage from file path {file_path} with download url {download_url[:50]}..."})
        return download_url