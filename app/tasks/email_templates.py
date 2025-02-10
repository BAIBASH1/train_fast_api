from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def create_bookings_confirmation_template(bookings: dict, email_to: EmailStr):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {bookings["date_from"]} до {bookings["date_to"]}
        """,
        subtype="html",
    )
    return email
