from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from geomatrix.config import get_settings
from typing import List
from geomatrix.common.schemas import HtmlEmailSchema, TextEmailSchema
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
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = "src/geomatrix/templates",
)

async def send_template_mail(email_schema:HtmlEmailSchema):
    """
    Accept : target[] emails and : template optional
    """
    try:
        mailer = FastMail(conf)
        message = MessageSchema(
            subject=email_schema.subject,
            recipients=email_schema.recipients,
            template_body=email_schema.template_body,
            subtype="html",
        )
        await mailer.send_message(message, template_name="varify_account.html")
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True


async def send_mail(email_schema:TextEmailSchema):
    """
    Accept : target[] emails and : template optional
    """
    try:
        mailer = FastMail(conf)
        message = MessageSchema(
            subject=email_schema.subject,
            recipients=email_schema.recipients,
            body=email_schema.body,
            subtype="plain",
        )
        await mailer.send_message(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True