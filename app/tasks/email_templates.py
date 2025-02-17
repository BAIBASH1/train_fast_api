"""
Email Template Generator.

This module contains functions for creating email templates. Currently, it defines a template
for confirming bookings. The templates use HTML formatting for the email body and are configured
to be sent via the email server specified in the application settings.

Functions:
    - create_bookings_confirmation_template: Creates an HTML email template for
     booking confirmation.
"""

from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def create_bookings_confirmation_template(bookings: dict, email_to: EmailStr):
    """
    Creates a booking confirmation email template.

    This function generates an email template for confirming a booking. The email includes the
    booking details, such as the booking period, and is formatted in HTML.

    Args:
        bookings (dict): The booking data that needs to be included in the email.
        email_to (EmailStr): The email address of the recipient.

    Returns:
        EmailMessage: The constructed email message object with the confirmation details.
    """
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
