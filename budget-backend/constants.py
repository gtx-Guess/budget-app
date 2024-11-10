import os
from dotenv import load_dotenv
load_dotenv()

PLAID_URL = os.getenv("PLAID_SANDBOX_URL")
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN")