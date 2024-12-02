from django.core.mail import send_mail

def send_reset_email(email, reset_link):
    try:
        subject = "Password Reset"
        message = f"Click the link to reset your password: {reset_link}"
        from_email = 'lelouchzero093@gmail.com'
        
        send_mail(
            subject,
            message,
            from_email,
            [email],  # Người nhận
            fail_silently=False,  # Bật chế độ báo lỗi nếu có
        )
    except Exception as e:
        print("Error sending email:", e)
