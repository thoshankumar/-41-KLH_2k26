"""
Financial Health Score Engine
Calculates comprehensive health score (0-100) based on multiple factors
"""

import numpy as np
from datetime import datetime
from database.db import get_connection, execute_query
from config import HEALTH_SCORE_WEIGHTS, RISK_THRESHOLDS
from modules.analytics import FinancialAnalytics
from modules.anomaly import AnomalyDetector


class HealthScoreEngine:
    """Calculate and track financial health score"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = get_connection()
        self.analytics = FinancialAnalytics(user_id)
        self.anomaly_detector = AnomalyDetector(user_id)
        self.weights = HEALTH_SCORE_WEIGHTS
    
    def calculate_health_score(self):
        """
        Calculate comprehensive health score (0-100)
        
        Components:
        1. Delivery ratio (30%)
        2. Volatility (25%)
        3. Anomaly frequency (25%)
        4. Overspending (20%)
        
        Returns:
            dict with score and component breakdown
        """
        # Get metrics
        delivery_ratio = self.analytics.calculate_delivery_ratio()
        volatility = self.analytics.calculate_volatility()
        anomaly_count = self.anomaly_detector.get_anomaly_count()
        total_transactions = len(self.analytics.transactions_df)
        
        # Calculate component scores (0-100 each)
        delivery_score = self._score_delivery_ratio(delivery_ratio)
        volatility_score = self._score_volatility(volatility)
        anomaly_score = self._score_anomalies(anomaly_count, total_transactions)
        overspend_score = self._score_overspending()
        
        # Calculate weighted final score
        final_score = (
            delivery_score * self.weights['delivery_ratio'] +
            volatility_score * self.weights['volatility'] +
            anomaly_score * self.weights['anomaly_frequency'] +
            overspend_score * self.weights['overspending']
        )
        
        # Ensure score is between 0-100
        final_score = max(0, min(100, final_score))
        
        return {
            'final_score': round(final_score, 1),
            'components': {
                'delivery_ratio': {
                    'score': round(delivery_score, 1),
                    'value': round(delivery_ratio * 100, 1),
                    'weight': self.weights['delivery_ratio']
                },
                'volatility': {
                    'score': round(volatility_score, 1),
                    'value': round(volatility, 2),
                    'weight': self.weights['volatility']
                },
                'anomaly_frequency': {
                    'score': round(anomaly_score, 1),
                    'value': anomaly_count,
                    'weight': self.weights['anomaly_frequency']
                },
                'overspending': {
                    'score': round(overspend_score, 1),
                    'weight': self.weights['overspending']
                }
            },
            'grade': self._get_grade(final_score),
            'status': self._get_status(final_score)
        }
    
    def _score_delivery_ratio(self, ratio):
        """Score based on delivery spending ratio (lower is better)"""
        threshold = RISK_THRESHOLDS['high_delivery_ratio']
        
        if ratio <= threshold * 0.5:  # Very low delivery spending
            return 100
        elif ratio <= threshold:  # Acceptable
            return 100 - ((ratio - threshold * 0.5) / (threshold * 0.5)) * 20
        elif ratio <= threshold * 2:  # High
            return 80 - ((ratio - threshold) / threshold) * 50
        else:  # Very high
            return max(0, 30 - (ratio - threshold * 2) * 100)
    
    def _score_volatility(self, volatility):
        """Score based on spending volatility (lower is better)"""
        if self.analytics.transactions_df.empty:
            return 100
        
        # Normalize volatility by average transaction
        avg_amount = self.analytics.transactions_df['amount'].mean()
        if avg_amount == 0:
            return 100
        
        normalized_volatility = volatility / avg_amount
        
        if normalized_volatility <= 0.2:  # Very low volatility
            return 100
        elif normalized_volatility <= 0.5:  # Low volatility
            return 100 - (normalized_volatility - 0.2) / 0.3 * 20
        elif normalized_volatility <= 1.0:  # Moderate volatility
            return 80 - (normalized_volatility - 0.5) / 0.5 * 40
        else:  # High volatility
            return max(0, 40 - (normalized_volatility - 1.0) * 30)
    
    def _score_anomalies(self, anomaly_count, total_transactions):
        """Score based on anomaly frequency (lower is better)"""
        if total_transactions == 0:
            return 100
        
        anomaly_rate = anomaly_count / total_transactions
        
        if anomaly_rate == 0:
            return 100
        elif anomaly_rate <= 0.05:  # Less than 5%
            return 100 - (anomaly_rate / 0.05) * 10
        elif anomaly_rate <= 0.15:  # 5-15%
            return 90 - ((anomaly_rate - 0.05) / 0.10) * 40
        else:  # More than 15%
            return max(0, 50 - (anomaly_rate - 0.15) * 200)
    
    def _score_overspending(self):
        """Score based on overspending incidents"""
        overspend_periods = self.anomaly_detector.detect_overspending_periods()
        total_transactions = len(self.analytics.transactions_df)
        
        if total_transactions == 0:
            return 100
        
        overspend_rate = len(overspend_periods) / total_transactions
        
        if overspend_rate == 0:
            return 100
        elif overspend_rate <= 0.1:  # Less than 10%
            return 100 - (overspend_rate / 0.1) * 20
        elif overspend_rate <= 0.25:  # 10-25%
            return 80 - ((overspend_rate - 0.1) / 0.15) * 40
        else:  # More than 25%
            return max(0, 40 - (overspend_rate - 0.25) * 100)
    
    def _get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90:
            return "A+ Excellent"
        elif score >= 80:
            return "A Good"
        elif score >= 70:
            return "B Fair"
        elif score >= 60:
            return "C Needs Improvement"
        elif score >= 50:
            return "D Poor"
        else:
            return "F Critical"
    
    def _get_status(self, score):
        """Get status description"""
        if score >= 80:
            return "Healthy"
        elif score >= 60:
            return "Moderate"
        else:
            return "At Risk"
    
    def save_metrics(self):
        """Save current metrics to database"""
        score_data = self.calculate_health_score()
        delivery_metrics = self.analytics.get_delivery_metrics()
        volatility = self.analytics.calculate_volatility()
        anomaly_count = self.anomaly_detector.get_anomaly_count()
        
        # For overspend risk, we'll use a simple calculation
        # In production, this would come from the ML model
        delivery_ratio = delivery_metrics['delivery_percentage'] / 100
        overspend_risk = self._calculate_simple_risk(delivery_ratio, volatility, anomaly_count)
        
        query = """
            INSERT INTO metrics (user_id, health_score, overspend_risk, volatility, 
                                delivery_ratio, anomaly_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        execute_query(query, (
            self.user_id,
            score_data['final_score'],
            overspend_risk,
            volatility,
            delivery_ratio,
            anomaly_count
        ))
        
        return score_data
    
    def _calculate_simple_risk(self, delivery_ratio, volatility, anomaly_count):
        """Calculate simple overspending risk score (0-1)"""
        # Simple weighted risk calculation
        risk = (
            delivery_ratio * 0.4 +
            min(volatility / 1000, 1.0) * 0.3 +
            min(anomaly_count / 10, 1.0) * 0.3
        )
        return min(max(risk, 0), 1)
    
    def get_previous_score(self):
        """Get previous health score for comparison"""
        query = """
            SELECT health_score, calculated_at
            FROM metrics
            WHERE user_id = ?
            ORDER BY calculated_at DESC
            LIMIT 2
        """
        
        results = execute_query(query, (self.user_id,), fetch_all=True)
        
        if results and len(results) >= 2:
            return {
                'previous_score': results[1]['health_score'],
                'current_score': results[0]['health_score'],
                'change': results[0]['health_score'] - results[1]['health_score'],
                'calculated_at': results[1]['calculated_at']
            }
        
        return None
    
    def get_score_history(self):
        """Get health score history"""
        query = """
            SELECT health_score, overspend_risk, calculated_at
            FROM metrics
            WHERE user_id = ?
            ORDER BY calculated_at DESC
            LIMIT 10
        """
        
        results = execute_query(query, (self.user_id,), fetch_all=True)
        
        return [dict(row) for row in results] if results else []
    
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'conn'):
            self.conn.close()
