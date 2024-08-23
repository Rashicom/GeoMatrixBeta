from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from geomatrix.config import get_settings
from typing import List
settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_template_mail(targets:List, data:dict, template:str=None):
    """
    Accept : target[] emails and : template optional
    """
    try:
        mailer = FastMail(conf)
        message = MessageSchema(
            subject="GeoMatrix - New User Registration",
            recipients=targets,
            body="html",
            subtype="MessageType.html",
        )
        await mailer.send_message(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True


async def send_mail(targets:List, template:str=None):
    """
    Accept : target[] emails and : template optional
    """
    try:
        mailer = FastMail(conf)
        message = MessageSchema(
            subject="GeoMatrix - New User Registration",
            recipients=targets,
            body="Test message",
            subtype="plain",
        )
        await mailer.send_message(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True