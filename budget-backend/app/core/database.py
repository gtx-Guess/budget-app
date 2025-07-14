import pymysql

from app.core.logger import LOG
from app.models.schemas import User
from app.core.constants import LOCAL_DB_HOST, LOCAL_DB_USER, LOCAL_DB_PASS, LOCAL_DB


LOG.info("Setting up connection to local db")

connection = None
cursor = None

def get_db_connection():
    global connection, cursor
    if connection is None or not connection.open:
        try:
            connection = pymysql.connect(
                host=LOCAL_DB_HOST,
                user=LOCAL_DB_USER,
                password=LOCAL_DB_PASS,
                database=LOCAL_DB
            )
            cursor = connection.cursor()
            LOG.info(f"Database connected successfully to `{LOCAL_DB}`")
        except pymysql.MySQLError as e:
            LOG.error(f"Failed to connect to database: {e}")
            return None, None
    return connection, cursor

def get_refresh_token(user_id: str) -> str:
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        query = """
            SELECT `refresh_token` FROM `budget-app-user` WHERE id = %s
        """
        cur.execute(query, user_id)
        results = cur.fetchone()
        return results[0] if results else None
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}

def store_user_refresh_token(user_id: str, token: str):
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        query = """
            UPDATE `budget-app-user`
            SET `refresh_token` = %s
            WHERE id = %s
        """
        resp = cur.execute(query, (token, user_id))
        conn.commit()
        return 200 if resp == 1 else {"error": f"Failed to update row with refresh token for id: {user_id}"}
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}

def get_pwd_hash_from_db_by_user(userObject: object) -> dict:
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        query = """
            SELECT password, id FROM `budget-app-user` WHERE `user_name` = %s
        """
        cur.execute(query, userObject.user)
        results = cur.fetchone()
        return {"password": results[0], "id": results[1]} if results else None
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}

def create_user(user: User, hashed_pwd: str) -> int:
    conn, cur = get_db_connection()
    if cur is None:
        return {"status": 500, "message": "Database connection failed"}
    
    try:
        query = """
            INSERT INTO `budget-app-user` (`user_name`, `email_address`, `password`) VALUES (%s, %s, %s)
        """
        resp = cur.execute(query, (user.user_name, user.email_address, hashed_pwd))
        conn.commit()
        return 200 if resp == 1 else 400
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"status": 500, "message": "Database error"}
    
def get_all_accounts(user_id: str = None):
    """Get all accounts from local database for a specific user"""
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        
        if user_id:
            # Filter by user_id when provided
            query = """
                SELECT id, airtable_id, institution, usd, last_successful_update, 
                       plaid_account_id, user_id, created_at, updated_at 
                FROM accounts 
                WHERE user_id = %s
                ORDER BY institution
            """
            cur.execute(query, (user_id,))
        else:
            # Fallback for backward compatibility (no filtering)
            query = """
                SELECT id, airtable_id, institution, usd, last_successful_update, 
                       plaid_account_id, user_id, created_at, updated_at 
                FROM accounts 
                ORDER BY institution
            """
            cur.execute(query)
        accounts = cur.fetchall()
        formatted_accounts = []
        for account in accounts:
            formatted_accounts.append({
                "id": account["airtable_id"],
                "fields": {
                    "Institution": account["institution"],
                    "USD": float(account["usd"]) if account["usd"] else 0,
                    "Last Successful Update": account["last_successful_update"].strftime('%B %d at %H:%M') if account["last_successful_update"] else None,
                    "Plaid Account ID": account["plaid_account_id"]
                }
            })
        
        return formatted_accounts
        
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}
    finally:
        cur.close()

def get_all_transactions():
    """Get all transactions from local database"""
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        
        query = """
            SELECT id, airtable_id, name, usd, date, vendor, notes, account_id,
                   created_at, updated_at 
            FROM transactions 
            ORDER BY date DESC
        """
        cur.execute(query)
        transactions = cur.fetchall()
        formatted_transactions = []
        for transaction in transactions:
            formatted_transactions.append({
                "id": transaction["airtable_id"],
                "fields": {
                    "Name": transaction["name"],
                    "USD": float(transaction["usd"]) if transaction["usd"] else 0,
                    "Date": transaction["date"].strftime('%Y-%m-%d') if transaction["date"] else None,
                    "Vendor": transaction["vendor"],
                    "Notes": transaction["notes"],
                    "Account ID": transaction["account_id"]
                }
            })
        
        return formatted_transactions
        
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}
    finally:
        cur.close()

def get_user_by_id(user_id: str, include_password: bool = False):
    """Get user details by user ID"""
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        if include_password:
            query = """
                SELECT id, user_name, email_address, password, created_at
                FROM `budget-app-user` 
                WHERE id = %s
            """
        else:
            query = """
                SELECT id, user_name, email_address, created_at
                FROM `budget-app-user` 
                WHERE id = %s
            """
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        
        if user:
            # Split user_name into first and last name if it contains a space
            full_name = user[1] if user[1] else ""
            name_parts = full_name.split(" ", 1)
            
            result = {
                "id": user[0],
                "first_name": name_parts[0] if name_parts else "",
                "last_name": name_parts[1] if len(name_parts) > 1 else "",
                "email_address": user[2],
                "user_name": user[1],
                "created_at": user[-1].isoformat() if user[-1] else None
            }
            
            if include_password:
                result["password"] = user[3]
            
            return result
        else:
            return None
            
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}

def update_user_password(user_id: str, hashed_password: str):
    """Update user's password"""
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        query = """
            UPDATE `budget-app-user`
            SET `password` = %s
            WHERE id = %s
        """
        resp = cur.execute(query, (hashed_password, user_id))
        conn.commit()
        return 200 if resp == 1 else {"error": f"Failed to update password for user_id: {user_id}"}
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}

def update_user_email(user_id: str, new_email: str):
    """Update user's email address"""
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        query = """
            UPDATE `budget-app-user`
            SET `email_address` = %s
            WHERE id = %s
        """
        resp = cur.execute(query, (new_email, user_id))
        conn.commit()
        return 200 if resp == 1 else {"error": f"Failed to update email for user_id: {user_id}"}
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}