import io
from fastapi import UploadFile, HTTPException, status, File
from PIL import Image



class ImageValidationMiddleware:
    def __call__(self, file: UploadFile = File(...)):
        # Check if the content type is an image
        if not file.content_type in ["image/jpeg", "image/png", "image/jpg", "image/webp"]:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only images with jpeg, jpg, png, and webp formats are supported"
            )
        
        # Check if the image is corrupted
        try:
            img_stream = io.BytesIO(file.file.read())
            Image.open(img_stream)
        except:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Image is corrupted or not supported"
            )
        finally:
            file.file.seek(0)
            img_stream.close()
            
        return file