import app.services.auth_service as auth
import app.core.database as database
import asyncio
import re

_EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

def _valid_email(email: str) -> bool:
    return bool(_EMAIL_RE.match(email))

from app.core.logger import LOG
from app.models.schemas import *
from app.core.constants import *
from app.services.airtable_service import *
from app.services.sync_service import sync_service

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware


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

# Trust X-Forwarded-For from nginx proxy so rate limiting uses real client IPs
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGIN,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

@app.post("/api/authenticated")
@limiter.limit("30/minute")
async def authenticate_user(request: Request, status: dict = Depends(auth.authenticated_user)) -> JSONResponse:
    return status

@app.post("/api/refresh_token")
@limiter.limit("20/minute")
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
            samesite="strict",
            secure=IS_PRODUCTION
        )

        response.set_cookie(
            key="refresh_token",
            value=payload.get('refresh_token'),
            httponly=True,
            max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
            samesite="strict",
            secure=IS_PRODUCTION
        )

        return response

    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/logout")
@limiter.limit("10/minute")
async def logout(request: Request, response: Response) -> JSONResponse:
    # Create the response object
    response = JSONResponse(
        content={"message": "Logged out successfully."},
        status_code=200
    )

    # Delete cookies
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="strict",
        secure=IS_PRODUCTION
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        samesite="strict",
        secure=IS_PRODUCTION
    )
    response.delete_cookie(
        key="user_id",
        path="/",
        samesite="strict",
        secure=IS_PRODUCTION
    )

    return response

@app.post("/api/login")
@limiter.limit("5/minute")
async def login_user_with_credentials(request: Request, userObject: LoginDetails, response: Response) -> JSONResponse:
    try:
        validation_result = auth.validate(userObject)
        is_valid_user, user_id, is_admin = validation_result[0], validation_result[1], validation_result[2] if len(validation_result) > 2 else False

        if is_valid_user:
            LOG.info(f"AUDIT login_success user_id={user_id} ip={request.client.host}")
            user_data = {"sub": user_id, "is_admin": is_admin}
            access_token = auth.create_token(user_data, "access")
            refresh_token = auth.create_token(user_data, "refresh")

            refresh_token_resp = database.store_user_refresh_token(user_id, refresh_token)
            if refresh_token_resp != 200:
                return JSONResponse(status_code=500, content={"message": "Internal Server Error!"})

            response = JSONResponse(
                status_code = 200,
                content = {
                    "message": "Verified!",
                    "admin_login": is_admin
                }
            )

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=ACCESS_TOKEN_EXPIRATION_MINUTES * 60,
                samesite="strict",
                secure=IS_PRODUCTION
            )

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
                samesite="strict",
                secure=IS_PRODUCTION
            )

            response.set_cookie(
                key="user_id",
                value=user_id,
                httponly=True,
                max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
                samesite="strict",
                secure=IS_PRODUCTION
            )

            response.set_cookie(
                key="is_admin",
                value="true" if is_admin else "false",
                httponly=True,
                max_age=REFRESH_TOKEN_EXPIRATION_DAYS * 24 * 60 * 60,
                samesite="strict",
                secure=IS_PRODUCTION
            )

            return response
        else:
            LOG.warning(f"AUDIT login_failure username={userObject.user} ip={request.client.host}")
            return JSONResponse(status_code=404, content={"message": "Could not verify user/password combination!"})

    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post('/api/create_user')
@limiter.limit("3/minute")
async def create_user_with_credentials(request: Request, user: User) -> JSONResponse:
    try:
        if len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        if not _valid_email(user.email_address):
            raise HTTPException(status_code=400, detail="Please enter a valid email address")
        if database.username_or_email_exists(user.user_name, user.email_address):
            raise HTTPException(status_code=409, detail="Username or email already in use")
        response = database.create_user(user, auth.hash_pwd(user.password))
        if response == 200:
            return JSONResponse(status_code=200, content={"message": "User created successfully!"})
    except HTTPException:
        raise
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.post("/api/manual_sync")
@limiter.limit("3/minute")
async def manual_sync(request: Request, status: dict = Depends(auth.authenticated_user)):
    """Trigger immediate sync from frontend"""
    try:
        user_id = status.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found")
            
        result = await sync_service.sync_all_data(user_id)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/sync_status")
