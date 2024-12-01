import yagmail

def send_reset_email(email, reset_link):
    try:
        yag = yagmail.SMTP(user='lelouchzero093@gmail.com', password='yoag nlig okku bryv')
        yag.send(
            to=email,
            subject="Reset Password",
            contents=f"Click the link to reset your password: {reset_link}"
        )
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
