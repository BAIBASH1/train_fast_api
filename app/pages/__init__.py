"""
Frontend Routes Package

This package contains routes for rendering frontend HTML pages in the application.
It includes the routes for serving hotel-related pages, utilizing Jinja2 templates for rendering
dynamic content from the backend data.

Modules:
    - router: Defines the frontend routes for serving HTML pages, such as the hotels page.
"""

from .pages_router import router

__all__ = ["router"]
