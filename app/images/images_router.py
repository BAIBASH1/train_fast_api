"""
Router module for handling image uploads.

This module defines the FastAPI router for handling image uploads related to hotels.
It provides an endpoint for uploading hotel images, storing them in the static images directory,
and processing the images asynchronously using a background task.

Endpoints:
    - add_hotel_image: Uploads an image for a hotel, stores it, and triggers background image
     processing.
"""

import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import proceed_picture

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    """
    Asynchronously uploads and processes a hotel image.

    This endpoint allows users to upload an image for a hotel. The image is saved in the
    `app/static/images/` directory with the provided hotel name as the file name
    (with a `.webp` extension). After storing the file, a background task (`proceed_picture`)
    is triggered to process the image.

    Args:
        name (int): The ID or name associated with the hotel to which the image belongs.
        file (UploadFile): The image file being uploaded.

    Returns:
        dict: A message indicating the successful upload and processing initiation.
    """
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    proceed_picture.delay(im_path)
