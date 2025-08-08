from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf= ConnectionConfig(

    MAIL_USERNAME = "sebinsaji10@gmail.com",
    MAIL_PASSWORD = "tbzdedrhmwmbzsgq",
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS=True,       # this for TLS
    MAIL_SSL_TLS=False,       # Don't use SSL if you're using STARTTLS
    MAIL_FROM = "sebinsaji10@gmail.com"    ,
    USE_CREDENTIALS = True ,
    MAIL_PORT=587
    
    )

async def send_email_apis(to_mail:EmailStr,username=str):

    mail_id=to_mail
    subject="Booking Confirmation"

    body = f"Dear {username} , Your booking is confirmed"

    message= MessageSchema(

        subject=subject,
        body=body,
        recipients=[mail_id],
        subtype="plain"
    )

    fm=FastMail(conf)

    await fm.send_message(message)
