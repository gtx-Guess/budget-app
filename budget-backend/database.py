import requests
import json
from constants import DB_BASE_URL, SUPA_ACCESS_TOKEN
from schemas import User

HEADERS = {
    "apikey": SUPA_ACCESS_TOKEN,
    "Authorization": f"Bearer {SUPA_ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_refresh_token(user_id: str) -> str:
    url = f"{DB_BASE_URL}?id=eq.{user_id}&select=refresh_token"
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code in [200, 201]:
            return resp.json()
        else:
            return {"error": f"Failed to get refresh token for user_id: {user_id} - {resp.text}"}
        
    except requests.exceptions.ConnectionError:
        print("\n\nCould not make connection to Supabase from get_refresh_token function\n\n")
        return {"error": "Connection error"}

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}


def store_user_refresh_token(user_id: str, token: str):
    url = f"{DB_BASE_URL}?id=eq.{user_id}"
    data = {"refresh_token": token}
    try:
        resp = requests.patch(url, json=data, headers=HEADERS)

        if resp.status_code in [200, 201]:
            return 200
        else:
            return {"error": f"Failed to insert data: {resp.status_code} - {resp.text}"}

    except requests.exceptions.ConnectionError:
        print("\n\nCould not make connection to Supabase from store_user_refresh_token function\n\n")
        return {"error": "Connection error"}

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}

def get_pwd_hash_from_db_by_user(userObject: object) -> json:
    url = f"{DB_BASE_URL}?user_name=eq.{userObject.user}"
    try:
        resp = requests.get(url, headers=HEADERS)

        if resp.status_code == 200:
            return resp.json()[0]
        elif resp.stauts_code == 401:
            return "Unauthorized request: 401"
        else:
            return f"Idk figure it out: {resp.status_code}"
        
    except Exception as e:
        if type(e) == requests.exceptions.ConnectionError:
            print("\n\nCould not make connection to supabase from check_pwd func\n\n")
            return 500
        
def create_user(user: User, hashed_pwd: str) -> json:
    url = DB_BASE_URL

    data = {
        "user_name": user.user_name,
        "email_address": user.email_address,
        "password": hashed_pwd
    }

    try:
        resp = requests.post(url, json=data, headers=HEADERS)

        if resp.status_code in [200, 201]:
            return 200
        else:
            return {"error": f"Failed to insert data: {resp.status_code} - {resp.text}"}
        
    except requests.exceptions.ConnectionError:
        print("\n\nCould not make connection to Supabase from create_user func\n\n")
        return {"error": "Connection error"}
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}