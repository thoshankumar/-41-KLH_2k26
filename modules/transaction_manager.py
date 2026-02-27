"""
Transaction Manager Module
Handles all transaction input methods: CSV, Gmail, Manual, Simulation
"""

import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import random
from database.db import get_connection
from config import CATEGORIES, SOURCES


class TransactionManager:
    """Manages all transaction operations"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = get_connection()
    
    def get_all_transactions(self):
        """Get all transactions for user"""
        query = """
            SELECT transaction_id, date, category, amount, source, description, created_at
            FROM transactions
            WHERE user_id = ?
            ORDER BY date DESC
        """
        df = pd.read_sql_query(query, self.conn, params=(self.user_id,))
        return df
    
    def add_transaction(self, date, category, amount, source, description=""):
        """
        Add single transaction to database
        
        Args:
            date: Transaction date (string or datetime)
            category: Transaction category
            amount: Transaction amount (float)
            source: Transaction source
            description: Optional description
        
        Returns:
            transaction_id or None
        """
        # Check for duplicates
        if self._is_duplicate(date, amount, category):
            return None
        
        cursor = self.conn.cursor()
        try:
            # Convert datetime to string if needed
            if isinstance(date, datetime):
                date = date.strftime('%Y-%m-%d')
            
            cursor.execute("""
                INSERT INTO transactions (user_id, date, category, amount, source, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.user_id, date, category, float(amount), source, description))
            
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None
    
    def _is_duplicate(self, date, amount, category):
        """Check if transaction already exists (duplicate prevention)"""
        cursor = self.conn.cursor()
        
        # Convert datetime to string if needed
        if isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM transactions
            WHERE user_id = ? AND date = ? AND amount = ? AND category = ?
        """, (self.user_id, date, float(amount), category))
        
        result = cursor.fetchone()
        return result[0] > 0
    
    def import_csv(self, uploaded_file):
        """
        Import transactions from CSV file
        
        Expected CSV columns: date, category, amount, description (optional)
        
        Returns:
            (success_count, error_count, message)
        """
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate columns
            required_cols = ['date', 'category', 'amount']
            if not all(col in df.columns for col in required_cols):
                return 0, 0, f"CSV must contain columns: {', '.join(required_cols)}"
            
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    # Get description if exists
                    description = row.get('description', '')
                    
                    # Add transaction
                    result = self.add_transaction(
                        date=row['date'],
                        category=row['category'],
                        amount=row['amount'],
                        source=SOURCES['CSV'],
                        description=str(description)
                    )
                    
                    if result:
                        success_count += 1
                    else:
                        error_count += 1  # Duplicate or error
                        
                except Exception as e:
                    print(f"Error processing row: {e}")
                    error_count += 1
            
            return success_count, error_count, f"Imported {success_count} transactions ({error_count} duplicates skipped)"
            
        except Exception as e:
            return 0, 0, f"Error reading CSV: {str(e)}"
    
    def add_manual_transaction(self, date, category, amount, description=""):
        """Add manual transaction via form"""
        result = self.add_transaction(
            date=date,
            category=category,
            amount=amount,
            source=SOURCES['MANUAL'],
            description=description
        )
        return result is not None
    
    def simulate_transaction(self):
        """
        Simulate a delivery order transaction
        Returns: (success, message)
        """
        # Random delivery service and amount
        categories = ["Food Delivery"]
        amounts = [250, 350, 450, 550, 650, 750, 420, 380, 520]
        descriptions = [
            "Swiggy Order - Dinner",
            "Zomato Order - Lunch",
            "Swiggy Order - Late Night Snack",
            "Zomato Order - Weekend Treat",
            "Swiggy Order - Office Lunch"
        ]
        
        # Random date in last 7 days
        days_ago = random.randint(0, 7)
        sim_date = datetime.now() - timedelta(days=days_ago)
        
        result = self.add_transaction(
            date=sim_date,
            category=random.choice(categories),
            amount=random.choice(amounts),
            source=SOURCES['SIMULATION'],
            description=random.choice(descriptions)
        )
        
        if result:
            return True, "✅ Simulated delivery order added successfully!"
        else:
            return False, "⚠️ Could not add simulation (duplicate detected)"
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM transactions
                WHERE transaction_id = ? AND user_id = ?
            """, (transaction_id, self.user_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            return False
    
    def get_transaction_stats(self):
        """Get basic transaction statistics"""
        df = self.get_all_transactions()
        
        if df.empty:
            return {
                "total_transactions": 0,
                "total_spent": 0.0,
                "avg_transaction": 0.0,
                "date_range": "No data"
            }
        
        return {
            "total_transactions": len(df),
            "total_spent": df['amount'].sum(),
            "avg_transaction": df['amount'].mean(),
            "date_range": f"{df['date'].min()} to {df['date'].max()}"
        }
    
    def export_csv(self):
        """Export transactions to CSV"""
        df = self.get_all_transactions()
        return df.to_csv(index=False)
    
    def __del__(self):
        """Close connection on cleanup"""
        if hasattr(self, 'conn'):
            self.conn.close()
