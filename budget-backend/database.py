import requests
import json
import pymysql
from constants import DB_BASE_URL, SUPA_ACCESS_TOKEN, IS_LOCAL, LOCAL_DB_HOST, LOCAL_DB_USER, LOCAL_DB_PASS, LOCAL_DB
from schemas import User

HEADERS = {
    "apikey": SUPA_ACCESS_TOKEN,
    "Authorization": f"Bearer {SUPA_ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

if IS_LOCAL:
    print("Running locally, setting up connection to local db")
    try:
        connection = pymysql.connect(
            host=LOCAL_DB_HOST,
            user=LOCAL_DB_USER,
            password=LOCAL_DB_PASS,
            database=LOCAL_DB
        )
        print(f"Connection successful to `{LOCAL_DB}`")

        # Create a cursor object
        cursor = connection.cursor()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")

def get_refresh_token(user_id: str) -> str:
    if IS_LOCAL:
        query = """
            SELECT `refresh_token` FROM `budget-app-user` WHERE id = %s
        """
        cursor.execute(query, user_id)
        results = cursor.fetchone()
        return results[0]
    else:
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
    if IS_LOCAL:
        try:
            query = """
                UPDATE `budget-app-user`
                SET `refresh_token` = %s
                WHERE id = %s
            """
            resp = cursor.execute(query, (token, user_id))
            connection.commit()
            if resp == 1:
                return 200
            else:
                return {"error": f"Failed to update row with refresh token for id: {user_id}"}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return 500
    else:
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
    if IS_LOCAL:
        try:
            query = """
                SELECT password, id FROM `budget-app-user` WHERE `user_name` = %s
            """
            resp = cursor.execute(query, userObject.user)
            results = cursor.fetchone()
            return {"password": results[0], "id": results[1]}
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return 500
    else:
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
    data = {
        "user_name": user.user_name,
        "email_address": user.email_address,
        "password": hashed_pwd
    }

    if IS_LOCAL:

        try:
            query = """
                INSERT INTO `budget-app-user` (`user_name`, `email_address`, `password`) VALUES (%s, %s, %s)
            """
            resp = cursor.execute(query, (data["user_name"], data["email_address"], data["password"]))

            connection.commit()
            if resp == 1:
                return 200
            else:
                return 400

        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return {"status": 500, "message": "Database error"}
        
    else:
        url = DB_BASE_URL

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