"""
Chatbot Module
Rule-based conversational interface for transaction management and insights
"""

import re
from datetime import datetime
from config import CHATBOT_INTENTS, CATEGORIES
from modules.transaction_manager import TransactionManager
from modules.health_score import HealthScoreEngine
from modules.prediction import OverspendPredictor
from modules.analytics import FinancialAnalytics
from modules.behavior_engine import BehaviorEngine
from modules.anomaly import AnomalyDetector


class FinanceChatbot:
    """Rule-based chatbot for finance coaching"""
    
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name
        self.transaction_manager = TransactionManager(user_id)
        self.health_engine = HealthScoreEngine(user_id)
        self.predictor = OverspendPredictor(user_id)
        self.analytics = FinancialAnalytics(user_id)
        self.behavior_engine = BehaviorEngine(user_id)
        self.anomaly_detector = AnomalyDetector(user_id)
    
    def process_message(self, user_message):
        """
        Process user message and generate response
        
        Args:
            user_message: User's text input
        
        Returns:
            dict with response text and metadata
        """
        user_message = user_message.lower().strip()
        
        # Detect intent
        intent = self._detect_intent(user_message)
        
        # Route to appropriate handler
        if intent == 'greeting':
            return self._handle_greeting()
        elif intent == 'score':
            return self._handle_score_query()
        elif intent == 'risk':
            return self._handle_risk_query()
        elif intent == 'add_transaction':
            return self._handle_add_transaction_intent(user_message)
        elif intent == 'summary':
            return self._handle_summary()
        elif intent == 'delivery':
            return self._handle_delivery_query()
        elif intent == 'anomaly':
            return self._handle_anomaly_query()
        elif intent == 'help':
            return self._handle_help()
        else:
            return self._handle_unknown()
    
    def _detect_intent(self, message):
        """Detect user intent from message"""
        for intent, keywords in CHATBOT_INTENTS.items():
            for keyword in keywords:
                if keyword in message:
                    return intent
        return 'unknown'
    
    def _handle_greeting(self):
        """Handle greeting intent"""
        greetings = [
            f"Hello {self.user_name}! 👋 How can I help you manage your finances today?",
            f"Hi {self.user_name}! Ready to check your financial health?",
            f"Hey {self.user_name}! What would you like to know about your spending?"
        ]
        import random
        return {
            'response': random.choice(greetings),
            'intent': 'greeting',
            'actions': ['show_menu']
        }
    
    def _handle_score_query(self):
        """Handle health score query"""
        score_data = self.health_engine.calculate_health_score()
        
        response = f"""
📊 **Your Financial Health Score**

**Score: {score_data['final_score']:.1f}/100** - {score_data['grade']}
**Status: {score_data['status']}**

**Component Breakdown:**
• Delivery Ratio: {score_data['components']['delivery_ratio']['score']:.1f}/100
• Volatility: {score_data['components']['volatility']['score']:.1f}/100
• Anomaly Frequency: {score_data['components']['anomaly_frequency']['score']:.1f}/100
• Overspending Control: {score_data['components']['overspending']['score']:.1f}/100

"""
        
        # Add comparison if available
        previous = self.health_engine.get_previous_score()
        if previous:
            change = previous['change']
            if change > 0:
                response += f"📈 Your score improved by {change:.1f} points! Keep it up! 🎉"
            elif change < 0:
                response += f"📉 Your score decreased by {abs(change):.1f} points. Let's work on improvement!"
            else:
                response += "➡️ Your score remained stable."
        
        return {
            'response': response,
            'intent': 'score',
            'data': score_data
        }
    
    def _handle_risk_query(self):
        """Handle overspending risk query"""
        risk_data = self.predictor.predict_overspend_risk()
        risk_factors = self.predictor.get_risk_factors()
        recommendations = self.predictor.get_recommendations()
        
        response = f"""
🔮 **Overspending Risk Analysis**

**Risk Level: {risk_data['risk_level']}**
**Probability: {risk_data['risk_percentage']:.1f}%**

"""
        
        if risk_factors:
            response += "**Risk Factors:**\n"
            for factor in risk_factors:
                response += f"• {factor['factor']}: {factor['value']} ({factor['severity']} severity)\n"
            response += "\n"
        
        response += "**Recommendations:**\n"
        for rec in recommendations[:3]:
            response += f"• {rec}\n"
        
        return {
            'response': response,
            'intent': 'risk',
            'data': risk_data
        }
    
    def _handle_add_transaction_intent(self, message):
        """Handle add transaction intent"""
        # Try to extract amount from message
        amount_match = re.search(r'₹?\s*(\d+(?:,\d+)*(?:\.\d{2})?)', message)
        
        if amount_match:
            amount = float(amount_match.group(1).replace(',', ''))
            response = f"To add a transaction of ₹{amount}, please use the 'Transactions' page and fill in the complete details (date, category, etc.)."
        else:
            response = "To add a transaction, please visit the 'Transactions' page where you can:\n• Upload CSV\n• Add manually with date and category\n• Simulate a transaction\n• Sync from Gmail"
        
        return {
            'response': response,
            'intent': 'add_transaction',
            'actions': ['navigate_to_transactions']
        }
    
    def _handle_summary(self):
        """Handle summary query"""
        stats = self.transaction_manager.get_transaction_stats()
        delivery_metrics = self.analytics.get_delivery_metrics()
        weekly_comp = self.analytics.get_weekly_comparison()
        
        response = f"""
📈 **Financial Summary**

**Overall Statistics:**
• Total Transactions: {stats['total_transactions']}
• Total Spent: ₹{stats['total_spent']:,.2f}
• Average Transaction: ₹{stats['avg_transaction']:,.2f}

**Delivery Insights:**
• Delivery Orders: {delivery_metrics['delivery_count']}
• Delivery Spending: ₹{delivery_metrics['delivery_total']:,.2f}
• % of Total: {delivery_metrics['delivery_percentage']:.1f}%

**Weekly Trend:**
• This Week: ₹{weekly_comp['current_week']:,.2f}
• Last Week: ₹{weekly_comp['previous_week']:,.2f}
• Change: {weekly_comp['change_percentage']:.1f}% ({weekly_comp['trend']})
"""
        
        return {
            'response': response,
            'intent': 'summary',
            'data': stats
        }
    
    def _handle_delivery_query(self):
        """Handle delivery-specific query"""
        delivery_metrics = self.analytics.get_delivery_metrics()
        late_night = self.analytics.detect_late_night_orders()
        
        response = f"""
🍕 **Food Delivery Analysis**

**Spending Metrics:**
• Total Delivery Spending: ₹{delivery_metrics['delivery_total']:,.2f}
• Number of Orders: {delivery_metrics['delivery_count']}
• Average Order Value: ₹{delivery_metrics['avg_delivery_order']:,.2f}
• % of Total Spending: {delivery_metrics['delivery_percentage']:.1f}%

"""
        
        if delivery_metrics['delivery_percentage'] > 25:
            response += "⚠️ **Alert:** Delivery spending is above recommended threshold (25%)\n\n"
            response += "**Suggestion:** Try cooking at home 2-3 times per week to reduce this percentage."
        elif delivery_metrics['delivery_percentage'] > 15:
            response += "💡 **Tip:** Your delivery spending is moderate. Consider meal planning to optimize further."
        else:
            response += "✅ **Great job!** Your delivery spending is well-controlled."
        
        if late_night:
            response += f"\n\n🌙 Detected {len(late_night)} late-night orders. Planning ahead can help reduce these!"
        
        return {
            'response': response,
            'intent': 'delivery',
            'data': delivery_metrics
        }
    
    def _handle_anomaly_query(self):
        """Handle anomaly query"""
        anomalies = self.anomaly_detector.detect_amount_anomalies()
        
        response = "🔍 **Anomaly Detection**\n\n"
        
        if not anomalies:
            response += "✅ No unusual transactions detected. Your spending patterns look normal!"
        else:
            response += f"Found {len(anomalies)} unusual transaction(s):\n\n"
            for i, anomaly in enumerate(anomalies[:3], 1):
                response += f"{i}. ₹{anomaly['amount']:,.2f} on {anomaly['date']} ({anomaly['category']})\n"
                response += f"   {anomaly['deviation']}\n\n"
            
            if len(anomalies) > 3:
                response += f"... and {len(anomalies) - 3} more.\n\n"
            
            response += "💡 Review these transactions to ensure they're intentional."
        
        return {
            'response': response,
            'intent': 'anomaly',
            'data': anomalies
        }
    
    def _handle_help(self):
        """Handle help query"""
        response = """
🤖 **I can help you with:**

**Financial Insights:**
• "What's my score?" - Check your financial health score
• "Show me my risk" - Analyze overspending risk
• "Give me a summary" - View spending overview
• "Check my delivery spending" - Delivery order analysis

**Anomaly Detection:**
• "Show anomalies" - Detect unusual transactions

**Tips & Nudges:**
• "Give me a tip" - Get financial advice
• Just chat with me for personalized insights!

**Transaction Management:**
Visit the 'Transactions' page to add expenses via CSV, Gmail, or manual entry.
"""
        
        return {
            'response': response,
            'intent': 'help'
        }
    
    def _handle_unknown(self):
        """Handle unknown intent"""
        tip = self.behavior_engine.get_daily_tip()
        
        response = f"I'm not sure I understood that. {tip}\n\nType 'help' to see what I can do!"
        
        return {
            'response': response,
            'intent': 'unknown'
        }
