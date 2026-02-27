"""
Configuration file for Real-time Budget Nudge Agent
Contains all global settings and constants
"""

# Application Settings
APP_NAME = "Real-time Budget Nudge Agent"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Your intelligent companion for real-time budget monitoring and spending insights"

# Database Configuration
DATABASE_NAME = "finance_coach.db"

# Transaction Categories
CATEGORIES = [
    "Food Delivery",
    "Groceries",
    "Transportation",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Shopping",
    "Education",
    "Investment",
    "Other"
]

# Transaction Sources
SOURCES = {
    "CSV": "csv_upload",
    "GMAIL": "gmail_sync",
    "MANUAL": "manual_entry",
    "SIMULATION": "simulation"
}

# Health Score Weights
HEALTH_SCORE_WEIGHTS = {
    "delivery_ratio": 0.3,      # 30% weight
    "volatility": 0.25,          # 25% weight
    "anomaly_frequency": 0.25,   # 25% weight
    "overspending": 0.2          # 20% weight
}

# Risk Thresholds
RISK_THRESHOLDS = {
    "high_delivery_ratio": 0.25,     # >25% of spending on delivery
    "high_volatility": 0.4,          # High std deviation
    "anomaly_zscore": 2.0,           # Z-score threshold for anomalies
    "overspend_threshold": 1.2       # 120% of average spending
}

# ML Model Settings
ML_MODEL_PATH = "models/overspend_model.pkl"
ML_FEATURES = ["delivery_ratio", "volatility", "anomaly_count", "budget_breach_count"]

# Email Parser Settings
DELIVERY_SERVICES = ["swiggy", "zomato", "uber eats", "dunzo"]
EMAIL_AMOUNT_PATTERNS = [
    r'₹\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
    r'INR\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
    r'Rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)'
]

# Chatbot Intents
CHATBOT_INTENTS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
    "score": ["score", "health", "financial health", "how am i doing"],
    "risk": ["risk", "overspend", "prediction", "forecast"],
    "add_transaction": ["add", "record", "expense", "spent", "bought"],
    "summary": ["summary", "overview", "stats", "statistics", "show me"],
    "help": ["help", "what can you do", "commands", "options"],
    "delivery": ["delivery", "swiggy", "zomato", "food orders"],
    "anomaly": ["anomaly", "unusual", "suspicious", "outlier"]
}

# Behavioral Nudge Templates
NUDGE_TONES = ["encouraging", "warning", "informative", "motivational"]

NUDGE_TEMPLATES = {
    "high_delivery": [
        "🍕 Your delivery spending is higher than usual. Consider cooking at home 2x this week!",
        "💡 Delivery orders make up {percent}% of your spending. Small changes can save big!",
        "🎯 Challenge: Reduce delivery orders by 20% this month. You can do it!"
    ],
    "late_night": [
        "🌙 Late-night orders detected. Planning meals ahead could save money and improve health!",
        "⏰ Midnight cravings adding up? Set a food ordering cutoff time!"
    ],
    "improvement": [
        "🎉 Great job! Your financial health score improved by {points} points!",
        "📈 You're on track! Keep up the good spending habits!",
        "💪 Excellent progress! Your spending discipline is showing results!"
    ],
    "warning": [
        "⚠️ Overspending risk detected. Review your budget this week.",
        "📊 Your spending volatility is high. Try to maintain consistency.",
        "🔔 Alert: You're {percent}% over your average spending this period."
    ]
}

# Report Settings
REPORT_TITLE = "Financial Health Report"
REPORT_SUBTITLE = "AI-Generated Behavioral Finance Analysis"

# UI Settings
UI_THEME = {
    "primary_color": "#1f77b4",
    "background_color": "#ffffff",
    "secondary_background_color": "#f0f2f6",
    "text_color": "#262730",
    "font": "sans-serif"
}

# Page Configuration
PAGES = {
    "home": "🏠 Dashboard",
    "chat": "💬 Chat Assistant",
    "transactions": "💰 Transactions",
    "insights": "📊 Insights",
    "reports": "📄 Reports"
}

# Session State Keys
SESSION_KEYS = {
    "user_id": "user_id",
    "user_name": "user_name",
    "user_email": "user_email",
    "logged_in": "logged_in",
    "current_page": "current_page"
}
