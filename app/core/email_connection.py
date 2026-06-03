from fastapi_mail import ConnectionConfig

config = ConnectionConfig(
    MAIL_USERNAME="hitheshrhithu41@gmail.com",
    MAIL_PASSWORD="tszxtvpkqascxege",
    MAIL_FROM="hitheshrhithu41@gmail",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)