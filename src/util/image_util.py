import io
from PIL import Image
from fastapi import UploadFile


MAX_IMAGE_SIZE = (2048, 2048)

def convet_file_webp(file: UploadFile):
    img_stream = io.BytesIO(file.file.read())
    img_obj = Image.open(img_stream)
    img_obj.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
    webp_stream = io.BytesIO()
    img_obj.save(webp_stream, format='WebP')
    return webp_stream.getvalue()