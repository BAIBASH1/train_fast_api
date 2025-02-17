"""
Frontend Routes for Rendering HTML Pages.

This module defines the FastAPI router for rendering HTML pages for the frontend. It includes
a route for rendering the hotels page, which fetches hotel data
and renders it using a Jinja2 template.

Endpoints:
    - get_hotels_page: Renders a page displaying hotels available
     in a specified location and date range.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.hotel_router import get_hotels_by_location_and_time

router = APIRouter(prefix="/pages", tags=["Фронтент"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(
    request: Request, hotels=Depends(get_hotels_by_location_and_time)
):
    """
    Renders the hotels page displaying available hotels based on the location and date range.

    This endpoint fetches the list of hotels from the backend (using the
    `get_hotels_by_location_and_time` function) and renders it on the `hotels.html`
     page using Jinja2 templates.

    Args:
        request (Request): The incoming HTTP request required for rendering the template.
        hotels: A list of hotels retrieved based on the location and date range.

    Returns:
        TemplateResponse: The rendered HTML page with the list of hotels.
    """
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels},
    )
