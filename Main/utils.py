from django.shortcuts import redirect
from django.contrib import messages

import smtplib
from email.message import EmailMessage
from .config import EMAIL_ADDRESS, PASSWORD
import secrets


code = secrets.token_hex(3)

def send_confirm_email(username, email):
    message = EmailMessage()
    message["Subject"] = f"Confirm email - {username}"
    message["From"] = EMAIL_ADDRESS
    message["To"] = email
    message.set_content(f'Please type this code to confirm your account: {code}')

    with smtplib.SMTP_SSL('smtp.gmail.com', '465') as smtp:
        smtp.login(EMAIL_ADDRESS, PASSWORD)
        smtp.send_message(message)

def confirm_email_address(code_field):
    if code_field == code:
        messages.success('Your email address has been confirmed.')
        return redirect('login')
    else:
        messages.error('You have entered an invalid code. Try again!')