"""
ML Prediction Module
Predicts overspending risk using machine learning
"""

import numpy as np
import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from modules.analytics import FinancialAnalytics
from modules.anomaly import AnomalyDetector
from config import ML_MODEL_PATH, ML_FEATURES


class OverspendPredictor:
    """ML-based overspending risk prediction"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.analytics = FinancialAnalytics(user_id)
        self.anomaly_detector = AnomalyDetector(user_id)
        self.model = None
        self.scaler = None
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Load existing model or train new one"""
        model_path = ML_MODEL_PATH
        
        # Ensure models directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        if os.path.exists(model_path):
            # Load existing model
            try:
                with open(model_path, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.model = saved_data['model']
                    self.scaler = saved_data['scaler']
            except:
                # If loading fails, train new model
                self._train_demo_model()
        else:
            # Train new model
            self._train_demo_model()
    
    def _train_demo_model(self):
        """Train a demo model with synthetic data"""
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 200
        
        # Features: delivery_ratio, volatility, anomaly_count, budget_breach_count
        X = np.random.rand(n_samples, 4)
        
        # Adjust feature ranges
        X[:, 0] = X[:, 0] * 0.5  # delivery_ratio: 0-0.5
        X[:, 1] = X[:, 1] * 500  # volatility: 0-500
        X[:, 2] = (X[:, 2] * 10).astype(int)  # anomaly_count: 0-10
        X[:, 3] = (X[:, 3] * 5).astype(int)  # budget_breach_count: 0-5
        
        # Generate labels based on features (synthetic logic)
        # High delivery ratio, high volatility, or many anomalies -> overspending risk
        y = (
            (X[:, 0] > 0.25) | 
            (X[:, 1] > 300) | 
            (X[:, 2] > 5) | 
            (X[:, 3] > 2)
        ).astype(int)
        
        # Train model
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.model.fit(X_scaled, y)
        
        # Save model
        with open(ML_MODEL_PATH, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'trained_at': datetime.now().isoformat(),
                'features': ML_FEATURES
            }, f)
        
        print("✓ ML model trained and saved")
    
    def extract_features(self):
        """Extract features for prediction"""
        if self.analytics.transactions_df.empty:
            # Return default features for no data
            return np.array([[0.0, 0.0, 0, 0]])
        
        # Feature 1: Delivery ratio
        delivery_ratio = self.analytics.calculate_delivery_ratio()
        
        # Feature 2: Volatility
        volatility = self.analytics.calculate_volatility()
        
        # Feature 3: Anomaly count
        anomaly_count = self.anomaly_detector.get_anomaly_count()
        
        # Feature 4: Budget breach count (overspending periods)
        budget_breaches = len(self.anomaly_detector.detect_overspending_periods())
        
        features = np.array([[
            delivery_ratio,
            volatility,
            anomaly_count,
            budget_breaches
        ]])
        
        return features
    
    def predict_overspend_risk(self):
        """
        Predict overspending risk
        
        Returns:
            dict with risk probability and classification
        """
        features = self.extract_features()
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        risk_probability = self.model.predict_proba(features_scaled)[0][1]
        risk_class = self.model.predict(features_scaled)[0]
        
        # Determine risk level
        if risk_probability < 0.3:
            risk_level = "Low"
            risk_color = "green"
        elif risk_probability < 0.6:
            risk_level = "Moderate"
            risk_color = "orange"
        else:
            risk_level = "High"
            risk_color = "red"
        
        return {
            'risk_probability': round(float(risk_probability), 3),
            'risk_percentage': round(float(risk_probability) * 100, 1),
            'risk_class': int(risk_class),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'features': {
                'delivery_ratio': float(features[0][0]),
                'volatility': float(features[0][1]),
                'anomaly_count': int(features[0][2]),
                'budget_breach_count': int(features[0][3])
            }
        }
    
    def get_risk_factors(self):
        """Identify primary risk factors"""
        features = self.extract_features()[0]
        risk_factors = []
        
        # Check each feature against thresholds
        if features[0] > 0.25:  # Delivery ratio
            risk_factors.append({
                'factor': 'High Delivery Spending',
                'value': f"{features[0]*100:.1f}%",
                'severity': 'High' if features[0] > 0.4 else 'Moderate'
            })
        
        if features[1] > 300:  # Volatility
            risk_factors.append({
                'factor': 'Spending Volatility',
                'value': f"₹{features[1]:.0f}",
                'severity': 'High' if features[1] > 500 else 'Moderate'
            })
        
        if features[2] > 3:  # Anomaly count
            risk_factors.append({
                'factor': 'Unusual Transactions',
                'value': f"{int(features[2])} anomalies",
                'severity': 'High' if features[2] > 6 else 'Moderate'
            })
        
        if features[3] > 1:  # Budget breaches
            risk_factors.append({
                'factor': 'Budget Breaches',
                'value': f"{int(features[3])} incidents",
                'severity': 'High' if features[3] > 3 else 'Moderate'
            })
        
        return risk_factors
    
    def get_recommendations(self):
        """Generate recommendations based on risk factors"""
        risk_factors = self.get_risk_factors()
        recommendations = []
        
        if not risk_factors:
            recommendations.append("✅ Keep up the excellent spending habits!")
            return recommendations
        
        for factor in risk_factors:
            if 'Delivery' in factor['factor']:
                recommendations.append("🍕 Reduce food delivery orders by cooking at home more often")
            elif 'Volatility' in factor['factor']:
                recommendations.append("📊 Create a monthly budget and stick to it for consistency")
            elif 'Unusual' in factor['factor']:
                recommendations.append("🔍 Review large or unusual transactions to ensure they're necessary")
            elif 'Budget' in factor['factor']:
                recommendations.append("💰 Set spending alerts to avoid exceeding your budget")
        
        # Add general recommendations
        recommendations.append("📱 Enable transaction notifications for better awareness")
        recommendations.append("🎯 Set specific savings goals to stay motivated")
        
        return recommendations
