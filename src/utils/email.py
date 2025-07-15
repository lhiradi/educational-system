from flask_mail import Message
from src.extensions import mail
from flask import current_app

def send_login_otp_email(user, otp):
    msg = Message(
        'Your Login OTP',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email]
    )
    msg.body = f"""
Your One-Time Password (OTP) is: {otp}

This OTP will expire in 10 minutes.

If you did not request this, let the admin know.
"""
    mail.send(msg)