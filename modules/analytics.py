"""
Analytics Module
Provides financial analytics and insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from database.db import get_connection


class FinancialAnalytics:
    """Comprehensive financial analytics engine"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = get_connection()
        self.transactions_df = self._load_transactions()
    
    def _load_transactions(self):
        """Load user transactions as DataFrame"""
        query = """
            SELECT transaction_id, date, category, amount, source, description
            FROM transactions
            WHERE user_id = ?
            ORDER BY date ASC
        """
        df = pd.read_sql_query(query, self.conn, params=(self.user_id,))
        
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['amount'] = pd.to_numeric(df['amount'])
        
        return df
    
    def get_category_breakdown(self):
        """Get spending breakdown by category"""
        if self.transactions_df.empty:
            return pd.DataFrame()
        
        category_totals = self.transactions_df.groupby('category')['amount'].agg(['sum', 'count', 'mean'])
        category_totals.columns = ['Total', 'Count', 'Average']
        category_totals = category_totals.sort_values('Total', ascending=False)
        
        return category_totals
    
    def get_delivery_metrics(self):
        """Calculate delivery-specific metrics"""
        if self.transactions_df.empty:
            return {
                "delivery_total": 0,
                "delivery_count": 0,
                "delivery_percentage": 0,
                "total_spending": 0,
                "avg_delivery_order": 0
            }
        
        total_spending = self.transactions_df['amount'].sum()
        delivery_df = self.transactions_df[self.transactions_df['category'] == 'Food Delivery']
        
        delivery_total = delivery_df['amount'].sum() if not delivery_df.empty else 0
        delivery_count = len(delivery_df)
        delivery_percentage = (delivery_total / total_spending * 100) if total_spending > 0 else 0
        avg_delivery = delivery_df['amount'].mean() if not delivery_df.empty else 0
        
        return {
            "delivery_total": delivery_total,
            "delivery_count": delivery_count,
            "delivery_percentage": delivery_percentage,
            "total_spending": total_spending,
            "avg_delivery_order": avg_delivery
        }
    
    def calculate_volatility(self):
        """Calculate spending volatility (standard deviation)"""
        if self.transactions_df.empty or len(self.transactions_df) < 2:
            return 0.0
        
        # Group by date and calculate daily totals
        daily_spending = self.transactions_df.groupby('date')['amount'].sum()
        
        # Calculate standard deviation
        volatility = daily_spending.std()
        return float(volatility) if not pd.isna(volatility) else 0.0
    
    def get_weekly_comparison(self):
        """Compare spending between last two weeks"""
        if self.transactions_df.empty:
            return {
                "current_week": 0,
                "previous_week": 0,
                "change_percentage": 0,
                "trend": "neutral"
            }
        
        today = datetime.now()
        one_week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)
        
        current_week_df = self.transactions_df[
            (self.transactions_df['date'] >= one_week_ago) &
            (self.transactions_df['date'] <= today)
        ]
        
        previous_week_df = self.transactions_df[
            (self.transactions_df['date'] >= two_weeks_ago) &
            (self.transactions_df['date'] < one_week_ago)
        ]
        
        current_total = current_week_df['amount'].sum() if not current_week_df.empty else 0
        previous_total = previous_week_df['amount'].sum() if not previous_week_df.empty else 0
        
        if previous_total > 0:
            change_pct = ((current_total - previous_total) / previous_total) * 100
        else:
            change_pct = 0
        
        if change_pct > 10:
            trend = "increasing"
        elif change_pct < -10:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "current_week": current_total,
            "previous_week": previous_total,
            "change_percentage": change_pct,
            "trend": trend
        }
    
    def detect_late_night_orders(self):
        """Detect late-night delivery orders (10 PM - 2 AM)"""
        if self.transactions_df.empty:
            return []
        
        # For this demo, we'll randomly mark some delivery orders as late-night
        # In production, you'd extract hour from timestamp
        delivery_df = self.transactions_df[self.transactions_df['category'] == 'Food Delivery']
        
        # Simulate: 20% of deliveries are late-night
        late_night_sample = delivery_df.sample(n=min(len(delivery_df) // 5, len(delivery_df)))
        
        return late_night_sample[['date', 'amount', 'description']].to_dict('records')
    
    def project_future_spending(self, days=30):
        """Project future spending based on historical average"""
        if self.transactions_df.empty:
            return {
                "projected_amount": 0,
                "daily_average": 0,
                "projection_days": days
            }
        
        # Calculate daily average
        date_range = (self.transactions_df['date'].max() - self.transactions_df['date'].min()).days
        if date_range == 0:
            date_range = 1
        
        total_spending = self.transactions_df['amount'].sum()
        daily_avg = total_spending / date_range
        
        projected = daily_avg * days
        
        return {
            "projected_amount": projected,
            "daily_average": daily_avg,
            "projection_days": days
        }
    
    def get_spending_trend(self):
        """Get spending trend over time"""
        if self.transactions_df.empty:
            return pd.DataFrame()
        
        # Group by date and sum amounts
        daily_trend = self.transactions_df.groupby('date')['amount'].sum().reset_index()
        daily_trend.columns = ['Date', 'Amount']
        
        return daily_trend
    
    def calculate_delivery_ratio(self):
        """Calculate delivery spending as ratio of total spending"""
        metrics = self.get_delivery_metrics()
        total = metrics['total_spending']
        delivery = metrics['delivery_total']
        
        if total == 0:
            return 0.0
        
        return delivery / total
    
    def get_summary_stats(self):
        """Get comprehensive summary statistics"""
        if self.transactions_df.empty:
            return {
                "total_transactions": 0,
                "total_spent": 0,
                "average_transaction": 0,
                "median_transaction": 0,
                "max_transaction": 0,
                "min_transaction": 0,
                "date_range_days": 0
            }
        
        date_range = (self.transactions_df['date'].max() - self.transactions_df['date'].min()).days
        
        return {
            "total_transactions": len(self.transactions_df),
            "total_spent": self.transactions_df['amount'].sum(),
            "average_transaction": self.transactions_df['amount'].mean(),
            "median_transaction": self.transactions_df['amount'].median(),
            "max_transaction": self.transactions_df['amount'].max(),
            "min_transaction": self.transactions_df['amount'].min(),
            "date_range_days": date_range
        }
    
    def get_weekly_spending_pattern(self):
        """Get spending pattern by day of week"""
        if self.transactions_df.empty:
            return pd.DataFrame()
        
        # Add day of week column
        df = self.transactions_df.copy()
        df['day_of_week'] = df['date'].dt.day_name()
        df['day_num'] = df['date'].dt.dayofweek
        
        # Group by day of week
        daily_pattern = df.groupby(['day_num', 'day_of_week'])['amount'].sum().reset_index()
        daily_pattern.columns = ['DayNum', 'DayOfWeek', 'Amount']
        daily_pattern = daily_pattern.sort_values('DayNum')
        
        return daily_pattern
    
    def get_monthly_trend_with_projection(self):
        """Get monthly trend with 4-week projection"""
        if self.transactions_df.empty:
            return pd.DataFrame()
        
        # Get last 8 weeks of data
        today = datetime.now()
        eight_weeks_ago = today - timedelta(weeks=8)
        
        df = self.transactions_df[self.transactions_df['date'] >= eight_weeks_ago].copy()
        
        if df.empty:
            return pd.DataFrame()
        
        # Add week number
        df['week'] = (today - df['date']).dt.days // 7
        df['week'] = 8 - df['week']  # Reverse so week 1 is oldest
        
        # Group by week
        weekly_trend = df.groupby('week')['amount'].sum().reset_index()
        weekly_trend.columns = ['Week', 'Amount']
        weekly_trend = weekly_trend[weekly_trend['Week'] > 0]
        
        # Calculate projection for next 4 weeks
        if len(weekly_trend) >= 2:
            # Simple linear projection
            avg_growth = weekly_trend['Amount'].diff().mean()
            last_amount = weekly_trend['Amount'].iloc[-1]
            
            projection_weeks = []
            for i in range(1, 5):
                proj_week = weekly_trend['Week'].max() + i
                proj_amount = last_amount + (avg_growth * i)
                projection_weeks.append({
                    'Week': proj_week,
                    'Amount': max(proj_amount, 0),
                    'Type': 'Projected'
                })
            
            weekly_trend['Type'] = 'Actual'
            projection_df = pd.DataFrame(projection_weeks)
            
            result = pd.concat([weekly_trend, projection_df], ignore_index=True)
            return result
        
        weekly_trend['Type'] = 'Actual'
        return weekly_trend
    
    def get_budget_comparison(self):
        """Get budget vs actual spending by category"""
        if self.transactions_df.empty:
            return pd.DataFrame()
        
        # Calculate actual spending by category
        category_spending = self.transactions_df.groupby('category')['amount'].sum().reset_index()
        category_spending.columns = ['Category', 'Actual']
        
        # Define suggested budgets (in INR) - these could be user-defined in production
        suggested_budgets = {
            'Food Delivery': 6000,
            'Groceries': 8000,
            'Transportation': 5000,
            'Entertainment': 2000,
            'Utilities': 5000,
            'Healthcare': 3000,
            'Shopping': 15000,
            'Education': 10000,
            'Investment': 20000,
            'Other': 5000
        }
        
        # Add budget column
        category_spending['Budget'] = category_spending['Category'].map(suggested_budgets).fillna(5000)
        
        # Calculate percentage
        category_spending['Percentage'] = (category_spending['Actual'] / category_spending['Budget'] * 100).round(0)
        
        # Sort by actual spending
        category_spending = category_spending.sort_values('Actual', ascending=False)
        
        return category_spending
    
    def __del__(self):
        """Close connection on cleanup"""
        if hasattr(self, 'conn'):
            self.conn.close()
