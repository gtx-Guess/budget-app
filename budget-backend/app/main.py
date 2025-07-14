import app.services.auth_service as auth
import app.core.database as database
import asyncio

from app.core.logger import LOG
from app.models.schemas import *
from app.core.constants import *
from app.services.airtable_service import *
from app.services.sync_service import sync_service

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    LOG.info("Starting background sync service...")
    sync_task = asyncio.create_task(sync_service.start_background_sync())
    
    yield
    
    LOG.info("Shutting down background sync service...")
    sync_service.stop()
    sync_task.cancel()
    try:
        await sync_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/authenticated")
async def authenticate_user(status: dict = Depends(auth.authenticated_user)) -> JSONResponse:
    return status

@app.post("/api/refresh_token")
async def generate_new_tokens_using_refresh_token(request: Request, response: Response) -> JSONResponse:
    old_refresh_token = request.cookies.get("refresh_token")
    user_id = request.cookies.get("user_id")

    if not old_refresh_token:
        raise HTTPException(status_code=401, detail="Refresh Token Not Found")
    
    try:
        payload = auth.verify_refresh_token(old_refresh_token, user_id)
        if payload == 401:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
        response = JSONResponse(
            status_code = 200,
            content = {"message": "Tokens refreshed!"}
        )
        
        response.set_cookie(
            key="access_token",
            value=payload.get('access_token'),
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRATION_MINUTES * 60,
            samesite="none",
            secure=True
        )

        response.set_cookie(
            key="refresh_token",
            value=payload.get('refresh_token'),
            httponly=True,
            max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
            samesite="none",
            secure=True
        )

        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/logout")
async def logout(response: Response) -> JSONResponse:
    # Create the response object
    response = JSONResponse(
        content={"message": "Logged out successfully."},
        status_code=200
    )
    
    # Delete cookies
    response.delete_cookie(
        key="access_token",
        path="/",  # Ensure this matches the path used to set the cookie
        samesite="none",
        secure=True
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        samesite="none",
        secure=True
    )
    response.delete_cookie(
        key="user_id",
        path="/",
        samesite="none",
        secure=True
    )
    
    return response

@app.post("/api/login")
async def login_user_with_credentials(userObject: LoginDetails, response: Response) -> JSONResponse:
    try:
        is_valid_user, user_id = auth.validate(userObject)
        if is_valid_user:
            user_data = {"sub": user_id}
            access_token = auth.create_token(user_data, "access")
            refresh_token = auth.create_token(user_data, "refresh")

            refresh_token_resp = database.store_user_refresh_token(user_id, refresh_token)
            if refresh_token_resp != 200:
                return JSONResponse(status_code=500, content={"message": "Internal Server Error!"})
            
            response = JSONResponse(
                status_code = 200,
                content = {"message": "Verified!"}
            )
            
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=ACCESS_TOKEN_EXPIRATION_MINUTES * 60,
                samesite="none",
                secure=True
            )

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
                samesite="none",
                secure=True
            )

            response.set_cookie(
                key="user_id",
                value=user_id,
                httponly=True,
                max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
                samesite="none",
                secure=True
            )

            return response
        else:
            return JSONResponse(status_code=404, content={"message": "Could not verify user/password combination!"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/create_user')
async def create_user_with_credentials(user: User) -> JSONResponse:
    try:
        response = database.create_user(user, auth.hash_pwd(user.password))
        if response == 200:
            return JSONResponse(status_code=200, content={"message": "User created successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/manual_sync")
async def manual_sync(status: dict = Depends(auth.authenticated_user)):
    """Trigger immediate sync from frontend"""
    try:
        result = await sync_service.sync_all_data()
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sync_status")
async def get_sync_status(status: dict = Depends(auth.authenticated_user)):
    """Return sync status and last sync time"""
    try:
        return JSONResponse(status_code=200, content={
            "last_sync": sync_service.last_sync.isoformat() if sync_service.last_sync else None,
            "is_running": sync_service.is_running
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get_local_accounts")
async def get_local_accounts(status: dict = Depends(auth.authenticated_user)):
    """Get accounts from local database for authenticated user"""
    try:
        user_id = status.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found")
            
        accounts = database.get_all_accounts(user_id)
        if isinstance(accounts, dict) and "error" in accounts:
            raise HTTPException(status_code=500, detail=accounts["error"])
        return accounts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get_local_transactions")
async def get_local_transactions(status: dict = Depends(auth.authenticated_user)):
    """Get transactions from local database"""
    try:
        transactions = database.get_all_transactions()
        if isinstance(transactions, dict) and "error" in transactions:
            raise HTTPException(status_code=500, detail=transactions["error"])
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get_current_user")
async def get_current_user(status: dict = Depends(auth.authenticated_user)):
    """Get current authenticated user's details"""
    try:
        user_id = status.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found")
        
        user = database.get_user_by_id(user_id)
        if isinstance(user, dict) and "error" in user:
            raise HTTPException(status_code=500, detail=user["error"])
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/update_password")
async def update_password(
    password_data: dict,
    status: dict = Depends(auth.authenticated_user)
):
    """Update user's password"""
    try:
        user_id = status.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found")
        
        current_password = password_data.get("current_password")
        new_password = password_data.get("new_password")
        
        if not current_password or not new_password:
            raise HTTPException(status_code=400, detail="Both current and new passwords are required")
        
        # Verify current password
        user = database.get_user_by_id(user_id, include_password=True)
        if not user or not auth.verify_pwd(current_password, user.get("password", "")):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        # Hash new password and update
        hashed_password = auth.hash_pwd(new_password)
        result = database.update_user_password(user_id, hashed_password)
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {"message": "Password updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/update_email")
async def update_email(
    email_data: dict,
    status: dict = Depends(auth.authenticated_user)
):
    """Update user's email address"""
    try:
        user_id = status.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found")
        
        new_email = email_data.get("new_email")
        
        if not new_email:
            raise HTTPException(status_code=400, detail="New email address is required")
        
        # Basic email validation
        if "@" not in new_email or "." not in new_email:
            raise HTTPException(status_code=400, detail="Please enter a valid email address")
        
        # Update email
        result = database.update_user_email(user_id, new_email)
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {"message": "Email updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# python -m uvicorn app.main:app --reload