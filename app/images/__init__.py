"""
Image Upload Module

This package includes the functionality for uploading and processing images related to hotels.
It defines the router for handling image uploads and triggering background processing tasks for the images.

Modules:
    - router: Defines the FastAPI router for uploading hotel images and processing them asynchronously.
"""

from .images_router import router

__all__ = ["router"]
