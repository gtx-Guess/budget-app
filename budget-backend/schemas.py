from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
class PublicTokenRequest(BaseModel):
    public_token: str

class LinkTokenRequest(BaseModel):
    client_name: str
    language: str
    country_codes: list
    user: dict
    products: list

class TransactionsRequest(BaseModel):
    access_token: str
    start_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date: Optional[str] = datetime.now().strftime('%Y-%m-%d')

class LoginDetails(BaseModel):
    user: str
    password: str

class User(BaseModel):
    user_name: str
    password: str
    email_address: str