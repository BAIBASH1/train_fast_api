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
