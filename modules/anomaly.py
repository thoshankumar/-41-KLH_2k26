"""
Anomaly Detection Module
Identifies unusual spending patterns using statistical methods
"""

import pandas as pd
import numpy as np
from scipy import stats
from database.db import get_connection
from config import RISK_THRESHOLDS


class AnomalyDetector:
    """Detect anomalies in spending patterns using Z-score method"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = get_connection()
        self.transactions_df = self._load_transactions()
        self.zscore_threshold = RISK_THRESHOLDS['anomaly_zscore']
    
    def _load_transactions(self):
        """Load user transactions"""
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
    
    def detect_amount_anomalies(self):
        """
        Detect anomalies based on transaction amount using Z-score
        
        Returns:
            List of anomalous transactions
        """
        if self.transactions_df.empty or len(self.transactions_df) < 3:
            return []
        
        # Calculate Z-scores for amounts
        amounts = self.transactions_df['amount'].values
        mean = np.mean(amounts)
        std = np.std(amounts)
        
        if std == 0:
            return []
        
        z_scores = np.abs((amounts - mean) / std)
        
        # Find anomalies
        anomaly_indices = np.where(z_scores > self.zscore_threshold)[0]
        
        if len(anomaly_indices) == 0:
            return []
        
        anomalies = []
        for idx in anomaly_indices:
            transaction = self.transactions_df.iloc[idx]
            anomalies.append({
                'transaction_id': transaction['transaction_id'],
                'date': transaction['date'].strftime('%Y-%m-%d'),
                'category': transaction['category'],
                'amount': transaction['amount'],
                'z_score': z_scores[idx],
                'description': transaction['description'],
                'deviation': f"{((transaction['amount'] - mean) / mean * 100):.1f}% above average"
            })
        
        return anomalies
    
    def detect_category_anomalies(self):
        """Detect anomalies within each category"""
        if self.transactions_df.empty:
            return []
        
        anomalies = []
        
        for category in self.transactions_df['category'].unique():
            category_df = self.transactions_df[self.transactions_df['category'] == category]
            
            if len(category_df) < 3:
                continue
            
            amounts = category_df['amount'].values
            mean = np.mean(amounts)
            std = np.std(amounts)
            
            if std == 0:
                continue
            
            z_scores = np.abs((amounts - mean) / std)
            anomaly_mask = z_scores > self.zscore_threshold
            
            for idx, is_anomaly in enumerate(anomaly_mask):
                if is_anomaly:
                    transaction = category_df.iloc[idx]
                    anomalies.append({
                        'transaction_id': transaction['transaction_id'],
                        'date': transaction['date'].strftime('%Y-%m-%d'),
                        'category': category,
                        'amount': transaction['amount'],
                        'z_score': z_scores[idx],
                        'description': transaction['description'],
                        'category_average': mean,
                        'deviation': f"{((transaction['amount'] - mean) / mean * 100):.1f}% above category average"
                    })
        
        return anomalies
    
    def detect_frequency_anomalies(self):
        """Detect unusual spending frequency patterns"""
        if self.transactions_df.empty:
            return {}
        
        # Count transactions per day
        daily_counts = self.transactions_df.groupby('date').size()
        
        if len(daily_counts) < 3:
            return {}
        
        mean_daily = daily_counts.mean()
        std_daily = daily_counts.std()
        
        if std_daily == 0:
            return {}
        
        # Find days with unusual transaction frequency
        z_scores = np.abs((daily_counts - mean_daily) / std_daily)
        anomalous_days = daily_counts[z_scores > self.zscore_threshold]
        
        return {
            'average_daily_transactions': mean_daily,
            'anomalous_days': [
                {
                    'date': date.strftime('%Y-%m-%d'),
                    'count': count,
                    'deviation': f"{((count - mean_daily) / mean_daily * 100):.1f}% above average"
                }
                for date, count in anomalous_days.items()
            ]
        }
    
    def get_anomaly_count(self):
        """Get total count of detected anomalies"""
        amount_anomalies = self.detect_amount_anomalies()
        return len(amount_anomalies)
    
    def get_anomaly_summary(self):
        """Get comprehensive anomaly summary"""
        amount_anomalies = self.detect_amount_anomalies()
        category_anomalies = self.detect_category_anomalies()
        frequency_analysis = self.detect_frequency_anomalies()
        
        return {
            'total_amount_anomalies': len(amount_anomalies),
            'total_category_anomalies': len(category_anomalies),
            'amount_anomalies': amount_anomalies,
            'category_anomalies': category_anomalies,
            'frequency_analysis': frequency_analysis,
            'anomaly_rate': len(amount_anomalies) / len(self.transactions_df) * 100 if not self.transactions_df.empty else 0
        }
    
    def detect_overspending_periods(self):
        """Detect periods where spending exceeds threshold"""
        if self.transactions_df.empty:
            return []
        
        # Calculate average spending
        avg_spending = self.transactions_df['amount'].mean()
        threshold = avg_spending * RISK_THRESHOLDS['overspend_threshold']
        
        # Find transactions exceeding threshold
        overspending = self.transactions_df[self.transactions_df['amount'] > threshold]
        
        return [{
            'date': row['date'].strftime('%Y-%m-%d'),
            'amount': row['amount'],
            'category': row['category'],
            'threshold': threshold,
            'excess': row['amount'] - threshold
        } for _, row in overspending.iterrows()]
    
    def __del__(self):
        """Close connection on cleanup"""
        if hasattr(self, 'conn'):
            self.conn.close()
