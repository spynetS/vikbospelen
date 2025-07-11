#!/usr/bin/env python3

from django.contrib.auth.models import User  # <- Use default User model
from django.core.mail import EmailMessage
from mail.models import Mail
from vikbo import settings


def sendmail(subject, body, name, email, to, group=None, content_subtype="text/plain"):
    # Get all active staff users
    reply = [email]
    to = [to]


    mail_model = Mail(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
        reply_to=reply
    )
    mail_model.save()

    mail = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to,
        reply_to=reply
    )

    # Logging the email
    print("_____SENDEMAIL_____")
    print("____CONTENT____")
    print(f"subject={subject}")
    print(f"to={to}")
    print(f"from={settings.EMAIL_HOST_USER}")
    print(f"body={body}")

    mail.content_subtype = content_subtype

    try:
        value = mail.send()
        return value
    except Exception as e:
        print("not sent")
        mail_model.error = str(e)
        mail_model.save()
        return mail.send()