@limiter.limit("30/minute")
async def get_sync_status(request: Request, status: dict = Depends(auth.authenticated_user)):
    """Return sync status and last sync time"""
    try:
        if sync_service.last_sync is not None:
            last_sync_str = sync_service.last_sync.isoformat() + 'Z'
        else:
            # Fall back to sync_log DB table so the value survives restarts
            conn, cur = database.get_db_connection()
            last_sync_str = None
            if cur is not None:
                try:
                    cur.execute(
                        "SELECT completed_at FROM sync_log WHERE status = 'completed' "
                        "ORDER BY completed_at DESC LIMIT 1"
                    )
                    row = cur.fetchone()
                    if row and row[0]:
                        last_sync_str = row[0].isoformat() + 'Z'
                finally:
                    cur.close()
                    conn.close()

        return JSONResponse(status_code=200, content={
            "last_sync": last_sync_str,
            "is_running": sync_service.is_running
        })
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/get_local_accounts")
@limiter.limit("30/minute")
async def get_local_accounts(request: Request, status: dict = Depends(auth.authenticated_user)):
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
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/get_local_transactions")
@limiter.limit("30/minute")
async def get_local_transactions(request: Request, status: dict = Depends(auth.authenticated_user)):
    """Get transactions from local database for authenticated user"""
    try:
        user_id = status.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found")
            
        transactions = database.get_all_transactions(user_id)
        if isinstance(transactions, dict) and "error" in transactions:
            raise HTTPException(status_code=500, detail=transactions["error"])
        return transactions
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/get_current_user")
@limiter.limit("30/minute")
async def get_current_user(request: Request, status: dict = Depends(auth.authenticated_user)):
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
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/update_password")
@limiter.limit("5/minute")
async def update_password(
    request: Request,
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
        if len(new_password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        
        # Verify current password
        user = database.get_user_by_id(user_id, include_password=True)
        if not user or not auth.verify_pwd(current_password, user.get("password", "")):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        # Hash new password and update
        hashed_password = auth.hash_pwd(new_password)
        result = database.update_user_password(user_id, hashed_password)
        LOG.info(f"AUDIT password_changed user_id={user_id} ip={request.client.host}")
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {"message": "Password updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/update_email")
@limiter.limit("5/minute")
async def update_email(
    request: Request,
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
        
        if not _valid_email(new_email):
            raise HTTPException(status_code=400, detail="Please enter a valid email address")
        
        # Update email
        result = database.update_user_email(user_id, new_email)
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {"message": "Email updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin-only endpoints
@app.get("/api/admin/users")
@limiter.limit("10/minute")
async def get_all_users(request: Request, status: dict = Depends(auth.admin_required)):
    """Get all users (admin only)"""
    try:
        users = database.get_all_users_admin()
        return JSONResponse(status_code=200, content=users)
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/admin/reset_password")
@limiter.limit("5/minute")
async def admin_reset_password(
    request: Request,
    reset_data: dict,
    status: dict = Depends(auth.admin_required)
):
    """Reset any user's password (admin only)"""
    try:
        target_user = reset_data.get("username")
        new_password = reset_data.get("new_password")
        
        if not target_user or not new_password:
            raise HTTPException(status_code=400, detail="Username and new password are required")
        
        # Hash the new password
        hashed_password = auth.hash_pwd(new_password)
        
        # Update password in database
        success = database.admin_update_user_password(target_user, hashed_password)
        if success:
            LOG.info(f"AUDIT admin_reset_password admin_id={status.get('user_id')} target={target_user} ip={request.client.host}")
            return JSONResponse(status_code=200, content={
                "message": f"Password reset successfully for user: {target_user}"
            })
        else:
            raise HTTPException(status_code=404, detail="User not found")
            
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/admin/reset_demo_account")
@limiter.limit("2/minute")
async def reset_demo_account(request: Request, status: dict = Depends(auth.admin_required)):
    """Reset demo account password and regenerate data (admin only)"""
    try:
        # Reset demo password
        demo_password = "demo123"
        hashed_password = auth.hash_pwd(demo_password)
        
        password_reset = database.admin_update_user_password("demo", hashed_password)
        if not password_reset:
            raise HTTPException(status_code=404, detail="Demo user not found")
        
        # Regenerate demo data
        data_reset = database.reset_demo_data()
        LOG.info(f"AUDIT admin_reset_demo admin_id={status.get('user_id')} ip={request.client.host}")

        return JSONResponse(status_code=200, content={
            "message": "Demo account reset successfully",
            "data_regenerated": data_reset
        })
        
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/admin/user_stats")
@limiter.limit("10/minute")
async def get_user_stats(request: Request, status: dict = Depends(auth.admin_required)):
    """Get user statistics (admin only)"""
    try:
        stats = database.get_user_statistics()
        return JSONResponse(status_code=200, content=stats)
    except Exception as e:
        LOG.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

# python -m uvicorn app.main:app --reload