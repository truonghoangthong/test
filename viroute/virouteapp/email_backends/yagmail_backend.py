import yagmail
from django.core.mail.backends.base import BaseEmailBackend

import yagmail
from django.conf import settings

# Tạo một instance của Yagmail SMTP một lần duy nhất
yag = yagmail.SMTP(user='lelouchzero093@gmail.com', password='yoag nlig okku bryv')

def send_reset_email(email, reset_link):
    try:
        yag.send(
            to=email,
            subject="Reset Password",
            contents=f"Click the link to reset your password: {reset_link}"
        )
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")