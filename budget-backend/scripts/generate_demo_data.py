#!/usr/bin/env python3
"""
Mock Data Generation Script for Demo User
Creates realistic bank accounts and transactions for demo purposes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
import random
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

class DemoDataGenerator:
    def __init__(self, demo_user_id=2):
        self.demo_user_id = demo_user_id
        self.connection = None
        self.cursor = None
        
        # Demo bank institutions
        self.institutions = [
            "Chase Bank",
            "Bank of America", 
            "Wells Fargo"
        ]
        
        # Common transaction vendors and categories
        self.vendors = {
            'groceries': ['Whole Foods', 'Safeway', 'Trader Joes', 'Costco', 'Target', 'Walmart'],
            'restaurants': ['Starbucks', 'McDonald\'s', 'Subway', 'Chipotle', 'Olive Garden', 'Pizza Hut'],
            'gas': ['Shell', 'Chevron', 'Exxon', 'BP', 'Arco'],
            'utilities': ['PG&E', 'Comcast', 'Verizon', 'AT&T', 'Water Company'],
            'entertainment': ['Netflix', 'Spotify', 'AMC Theaters', 'GameStop', 'Apple'],
            'shopping': ['Amazon', 'Best Buy', 'Macy\'s', 'Home Depot', 'CVS'],
            'income': ['Payroll Direct Deposit', 'Freelance Payment', 'Investment Return'],
            'transfer': ['Transfer to Savings', 'Transfer from Checking', 'ATM Withdrawal']
        }
        
        # Transaction amount ranges by category
        self.amount_ranges = {
            'groceries': (15.00, 200.00),
            'restaurants': (8.00, 75.00),
            'gas': (25.00, 80.00),
            'utilities': (50.00, 300.00),
            'entertainment': (9.99, 50.00),
            'shopping': (20.00, 500.00),
            'income': (1500.00, 6000.00),
            'transfer': (100.00, 1000.00)
        }

    def connect_db(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='budget-app',
                user='devuser',
                password='devpassword',
                port=3306
            )
            self.cursor = self.connection.cursor()
            print("✅ Connected to database")
        except mysql.connector.Error as error:
            print(f"❌ Database connection error: {error}")
            sys.exit(1)

    def close_db(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("✅ Database connection closed")

    def generate_demo_accounts(self):
        """Generate 3 demo bank accounts"""
        print("\n🏦 Generating demo bank accounts...")
        
        accounts = []
        base_balances = [15000.00, 8000.00, 5000.00]  # Starting balances
        
        for i, institution in enumerate(self.institutions):
            account_data = {
                'airtable_id': f'demo_acc_{i+1}_{uuid.uuid4().hex[:8]}',
                'institution': institution,
                'usd': Decimal(str(base_balances[i])),
                'last_successful_update': datetime.now(),
                'plaid_account_id': f'demo_plaid_{i+1}_{uuid.uuid4().hex[:12]}',
                'user_id': self.demo_user_id
            }
            accounts.append(account_data)
            
            # Insert into database
            insert_query = """
                INSERT INTO accounts (airtable_id, institution, usd, last_successful_update, plaid_account_id, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(insert_query, (
                account_data['airtable_id'],
                account_data['institution'],
                account_data['usd'],
                account_data['last_successful_update'],
                account_data['plaid_account_id'],
                account_data['user_id']
            ))
            
            print(f"   Created: {institution} - ${account_data['usd']}")
        
        self.connection.commit()
        print(f"✅ Generated {len(accounts)} demo accounts")
        return accounts

    def generate_demo_transactions(self, accounts, num_transactions=1000):
        """Generate realistic transactions over 6 months"""
        print(f"\n💳 Generating {num_transactions} demo transactions...")
        
        # Date range: 6 months ago to today
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=180)
        
        transactions = []
        
        for i in range(num_transactions):
            # Random date within range
            days_offset = random.randint(0, 180)
            transaction_date = start_date + timedelta(days=days_offset)
            
            # Random account
            account = random.choice(accounts)
            
            # Random transaction type
            category = random.choice(list(self.vendors.keys()))
            vendor = random.choice(self.vendors[category])
            
            # Generate amount based on category
            min_amount, max_amount = self.amount_ranges[category]
            amount = round(random.uniform(min_amount, max_amount), 2)
            
            # Make expenses negative (except income)
            if category != 'income':
                amount = -amount
                
            # Add some randomness to income frequency (less frequent but larger)
            if category == 'income' and random.random() > 0.25:  # 25% chance for more income
                continue
                
            transaction_data = {
                'airtable_id': f'demo_txn_{i+1}_{uuid.uuid4().hex[:8]}',
                'name': f'{vendor} Transaction',
                'usd': Decimal(str(amount)),
                'date': transaction_date,
                'vendor': vendor,
                'notes': self.generate_transaction_notes(category, vendor),
                'account_id': account['plaid_account_id']
            }
            
            transactions.append(transaction_data)
            
            # Insert into database
            insert_query = """
                INSERT INTO transactions (airtable_id, name, usd, date, vendor, notes, account_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(insert_query, (
                transaction_data['airtable_id'],
                transaction_data['name'],
                transaction_data['usd'],
                transaction_data['date'],
                transaction_data['vendor'],
                transaction_data['notes'],
                transaction_data['account_id']
            ))
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"   Progress: {i + 1}/{num_transactions} transactions")
        
        self.connection.commit()
        print(f"✅ Generated {len(transactions)} demo transactions")
        return transactions

    def generate_transaction_notes(self, category, vendor):
        """Generate realistic transaction notes"""
        notes_templates = {
            'groceries': ['Weekly grocery shopping', 'Monthly stock-up', 'Quick grocery run'],
            'restaurants': ['Lunch with colleagues', 'Date night dinner', 'Quick coffee break'],
            'gas': ['Weekly gas fill-up', 'Road trip fuel', 'Monthly fuel expense'],
            'utilities': ['Monthly bill payment', 'Quarterly service charge'],
            'entertainment': ['Monthly subscription', 'Weekend entertainment', 'Digital purchase'],
            'shopping': ['Online purchase', 'Weekend shopping', 'Household items'],
            'income': ['Biweekly paycheck', 'Monthly salary', 'Freelance payment'],
            'transfer': ['Account transfer', 'Savings deposit', 'Cash withdrawal']
        }
        
        if category in notes_templates:
            return random.choice(notes_templates[category])
        return f'{vendor} transaction'

    def update_account_balances(self, accounts):
        """Update account balances based on transactions"""
        print("\n💰 Updating account balances...")
        
        for account in accounts:
            # Calculate total from transactions
            self.cursor.execute("""
                SELECT SUM(usd) as total 
                FROM transactions 
                WHERE account_id = %s
            """, (account['plaid_account_id'],))
            
            result = self.cursor.fetchone()
            transaction_total = result[0] if result[0] else Decimal('0.00')
            
            # Update account balance (starting balance + transaction total)
            new_balance = account['usd'] + transaction_total
            
            self.cursor.execute("""
                UPDATE accounts 
                SET usd = %s, last_successful_update = %s
                WHERE plaid_account_id = %s
            """, (new_balance, datetime.now(), account['plaid_account_id']))
            
            print(f"   {account['institution']}: ${new_balance}")
        
        self.connection.commit()
        print("✅ Account balances updated")

    def clean_existing_demo_data(self):
        """Clean existing demo data for fresh generation"""
        print("\n🧹 Cleaning existing demo data...")
        
        # Delete transactions for demo user accounts
        self.cursor.execute("""
            DELETE t FROM transactions t
            JOIN accounts a ON t.account_id = a.plaid_account_id
            WHERE a.user_id = %s
        """, (self.demo_user_id,))
        
        # Delete demo user accounts
        self.cursor.execute("DELETE FROM accounts WHERE user_id = %s", (self.demo_user_id,))
        
        self.connection.commit()
        print("✅ Existing demo data cleaned")

    def generate_all_demo_data(self):
        """Main method to generate all demo data"""
        print("🚀 Starting demo data generation...")
        
        self.connect_db()
        
        try:
            # Clean existing data
            self.clean_existing_demo_data()
            
            # Generate accounts
            accounts = self.generate_demo_accounts()
            
            # Generate transactions
            transactions = self.generate_demo_transactions(accounts, 1000)
            
            # Update balances
            self.update_account_balances(accounts)
            
            print(f"\n🎉 Demo data generation complete!")
            print(f"   User ID: {self.demo_user_id}")
            print(f"   Accounts: {len(accounts)}")
            print(f"   Transactions: {len(transactions)}")
            
        except Exception as e:
            print(f"❌ Error during data generation: {e}")
            self.connection.rollback()
            
        finally:
            self.close_db()

if __name__ == "__main__":
    generator = DemoDataGenerator(demo_user_id=2)
    generator.generate_all_demo_data()