import jwt
import hashlib
import datetime
import re
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import random

def encrypt_password(raw_password):
    salt = hashlib.sha256()
    salt.update(raw_password.encode('utf-8'))
    salt_bytes = salt.digest()

    hashed_password = hashlib.sha256()
    hashed_password.update(raw_password.encode('utf-8') + salt_bytes)
    hashed_password_bytes = hashed_password.digest()

    return hashed_password_bytes.hex()

def student_encode_token(payload: dict):
    payload["exp"] = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(days=7)
    token = jwt.encode(payload, "student_key", algorithm="HS256")
    return token

def faculty_encode_token(payload: dict):
    payload["exp"] = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(days=7)
    token = jwt.encode(payload, "faculty_key", algorithm="HS256")
    return token

def hoc_encode_token(payload: dict):
    payload["exp"] = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(days=7)
    token = jwt.encode(payload, "hoc_key", algorithm="HS256")
    return token
    
def validate_batch(batch_string):
    pattern = r'^BATCH(\d{4})-(\d{4})$'
    match = re.match(pattern, batch_string)
    if not match:
        return False
    start_year = int(match.group(1))
    end_year = int(match.group(2))
    if end_year - start_year == 4:
        return True
    else:
        return False
    
def generate_otp():
    return random.randint(100000, 999999)
    
def send_email(to_email, email_subject, email_body):
    sender_email = "gibson.25cs@licet.ac.in"
    sender_password = "GIBson6103@"

    if not sender_email or not sender_password:
        raise ValueError("Sender email or password not set in environment variables")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with the SMTP server. Check your email and password.")
        raise
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {str(e)}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise