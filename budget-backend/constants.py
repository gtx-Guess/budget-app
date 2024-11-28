import os
from dotenv import load_dotenv
load_dotenv()

PLAID_URL = os.getenv("PLAID_SANDBOX_URL")
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN")

DB_BASE_URL = os.getenv("SUPA_BASE_URL")
SUPA_ACCESS_TOKEN = os.getenv("SUPA_ACCESS_TOKEN")

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_TOKEN_EXPIRATION_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRATION_DAYS"))
ACCESS_TOKEN_EXPIRATION_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRATION_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")

IS_LOCAL = os.getenv("IS_LOCAL").upper() == "TRUE"
LOCAL_DB_HOST = os.getenv("LOCAL_DB_HOST") 
LOCAL_DB_USER = os.getenv("LOCAL_DB_USER")
LOCAL_DB_PASS = os.getenv("LOCAL_DB_PASS") 
LOCAL_DB = os.getenv("LOCAL_DB") 