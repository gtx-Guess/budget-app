import asyncio
import pymysql

from app.core.logger import LOG
from app.services.airtable_service import make_request_to_airtable
from app.core.constants import LOCAL_DB_HOST, LOCAL_DB_USER, LOCAL_DB_PASS, LOCAL_DB

from datetime import datetime, timedelta
from typing import Dict, Any


class AirtableSyncService:
    def __init__(self):
        self.sync_interval = 24 * 60 * 60  # 24 hours in seconds
        self.last_sync = None
        self.is_running = False

    def get_db_connection(self):
        """Get database connection"""
        try:
            connection = pymysql.connect(
                host=LOCAL_DB_HOST,
                user=LOCAL_DB_USER,
                password=LOCAL_DB_PASS,
                database=LOCAL_DB
            )
            return connection
        except pymysql.MySQLError as e:
            LOG.error(f"Database connection error: {e}")
            return None

    def is_demo_user(self, user_id: str) -> bool:
        """Check if user is a demo user"""
        connection = self.get_db_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT user_name FROM `budget-app-user` WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            return result and result[0] == 'demo'
        except pymysql.MySQLError as e:
            LOG.error(f"Database error checking demo user: {e}")
            return False
        finally:
            if connection:
                connection.close()

    async def start_background_sync(self):
        """Start the background sync task"""
        LOG.info("Starting background sync service...")
        self.is_running = True
        
        while self.is_running:
            try:
                if self.should_sync():
                    LOG.info("Starting scheduled sync...")
                    await self.sync_all_data()
                await asyncio.sleep(3600)  # Check every hour
            except Exception as e:
                LOG.error(f"Background sync error: {e}")
                await asyncio.sleep(3600)

    def should_sync(self) -> bool:
        """Check if 24 hours have passed since last sync"""
        if not self.last_sync:
            return True
        return datetime.now() - self.last_sync > timedelta(hours=24)

    async def sync_all_data(self, user_id: str = None) -> Dict[str, Any]:
        """Sync both accounts and transactions, then cleanup if needed"""
        # Skip Airtable sync for demo users
        if user_id and self.is_demo_user(user_id):
            LOG.info(f"Skipping Airtable sync for demo user: {user_id}")
            return {
                "accounts": {"status": "skipped", "reason": "demo_user"},
                "transactions": {"status": "skipped", "reason": "demo_user"},
                "cleanup": {"status": "skipped", "reason": "demo_user"}
            }
        
        results = {
            "accounts": await self.sync_accounts(),
            "transactions": await self.sync_transactions(),
            "cleanup": await self.smart_cleanup_if_needed()
        }
        self.last_sync = datetime.now()
        return results

    async def sync_accounts(self) -> Dict[str, Any]:
        """Sync accounts from Airtable to local DB"""
        return await self._sync_data_type("accounts")

    async def sync_transactions(self) -> Dict[str, Any]:
        """Sync transactions from Airtable to local DB"""
        return await self._sync_data_type("transactions")

    async def smart_cleanup_if_needed(self) -> Dict[str, Any]:
        """Only clean up if approaching the 1000 record limit"""
        from app.services.airtable_service import AIRTABLE_API, AIRTABLE_DB_ID, AIRTABLE_TRANSACTIONS
        
        try:
            table = AIRTABLE_API.table(AIRTABLE_DB_ID, AIRTABLE_TRANSACTIONS)
            all_records = table.all()
            current_count = len(all_records)
            
            LOG.info(f"Current Airtable record count: {current_count}")
            
            if current_count > 800:
                return await self.cleanup_old_airtable_records(months_to_keep=4)
            else:
                return {"status": "skipped", "current_count": current_count, "threshold": 800}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def cleanup_old_airtable_records(self, months_to_keep: int = 4) -> Dict[str, Any]:
        """Delete old records from Airtable to stay under 1000 record limit"""
        from app.services.airtable_service import AIRTABLE_API, AIRTABLE_DB_ID, AIRTABLE_TRANSACTIONS
        
        cutoff_date = datetime.now() - timedelta(days=months_to_keep * 30)
        LOG.info(f"Cleaning up records older than: {cutoff_date}")
        
        try:
            table = AIRTABLE_API.table(AIRTABLE_DB_ID, AIRTABLE_TRANSACTIONS)
            all_records = table.all()
            records_to_delete = []
            records_processed = 0
            
            for record in all_records:
                records_processed += 1
                fields = record.get('fields', {})
                
                clean_fields = {}
                for k, v in fields.items():
                    clean_key = k.replace('*', '')
                    clean_fields[clean_key] = v
                
                record_date_str = clean_fields.get('Date')
                
                if record_date_str:
                    try:
                        if 'T' in record_date_str:
                            record_date = datetime.fromisoformat(record_date_str.replace('Z', '+00:00'))
                        else:
                            record_date = datetime.strptime(record_date_str, '%Y-%m-%d')
                        
                        if record_date < cutoff_date:
                            records_to_delete.append(record['id'])
                    except ValueError as e:
                        LOG.info(f"Date parsing error: {e} for date: {record_date_str}")
                        continue
            
            # Delete old records in batches (Airtable API limit is 10 per request)
            deleted_count = 0
            for i in range(0, len(records_to_delete), 10):
                batch = records_to_delete[i:i+10]
                table.batch_delete(batch)
                deleted_count += len(batch)
                LOG.info(f"Deleted batch of {len(batch)} records")
            
            final_count = len(all_records) - deleted_count
            LOG.info(f"Cleanup complete: {deleted_count} deleted, {final_count} remaining")
            
            return {
                "status": "success",
                "deleted_count": deleted_count,
                "remaining_count": final_count,
                "cutoff_date": cutoff_date.isoformat()
            }
            
        except Exception as e:
            LOG.error(f"Cleanup error: {e}")
            return {"status": "error", "message": str(e)}

    async def _sync_data_type(self, data_type: str) -> Dict[str, Any]:
        """Generic sync method for any data type"""
        connection = self.get_db_connection()
        if not connection:
            return {"status": "error", "message": "Database connection failed"}

        cursor = connection.cursor()
        
        # Log sync start
        sync_id = self._log_sync_start(cursor, connection, data_type)
        
        try:
            # Get data from Airtable
            airtable_data = make_request_to_airtable(data_type)
            
            records_synced = 0
            
            for record in airtable_data:
                if data_type == "accounts":
                    records_synced += self._upsert_account(cursor, record)
                elif data_type == "transactions":
                    records_synced += self._upsert_transaction(cursor, record)
            
            connection.commit()
            
            # Log sync completion
            self._log_sync_completion(cursor, connection, sync_id, records_synced, "completed")
            
            LOG.info(f"Synced {records_synced} {data_type} records")
            return {
                "status": "success", 
                "records_synced": records_synced,
                "data_type": data_type
            }
            
        except Exception as e:
            connection.rollback()
            self._log_sync_completion(cursor, connection, sync_id, 0, "failed", str(e))
            LOG.error(f"Sync failed for {data_type}: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            cursor.close()
            connection.close()

    def _upsert_account(self, cursor, record: Dict) -> int:
        """Insert or update account record"""
        fields = record.get('fields', {})
        last_update = fields.get('Last Successful Update')
        parsed_date = None
        
        if last_update:
            try:
                parsed_date = datetime.fromisoformat(last_update)
            except ValueError as e:
                LOG.error(f"Date parsing error for '{last_update}': {e}")
                parsed_date = None
        
        query = """
            INSERT INTO accounts (airtable_id, institution, usd, last_successful_update, plaid_account_id, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            institution = VALUES(institution),
            usd = VALUES(usd),
            last_successful_update = VALUES(last_successful_update),
            plaid_account_id = VALUES(plaid_account_id),
            user_id = VALUES(user_id),
            updated_at = CURRENT_TIMESTAMP
        """
        
        try:
            # For now, assign all accounts to user ID 1 (your test user)
            # TODO: In the future, you'll want to determine user_id based on authentication
            default_user_id = 1
            
            cursor.execute(query, (
                record['id'],
                fields.get('Institution'),
                fields.get('USD'),
                parsed_date,
                fields.get('Plaid Account ID'),
                default_user_id
            ))
            
            return cursor.rowcount
            
        except Exception as e:
            LOG.error(f"Error inserting account {record['id']}: {e}")
            return 0

    def _upsert_transaction(self, cursor, record: Dict) -> int:
        """Insert or update transaction record"""
        fields = record.get('fields', {})
        
        query = """
            INSERT INTO transactions (airtable_id, name, usd, date, vendor, notes, account_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            usd = VALUES(usd),
            date = VALUES(date),
            vendor = VALUES(vendor),
            notes = VALUES(notes),
            account_id = VALUES(account_id),
            updated_at = CURRENT_TIMESTAMP
        """
        
        cursor.execute(query, (
            record['id'],
            fields.get('Name'),
            fields.get('USD'),
            fields.get('Date'),
            fields.get('Vendor'),
            fields.get('Notes'),
            fields.get('Account ID')
        ))
        
        return cursor.rowcount

    def _log_sync_start(self, cursor, connection, sync_type: str) -> int:
        """Log the start of a sync operation"""
        query = """
            INSERT INTO sync_log (sync_type, started_at, status)
            VALUES (%s, %s, 'running')
        """
        cursor.execute(query, (sync_type, datetime.now()))
        connection.commit()
        return cursor.lastrowid

    def _log_sync_completion(self, cursor, connection, sync_id: int, records_synced: int, status: str, error_message: str = None):
        """Log the completion of a sync operation"""
        query = """
            UPDATE sync_log 
            SET completed_at = %s, records_synced = %s, status = %s, error_message = %s
            WHERE id = %s
        """
        cursor.execute(query, (datetime.now(), records_synced, status, error_message, sync_id))
        connection.commit()

    def stop(self):
        """Stop the background sync service"""
        self.is_running = False
        LOG.info("Sync service stopped")

# Global instance
sync_service = AirtableSyncService()