from fastapi_mail import MessageSchema,FastMail
import asyncio

from core.email_connection import config
from core.celery import celery_app

@celery_app.task
def send_welcome_message(email: str,username: str):
    message = MessageSchema(
        subject = "Welcome message",
        recipients=[email],
        body = f"heyyy!!! {username} welcome to connect App , hope u find it entertining",
        subtype="plain"
    )
    fm = FastMail(config)
    asyncio.run(fm.send_message(message))