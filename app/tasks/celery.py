"""
Celery Configuration and Initialization.

This module configures and initializes the Celery application. The Celery app is used to handle
asynchronous tasks in the project, with Redis as the message broker.

Celery is set up based on the application environment, either using the test or production Redis
instance, and is used for background tasks such as image processing and sending emails.

Attributes:
    celery (Celery): The Celery application instance.
"""

from celery import Celery

from config import settings

if settings.MODE == "TEST":
    CELERY_BROKER_URL = f"redis://{settings.TEST_REDIS_HOST}:{settings.REDIS_PORT}"
else:
    CELERY_BROKER_URL = f"redis://{settings.REDIS_HOST}:{settings.TEST_REDIS_PORT}"

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    include=["app.tasks.tasks"],
)
