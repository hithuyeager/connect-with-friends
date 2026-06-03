from fastapi_mail import ConnectionConfig
from config import settings

config = ConnectionConfig(
    MAIL_USERNAME=settings.my_email,
    MAIL_PASSWORD=settings.my_email_password,
    MAIL_FROM=settings.my_email,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)