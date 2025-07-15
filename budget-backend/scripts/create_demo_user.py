#!/usr/bin/env python3
"""
Script to create a demo user account for the Budget App
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from passlib.context import CryptContext
import mysql.connector

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_demo_user():
    # Demo user details
    demo_user = {
        'user_name': 'demo',
        'first_name': 'Demo',
        'last_name': 'User',
        'email_address': 'demo@budgetapp.com',
        'password': 'demo123',  # Simple password for demo
        'pld_public_token': None,
        'refresh_token': None
    }
    
    # Hash the password
    hashed_password = hash_password(demo_user['password'])
    
    # Database connection
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='budget-app',
            user='devuser',
            password='devpassword',
            port=3306
        )
        
        cursor = connection.cursor()
        
        # Check if demo user already exists
        cursor.execute(
            "SELECT id FROM `budget-app-user` WHERE user_name = %s OR email_address = %s",
            (demo_user['user_name'], demo_user['email_address'])
        )
        
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"Demo user already exists with ID: {existing_user[0]}")
            return existing_user[0]
        
        # Insert demo user
        insert_query = """
            INSERT INTO `budget-app-user` (user_name, first_name, last_name, email_address, password, pld_public_token, refresh_token)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            demo_user['user_name'],
            demo_user['first_name'],
            demo_user['last_name'],
            demo_user['email_address'],
            hashed_password,
            demo_user['pld_public_token'],
            demo_user['refresh_token']
        ))
        
        connection.commit()
        user_id = cursor.lastrowid
        
        print(f"✅ Demo user created successfully!")
        print(f"   User ID: {user_id}")
        print(f"   Username: {demo_user['user_name']}")
        print(f"   Email: {demo_user['email_address']}")
        print(f"   Password: {demo_user['password']}")
        
        return user_id
        
    except mysql.connector.Error as error:
        print(f"❌ Database error: {error}")
        return None
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_demo_user()