"""
Behavior Engine
Generates personalized behavioral nudges based on spending patterns
"""

import random
from datetime import datetime
from database.db import execute_query
from config import NUDGE_TEMPLATES, NUDGE_TONES
from modules.analytics import FinancialAnalytics
from modules.health_score import HealthScoreEngine


class BehaviorEngine:
    """Generate personalized behavioral nudges"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.analytics = FinancialAnalytics(user_id)
        self.health_engine = HealthScoreEngine(user_id)
    
    def generate_nudge(self, nudge_type='auto'):
        """
        Generate behavioral nudge based on spending patterns
        
        Args:
            nudge_type: 'auto', 'high_delivery', 'late_night', 'improvement', 'warning'
        
        Returns:
            dict with nudge text and tone
        """
        if nudge_type == 'auto':
            nudge_type = self._determine_nudge_type()
        
        # Get appropriate template
        templates = NUDGE_TEMPLATES.get(nudge_type, NUDGE_TEMPLATES['improvement'])
        nudge_text = random.choice(templates)
        
        # Personalize nudge with data
        nudge_text = self._personalize_nudge(nudge_text, nudge_type)
        
        # Determine tone
        tone = self._determine_tone(nudge_type)
        
        # Save nudge to database
        self._save_nudge(nudge_text, tone)
        
        return {
            'text': nudge_text,
            'tone': tone,
            'type': nudge_type
        }
    
    def _determine_nudge_type(self):
        """Automatically determine appropriate nudge type"""
        delivery_metrics = self.analytics.get_delivery_metrics()
        weekly_comparison = self.analytics.get_weekly_comparison()
        health_score = self.health_engine.calculate_health_score()
        
        # Check for improvement
        previous_score = self.health_engine.get_previous_score()
        if previous_score and previous_score['change'] > 5:
            return 'improvement'
        
        # Check for high delivery spending
        if delivery_metrics['delivery_percentage'] > 25:
            return 'high_delivery'
        
        # Check for increasing trend
        if weekly_comparison['change_percentage'] > 20:
            return 'warning'
        
        # Check for late night orders
        late_night = self.analytics.detect_late_night_orders()
        if late_night and len(late_night) > 2:
            return 'late_night'
        
        # Default to improvement/motivational
        return 'improvement'
    
    def _personalize_nudge(self, nudge_text, nudge_type):
        """Insert personalized data into nudge template"""
        delivery_metrics = self.analytics.get_delivery_metrics()
        weekly_comparison = self.analytics.get_weekly_comparison()
        
        # Replace placeholders
        nudge_text = nudge_text.replace(
            '{percent}', 
            f"{delivery_metrics['delivery_percentage']:.1f}"
        )
        
        nudge_text = nudge_text.replace(
            '{points}',
            f"{abs(weekly_comparison['change_percentage']):.0f}"
        )
        
        return nudge_text
    
    def _determine_tone(self, nudge_type):
        """Determine appropriate tone for nudge"""
        tone_map = {
            'high_delivery': 'warning',
            'late_night': 'informative',
            'improvement': 'encouraging',
            'warning': 'warning'
        }
        return tone_map.get(nudge_type, 'motivational')
    
    def _save_nudge(self, nudge_text, tone):
        """Save nudge to database"""
        query = """
            INSERT INTO nudges (user_id, nudge_text, tone)
            VALUES (?, ?, ?)
        """
        execute_query(query, (self.user_id, nudge_text, tone))
    
    def get_recent_nudges(self, limit=5):
        """Get recent nudges for user"""
        query = """
            SELECT nudge_text, tone, created_at
            FROM nudges
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """
        results = execute_query(query, (self.user_id, limit), fetch_all=True)
        return [dict(row) for row in results] if results else []
    
    def generate_multiple_nudges(self, count=3):
        """Generate multiple diverse nudges"""
        nudge_types = ['high_delivery', 'improvement', 'warning', 'late_night']
        nudges = []
        
        for _ in range(count):
            nudge_type = random.choice(nudge_types)
            nudge = self.generate_nudge(nudge_type)
            nudges.append(nudge)
        
        return nudges
    
    def get_daily_tip(self):
        """Get daily financial tip"""
        tips = [
            "💡 Track every expense, no matter how small. Awareness is the first step to better finances.",
            "🎯 Set a specific savings goal for this month. You'll be more motivated to stick to your budget.",
            "📅 Review your spending every Sunday. Weekly check-ins prevent monthly surprises.",
            "🍳 Meal prep on weekends to reduce impulse food delivery orders during the week.",
            "💳 Use cash for discretionary spending. It creates a psychological barrier to overspending.",
            "📊 The 50/30/20 rule: 50% needs, 30% wants, 20% savings. Balance is key!",
            "⏰ Wait 24 hours before making non-essential purchases. Impulse fades, savings grow.",
            "🎁 Find free or low-cost entertainment options. Your wallet will thank you!",
            "📱 Unsubscribe from promotional emails. Out of sight, out of cart!",
            "💪 Challenge yourself: one no-spend day per week. Make it a game!"
        ]
        return random.choice(tips)
    
    def generate_summary_insights(self):
        """Generate comprehensive behavioral insights"""
        delivery_metrics = self.analytics.get_delivery_metrics()
        weekly_comparison = self.analytics.get_weekly_comparison()
        health_score = self.health_engine.calculate_health_score()
        
        insights = []
        
        # Delivery insight
        if delivery_metrics['delivery_percentage'] > 20:
            insights.append({
                'category': 'Delivery Spending',
                'message': f"Food delivery represents {delivery_metrics['delivery_percentage']:.1f}% of your spending",
                'action': 'Consider cooking at home more often',
                'severity': 'high' if delivery_metrics['delivery_percentage'] > 30 else 'medium'
            })
        
        # Trend insight
        if abs(weekly_comparison['change_percentage']) > 15:
            direction = 'increased' if weekly_comparison['change_percentage'] > 0 else 'decreased'
            insights.append({
                'category': 'Spending Trend',
                'message': f"Your spending {direction} by {abs(weekly_comparison['change_percentage']):.1f}% this week",
                'action': 'Review your recent transactions' if direction == 'increased' else 'Great job maintaining discipline!',
                'severity': 'medium' if direction == 'increased' else 'low'
            })
        
        # Health score insight
        if health_score['final_score'] < 60:
            insights.append({
                'category': 'Financial Health',
                'message': f"Your health score is {health_score['final_score']:.1f} - {health_score['status']}",
                'action': 'Focus on reducing variable expenses and increasing consistency',
                'severity': 'high'
            })
        
        return insights
