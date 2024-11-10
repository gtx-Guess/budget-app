from fastapi import FastAPI, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from constants import *
from fastapi.responses import JSONResponse

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],  # Update with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def login_user_with_credentials(login: LoginDetails):
    try:
        # response = generate_session_token()
        return JSONResponse(status_code=404, content={"message": "Not Verified!"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create_link_token")
async def create_link_token(link_request: LinkTokenRequest):
    try:
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "client_id": PLAID_CLIENT_ID,
            "secret": PLAID_SECRET,
            **link_request.dict(),
        }
        response = requests.post(f"{PLAID_URL}/link/token/create", json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/exchange_public_token")
async def exchange_public_token(request: PublicTokenRequest):
    try:
        response = requests.post(f"{PLAID_URL}/item/public_token/exchange", json={
            "client_id": PLAID_CLIENT_ID,
            "secret": PLAID_SECRET,
            "public_token": request.public_token,
        })

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        data = response.json()
        return {"access_token": data["access_token"], "item_id": data["item_id"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/get_transactions")
async def get_transactions(request: TransactionsRequest):
    try:
        response = requests.post(f"{PLAID_URL}/transactions/get", json={
            "client_id": PLAID_CLIENT_ID,
            "secret": PLAID_SECRET,
            "access_token": request.access_token,
            "start_date": request.start_date,
            "end_date": request.end_date,
        })

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return response.json()  # Return the transactions data directly

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# python3 -m uvicorn budget_backend:app --reload