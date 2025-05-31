import auth
import database
import requests
from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from constants import *
from fastapi.responses import JSONResponse
from airtable_utils import *

if STAGE == "PROD":
    plaid_secret = PLAID_PROD_SECRET
    plaid_url = PLAID_PROD_URL
else:
    plaid_secret = PLAID_SANDBOX_SECRET
    plaid_url = PLAID_SANDBOX_URL

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],  # Update with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/authenticated")
async def authenticate_user(status: dict = Depends(auth.authenticated_user)) -> JSONResponse:
    return status

@app.post("/refresh_token")
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

@app.post("/logout")
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


@app.post("/login")
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

@app.post('/create_user')
async def create_user_with_credentials(user: User) -> JSONResponse:
    try:
        response = database.create_user(user, auth.hash_pwd(user.password))
        if response == 200:
            return JSONResponse(status_code=200, content={"message": "User created successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create_link_token")
async def create_link_token(link_request: LinkTokenRequest) -> JSONResponse:
    try:
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "client_id": PLAID_CLIENT_ID,
            "secret": plaid_secret,
            **link_request.dict(),
        }
        response = requests.post(f"{plaid_url}/link/token/create", json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/exchange_public_token")
async def exchange_public_token(request: PublicTokenRequest) -> JSONResponse:
    try:
        response = requests.post(f"{plaid_url}/item/public_token/exchange", json={
            "client_id": PLAID_CLIENT_ID,
            "secret": plaid_secret,
            "public_token": request.public_token,
        })

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        data = response.json()
        return {"access_token": data["access_token"], "item_id": data["item_id"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/get_transactions")
async def get_transactions(request: TransactionsRequest) -> JSONResponse:
    try:
        response = requests.post(f"{plaid_url}/transactions/get", json={
            "client_id": PLAID_CLIENT_ID,
            "secret": plaid_secret,
            "access_token": request.access_token,
            "start_date": request.start_date,
            "end_date": request.end_date,
        })

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return response.json()  # Return the transactions data directly

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/api/get_airtable_data/{request_type}")
async def get_airtable_data(request_type: str) -> JSONResponse:
    try:
        response = make_request_to_airtable(request_type)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# python3 -m uvicorn budget_backend:app --reload