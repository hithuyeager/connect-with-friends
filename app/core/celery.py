from celery import Celery
from config import settings

celery_app = Celery(
    "worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["tasks.email_tasks"]
)