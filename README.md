# AI Behavioral Finance Coach 🏦

A production-ready, full-stack AI-powered financial coaching application built with Streamlit. This hackathon project provides comprehensive financial health monitoring, behavioral insights, ML-based predictions, and personalized coaching through an intelligent chatbot interface.

## 🌟 Features

### Core Functionality
- **🔐 User Authentication**: Secure login/registration system with bcrypt password hashing
- **💾 Persistent Storage**: SQLite database for storing users, transactions, metrics, and nudges
- **💬 AI Chatbot**: Rule-based conversational interface for natural interaction
- **📊 Financial Health Score**: Comprehensive 0-100 scoring system with component breakdown
- **🔮 ML Predictions**: Logistic regression model for overspending risk prediction
- **🔍 Anomaly Detection**: Statistical Z-score based anomaly detection
- **📄 PDF Reports**: Professional downloadable financial health reports

### Transaction Input Methods
1. **📤 CSV Upload**: Bulk import transactions from CSV files
2. **📧 Gmail Sync**: Automatic delivery order parsing (Swiggy, Zomato, Uber Eats)
3. **✍️ Manual Entry**: Form-based transaction input with date picker
4. **🎲 Simulation**: Generate random transactions for testing

### Analytics & Insights
- Category-wise spending breakdown
- Delivery spending analysis and comparison
- Spending volatility calculation
- Weekly trend comparison
- Late-night order detection
- Future spending projection
- Historical score comparison

### Behavioral Coaching
- Personalized behavioral nudges
- AI-generated insights
- Daily financial tips
- Risk factor identification
- Actionable recommendations

## 🏗️ Architecture

```
ai_finance_coach/
│
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration and constants
├── requirements.txt                # Python dependencies
│
├── database/
│   ├── db.py                       # Database operations
│   ├── schema.sql                  # Database schema
│   └── finance_coach.db            # SQLite database (auto-generated)
│
├── modules/
│   ├── auth.py                     # Authentication & session management
│   ├── transaction_manager.py     # Transaction CRUD operations
│   ├── analytics.py               # Financial analytics engine
│   ├── anomaly.py                 # Anomaly detection algorithms
│   ├── health_score.py            # Health score calculation
│   ├── prediction.py              # ML prediction model
│   ├── behavior_engine.py         # Behavioral nudge generation
│   ├── chatbot.py                 # Conversational interface
│   ├── email_parser.py            # Gmail order parsing
│   └── report_generator.py        # PDF report generation
│
└── models/
    └── overspend_model.pkl         # Trained ML model (auto-generated)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone/Download the Project
```bash
cd ai_finance_coach
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 👤 Demo Account

For quick testing, use the pre-created demo account:

- **Email**: `demo@financecoach.ai`
- **Password**: `demo123`

## 📖 User Guide

### Getting Started

1. **Login/Register**
   - Use the demo account or create a new account
   - Password must be at least 6 characters
   - Email must be unique

2. **Add Transactions**
   - Navigate to "Transactions" page
   - Choose from 4 input methods:
     - Upload CSV file
     - Simulate Gmail sync
     - Add manually with date and category
     - Generate random simulation

3. **View Dashboard**
   - See your financial health score
   - Monitor overspending risk
   - View spending breakdown
   - Track trends over time

4. **Chat with AI**
   - Ask questions like "What's my score?"
   - Request insights: "Show my delivery spending"
   - Get summaries: "Give me an overview"
   - Detect anomalies: "Show unusual transactions"

5. **Analyze Insights**
   - View detailed analytics
   - Explore anomaly detection
   - Check ML predictions
   - Compare delivery patterns

6. **Generate Reports**
   - Download PDF financial health report
   - Export transactions as CSV
   - Share with financial advisors

## 📊 Financial Health Score

The health score (0-100) is calculated based on:

### Components (Weighted)
- **Delivery Ratio (30%)**: Lower delivery spending = better score
- **Volatility (25%)**: Consistent spending = better score
- **Anomaly Frequency (25%)**: Fewer anomalies = better score
- **Overspending Control (20%)**: Less overspending = better score

### Score Grades
- **90-100**: A+ Excellent
- **80-89**: A Good
- **70-79**: B Fair
- **60-69**: C Needs Improvement
- **50-59**: D Poor
- **0-49**: F Critical

