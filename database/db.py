"""
Database module for AI Behavioral Finance Coach
Handles SQLite connection and initialization
"""

import sqlite3
import os
from datetime import datetime
import bcrypt

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'finance_coach.db')
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')


def get_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def initialize_database():
    """Initialize database with schema and demo user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Read and execute schema
    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    # Create demo user if not exists
    demo_email = "demo@financecoach.ai"
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (demo_email,))
    
    if not cursor.fetchone():
        # Hash demo password
        demo_password = "demo123"
        password_hash = bcrypt.hashpw(demo_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", demo_email, password_hash)
        )
        print(f"✓ Demo user created: {demo_email} / {demo_password}")
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a database query with error handling
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch_one: Return single row
        fetch_all: Return all rows
    
    Returns:
        Query results or None
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            result = cursor.fetchone()
            conn.close()
            return result
        elif fetch_all:
            result = cursor.fetchall()
            conn.close()
            return result
        else:
            conn.commit()
            conn.close()
            return cursor.lastrowid
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.close()
        return None


def get_user_by_email(email):
    """Retrieve user by email"""
    query = "SELECT * FROM users WHERE email = ?"
    return execute_query(query, (email,), fetch_one=True)


def get_user_by_id(user_id):
    """Retrieve user by ID"""
    query = "SELECT * FROM users WHERE user_id = ?"
    return execute_query(query, (user_id,), fetch_one=True)


def create_user(name, email, password):
    """Create new user with hashed password"""
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query = "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)"
    return execute_query(query, (name, email, password_hash))


def verify_password(plain_password, password_hash):
    """Verify password against hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8'))


# Initialize database on module import
if not os.path.exists(DB_PATH):
    initialize_database()
