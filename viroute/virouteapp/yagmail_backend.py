import yagmail

def send_reset_email(email, reset_link):
    try:
        # Kết nối với SMTP server
        yag = yagmail.SMTP(user='lelouchzero093@gmail.com', password='yoag nlig okku bryv')

        # Gửi email
        yag.send(
            to=email,
            subject="Reset Password",
            contents=f"Click the link to reset your password: {reset_link}"
        )
        print(f"Email sent successfully to {email}")
    except yagmail.YagConnectionError as e:
        # Kiểm tra lỗi kết nối
        raise Exception(f"Connection error while sending email: {str(e)}")
    except yagmail.YagInvalidEmailAddress as e:
        # Kiểm tra email không hợp lệ
        raise Exception(f"Invalid email address: {str(e)}")
    except Exception as e:
        # Bắt lỗi chung
        raise Exception(f"Failed to send email: {str(e)}")