## 🤖 ML Prediction Model

### Algorithm
- **Model**: Logistic Regression
- **Purpose**: Predict overspending risk probability
- **Features**:
  1. Delivery spending ratio
  2. Spending volatility
  3. Anomaly count
  4. Budget breach count

### Risk Levels
- **Low**: < 30% probability
- **Moderate**: 30-60% probability
- **High**: > 60% probability

## 🔍 Anomaly Detection

Uses **Z-score statistical method** to identify:

1. **Amount Anomalies**: Transactions significantly above/below average
2. **Category Anomalies**: Unusual spending within categories
3. **Frequency Anomalies**: Days with unusual transaction counts
4. **Overspending Periods**: Spending above 120% of average

**Threshold**: Z-score > 2.0 (configurable in `config.py`)

## 📧 Gmail Integration (Optional)

### Setup Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project and enable Gmail API
3. Download `credentials.json`
4. Place in project root
5. Install: `pip install google-api-python-client google-auth-oauthlib`

### Supported Services
- Swiggy
- Zomato
- Uber Eats
- Dunzo

**Demo Mode**: Use "Simulate Gmail Sync" for testing without API setup

## 💾 Database Schema

### Tables

**users**
- user_id (PK)
- name, email (UNIQUE), password_hash
- created_at

**transactions**
- transaction_id (PK)
- user_id (FK), date, category, amount, source, description
- created_at

**metrics**
- metric_id (PK)
- user_id (FK), health_score, overspend_risk, volatility
- delivery_ratio, anomaly_count
- calculated_at

**nudges**
- nudge_id (PK)
- user_id (FK), nudge_text, tone
- created_at

## ⚙️ Configuration

Edit `config.py` to customize:

- Categories
- Risk thresholds
- Health score weights
- ML model parameters
- Nudge templates
- UI theme

## 🎨 UI Pages

1. **🏠 Dashboard**: Overview with key metrics and charts
2. **💬 Chat Assistant**: Conversational AI interface
3. **💰 Transactions**: Add and manage transactions
4. **📊 Insights**: Detailed analytics and predictions
5. **📄 Reports**: Generate and download reports

## 🔒 Security Features

- Bcrypt password hashing (cost factor: 12)
- Session-based authentication
- User data isolation (queries filtered by user_id)
- SQL injection prevention (parameterized queries)
- Duplicate transaction prevention

## 🧪 Testing

### Quick Test Workflow
1. Login with demo account
2. Click "Simulate Transaction" 5-10 times
3. View dashboard to see score calculation
4. Chat: "What's my score?"
5. Navigate to Insights → Predictions
6. Generate PDF report

### CSV Test File
```csv
date,category,amount,description
2024-02-20,Food Delivery,450.00,Swiggy Order
2024-02-21,Groceries,1200.50,Monthly groceries
2024-02-22,Transportation,300.00,Uber ride
```

## 📈 Performance Optimizations

- SQLite with proper indexing
- Cached ML model loading
- Duplicate prevention on insert
- Efficient DataFrame operations
- Lazy loading of analytics modules

## 🐛 Troubleshooting

### Issue: Database not found
**Solution**: The database is auto-created on first run. Delete `finance_coach.db` and restart.

### Issue: Import errors
**Solution**: Ensure all requirements are installed: `pip install -r requirements.txt`

### Issue: Score shows 0
**Solution**: Add at least 3-5 transactions for meaningful calculations

### Issue: Gmail sync not working
**Solution**: Use "Simulate Gmail Sync" for demo, or setup Gmail API as per instructions

## 🎯 Future Enhancements

- Real-time Gmail API integration
- Budget setting and tracking
- Goal-based savings plans
- Multi-currency support
- Mobile responsive design
- Email/SMS notifications
- Bank account integration
- Investment tracking
- Tax planning insights

## 📝 License

This is a hackathon project built for educational purposes.

## 👨‍💻 Author

Built with ❤️ for the hackathon

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- scikit-learn for ML capabilities
- ReportLab for PDF generation
- The open-source community

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the user guide
3. Examine the code documentation

---

**Happy Coaching! 🚀**
