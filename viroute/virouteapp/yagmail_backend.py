from django.core.mail import send_mail
from django.conf import settings
import logging

# Tạo một logger để ghi lại thông tin
logger = logging.getLogger(__name__)

def send_reset_email(email, reset_link):
    subject = "Password Reset"
    message = f"Click the link to reset your password: {reset_link}"
    from_email = settings.EMAIL_HOST_USER
    
    try:
        send_mail(subject, message, from_email, [email])
        logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")

