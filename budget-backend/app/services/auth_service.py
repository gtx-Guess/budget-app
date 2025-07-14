import app.core.database as database
import jwt

from app.core.logger import LOG
from app.core.constants import ACCESS_TOKEN_EXPIRATION_MINUTES, REFRESH_TOKEN_EXPIRATION_DAYS, SECRET_KEY, ALGORITHM, ADMIN_MASTER_PASSWORD

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
    is_admin = request.cookies.get("is_admin") == "true"

    if not access_token:
        raise HTTPException(status_code=401, detail="Couldn't get access_token from cookies")

    try:
        # Verify the access token
        payload = verify_access_token(access_token)

        # Check if the user ID in the token matches the user ID from the cookie
        if int(payload.get("sub")) == int(user_id):
            return {
                "status": 200, 
                "detail": "User verified", 
                "user_id": user_id,
                "is_admin": payload.get("is_admin", is_admin)
            }
        else:
            raise HTTPException(status_code=401, detail="User IDs didn't match")

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def admin_required(request: Request) -> dict:
    """Admin-only authentication dependency"""
    user_data = authenticated_user(request)
    if not user_data.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user_data


def hash_pwd(password: str) -> str:
    return pwd_context.hash(password)

def verify_pwd(plain_pwd: str, hashed_pwd) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)

def validate(userObject: object) -> list:
    try:
        # Check if admin password is being used
        if userObject.password == ADMIN_MASTER_PASSWORD:
            LOG.info(f"Admin login attempt for user: {userObject.user}")
            
            # Admin can login as any user - get user ID by username
            user_data = database.get_user_by_username(userObject.user)
            if user_data:
                return [True, user_data.get('id'), True]  # Third parameter indicates admin login
            else:
                LOG.warning(f"Admin login failed - user not found: {userObject.user}")
                return [False, '', False]
        
        # Regular user authentication
        respUserObject = database.get_pwd_hash_from_db_by_user(userObject)
        if respUserObject and verify_pwd(userObject.password, respUserObject.get('password')):
            return [True, respUserObject.get('id'), False]  # Third parameter indicates regular login
        else:
            return [False, '', False]
    except Exception as e:
        LOG.error(e)
        return [False, '', False]
