import app.core.database as database
import jwt

from app.core.logger import LOG
from app.core.constants import ACCESS_TOKEN_EXPIRATION_MINUTES, REFRESH_TOKEN_EXPIRATION_DAYS, SECRET_KEY, ALGORITHM

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(data: dict, type: str) -> str:
    try:
        to_encode = data.copy()

        if type == "access":
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
        if type == "refresh":
            expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)

        to_encode.update({"exp": expire})        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    except Exception as e:
        LOG.error("Error creating access token:", str(e))
        raise HTTPException(status_code=500, detail="Failed to generate access token")
    

def verify_refresh_token(old_token: str, user_id: str) -> str:
    try:
        storedToken = database.get_refresh_token(user_id)
        if old_token != storedToken:
            return 401

        user_data = {"sub": user_id}
        new_access_token = create_token(user_data, "access")
        new_refresh_token = create_token(user_data, "refresh")

        database.store_user_refresh_token(user_id, new_refresh_token)
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    
    except Exception as e:
        LOG.error(e)

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticated_user(request: Request) -> dict:
    access_token = request.cookies.get("access_token")
    user_id = request.cookies.get("user_id")

    if not access_token:
        raise HTTPException(status_code=401, detail="Couldn't get access_token from cookies")

    try:
        # Verify the access token
        payload = verify_access_token(access_token)

        # Check if the user ID in the token matches the user ID from the cookie
        if int(payload.get("sub")) == int(user_id):
            return {"status": 200, "detail": "User verified", "user_id": user_id}
        else:
            raise HTTPException(status_code=401, detail="User IDs didn't match")

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def hash_pwd(password: str) -> str:
    return pwd_context.hash(password)

def verify_pwd(plain_pwd: str, hashed_pwd) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

def validate(userObject: object) -> list:
    try:
        respUserObject = database.get_pwd_hash_from_db_by_user(userObject)
        if respUserObject and verify_pwd(userObject.password, respUserObject.get('password')):
            return [True, respUserObject.get('id')]
        else:
            return [False, '']
    except Exception as e:
        LOG.error(e)
