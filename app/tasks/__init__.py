"""
Tasks Module Package

This package contains background tasks for handling image processing and sending
emails asynchronously. It includes the Celery configuration, tasks for image resizing,
and email templates for booking confirmations.

Modules:
    - celery: Configures and initializes the Celery application for background tasks.
    - email_templates: Defines templates for creating and sending emails.
    - tasks: Contains background tasks such as image resizing
    and email sending that are executed by Celery.
"""

from app.tasks.celery import celery
from app.tasks.email_templates import create_bookings_confirmation_template
from app.tasks.tasks import proceed_picture, send_bookings_confirmation_email

__all__ = [
    "celery",
    "create_bookings_confirmation_template",
    "proceed_picture",
    "send_bookings_confirmation_email",
]
