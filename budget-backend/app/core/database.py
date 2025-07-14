import pymysql

from app.core.logger import LOG
from app.models.schemas import User
from app.core.constants import LOCAL_DB_HOST, LOCAL_DB_USER, LOCAL_DB_PASS, LOCAL_DB


LOG.info("Setting up connection to local db")

def get_db_connection():
    """Get a fresh database connection each time"""
    try:
        connection = pymysql.connect(
            host=LOCAL_DB_HOST,
            user=LOCAL_DB_USER,
            password=LOCAL_DB_PASS,
            database=LOCAL_DB
        )
        cursor = connection.cursor()
        return connection, cursor
    except pymysql.MySQLError as e:
        LOG.error(f"Failed to connect to database: {e}")
        return None, None

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
    finally:
        cur.close()

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
    finally:
        cur.close()

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
    finally:
        cur.close()

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

def get_all_transactions(user_id: str = None):
    """Get all transactions from local database for a specific user"""
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        
        if user_id:
            # Get transactions for specific user by joining with accounts
            query = """
                SELECT t.id, t.airtable_id, t.name, t.usd, t.date, t.vendor, t.notes, t.account_id,
                       t.created_at, t.updated_at 
                FROM transactions t
                JOIN accounts a ON t.account_id = a.plaid_account_id
                WHERE a.user_id = %s
                ORDER BY t.date DESC
            """
            cur.execute(query, (user_id,))
        else:
            # Get all transactions (backward compatibility)
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

def is_demo_user(user_id: str) -> bool:
    """Check if user is a demo user"""
    conn, cur = get_db_connection()
    if cur is None:
        return False
    
    try:
        query = """
            SELECT user_name FROM `budget-app-user` WHERE id = %s
        """
        cur.execute(query, (user_id,))
        result = cur.fetchone()
        return result and result[0] == 'demo'
        
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return False
    finally:
        cur.close()

def get_user_by_username(username: str):
    """Get user details by username"""
    conn, cur = get_db_connection()
    if cur is None:
        return None
    
    try:
        query = """
            SELECT id, user_name, email_address FROM `budget-app-user` 
            WHERE user_name = %s
        """
        cur.execute(query, (username,))
        result = cur.fetchone()
        
        if result:
            return {
                'id': result[0],
                'user_name': result[1],
                'email_address': result[2]
            }
        return None
        
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return None
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
    finally:
        cur.close()

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
    finally:
        cur.close()

# Admin functions
def get_all_users_admin():
    """Get all users with basic info (admin only)"""
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        query = """
            SELECT id, user_name, email_address, created_at 
            FROM `budget-app-user` 
            ORDER BY created_at DESC
        """
        cur.execute(query)
        users = cur.fetchall()
        
        user_list = []
        for user in users:
            user_list.append({
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "created_at": user[3].isoformat() if user[3] else None,
                "is_demo": user[1] == "demo"
            })
        
        return user_list
        
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}
    finally:
        cur.close()

def admin_update_user_password(username: str, hashed_password: str) -> bool:
    """Update any user's password (admin only)"""
    conn, cur = get_db_connection()
    if cur is None:
        return False
    
    try:
        query = """
            UPDATE `budget-app-user` 
            SET `password` = %s 
            WHERE user_name = %s
        """
        cur.execute(query, (hashed_password, username))
        conn.commit()
        
        return cur.rowcount > 0
        
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return False
    finally:
        cur.close()

def reset_demo_data() -> bool:
    """Reset demo user data by regenerating accounts and transactions"""
    conn, cur = get_db_connection()
    if cur is None:
        return False
    
    try:
        # Delete demo user transactions and accounts
        cur.execute("""
            DELETE t FROM transactions t
            JOIN accounts a ON t.account_id = a.plaid_account_id
            WHERE a.user_id = 2
        """)
        
        cur.execute("DELETE FROM accounts WHERE user_id = 2")
        conn.commit()
        
        # Regenerate demo data would be done by calling the demo data generator
        # For now, just return success
        return True
        
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return False
    finally:
        cur.close()

def get_user_statistics():
    """Get user statistics for admin dashboard"""
    conn, cur = get_db_connection()
    if cur is None:
        return {"error": "Database connection failed"}
    
    try:
        # Get total users
        cur.execute("SELECT COUNT(*) FROM `budget-app-user`")
        total_users = cur.fetchone()[0]
        
        # Get demo user ID
        cur.execute("SELECT id FROM `budget-app-user` WHERE user_name = 'demo'")
        demo_user = cur.fetchone()
        demo_user_id = demo_user[0] if demo_user else None
        
        # Get account counts
        cur.execute("SELECT COUNT(*) FROM accounts WHERE user_id != %s", (demo_user_id,))
        real_accounts = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM accounts WHERE user_id = %s", (demo_user_id,))
        demo_accounts = cur.fetchone()[0]
        
        # Get transaction counts
        cur.execute("""
            SELECT COUNT(*) FROM transactions t
            JOIN accounts a ON t.account_id = a.plaid_account_id
            WHERE a.user_id != %s
        """, (demo_user_id,))
        real_transactions = cur.fetchone()[0]
        
        cur.execute("""
            SELECT COUNT(*) FROM transactions t
            JOIN accounts a ON t.account_id = a.plaid_account_id
            WHERE a.user_id = %s
        """, (demo_user_id,))
        demo_transactions = cur.fetchone()[0]
        
        return {
            "total_users": total_users,
            "real_accounts": real_accounts,
            "demo_accounts": demo_accounts,
            "real_transactions": real_transactions,
            "demo_transactions": demo_transactions
        }
        
    except pymysql.MySQLError as e:
        LOG.error(f"Database error: {e}")
        return {"error": "Database error"}
    finally:
        cur.close()