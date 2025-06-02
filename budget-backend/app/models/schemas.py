from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum

class VendorCategories(Enum):
    GROCERIES = "Groceries"
    RESTAURANTS = "Restaurants"
    SHOPPING = "Shopping"
    UTILITIES = "Utilities"
    DIGITAL_PURCHASE = "Digital Purchase"
    SUBSCRIPTIONS = "Subscriptions"
    CREDIT_CARDS = "Credit Cards"
    AUTO = "Auto"
    MISC = "Misc"
    BALANCE_TRANSFERS = "Balance Transfers"
    
    @classmethod
    def get_all(cls):
        """Get all the categories from the class in a list"""
        return [category.value for category in cls]

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