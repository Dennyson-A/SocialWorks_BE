import jwt
import hashlib
import datetime
import re

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
    
    
def ob_encode_token(payload: dict):
    payload["exp"] = datetime.datetime.now(
        tz=datetime.timezone.utc
    ) + datetime.timedelta(days=7)
    token = jwt.encode(payload, "ob_key", algorithm="HS256")
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
    