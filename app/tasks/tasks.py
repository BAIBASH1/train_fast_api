import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.tasks.celery import celery
from app.tasks.email_templates import create_bookings_confirmation_template
from config import settings


@celery.task
def proceed_picture(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")
    im_resized_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")


@celery.task
def send_bookings_confirmation_email(
    bookings: dict,
    email_to: EmailStr,
):
    msg_content = create_bookings_confirmation_template(
        bookings=bookings,
        email_to=email_to,
    )

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
