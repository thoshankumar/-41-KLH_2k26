# 🚀 Quick Start Guide

## AI Behavioral Finance Coach

### Installation (2 minutes)

1. **Open Terminal/Command Prompt**
   ```bash
   cd ai_finance_coach
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Access in Browser**
   - Automatically opens at: `http://localhost:8501`
   - Or manually navigate to that URL

### First Time Login

**Demo Account (Pre-configured)**
- Email: `demo@financecoach.ai`
- Password: `demo123`

**OR Create New Account**
- Click "Register" tab
- Enter name, email, password
- Click "Create Account"
- Login with your credentials

### Quick Demo (5 minutes)

#### Step 1: Add Sample Data
1. Go to **Transactions** page
2. Click **"Simulation"** tab
3. Click **"Generate Random Delivery Order"** button 10 times
4. You'll see success messages for each transaction

**OR Upload Sample CSV:**
1. Go to **Transactions** page
2. Click **"CSV Upload"** tab
3. Upload `sample_transactions.csv`
4. Click **"Import CSV"**

#### Step 2: View Dashboard
1. Navigate to **Dashboard** page
2. See your:
   - Financial Health Score
   - Risk Level
   - Total Spending
   - Delivery Percentage
3. Scroll down for charts and insights

#### Step 3: Chat with AI
1. Go to **Chat Assistant** page
2. Try these commands:
   - "What's my score?"
   - "Show my risk"
   - "Give me a summary"
   - "Check my delivery spending"
   - "Show anomalies"

#### Step 4: Explore Insights
1. Visit **Insights** page
2. Check each tab:
   - **Analytics**: Spending trends and patterns
   - **Anomalies**: Unusual transactions
   - **Predictions**: ML-based risk analysis
   - **Delivery Analysis**: Food delivery insights

#### Step 5: Generate Report
1. Go to **Reports** page
2. Click **"Generate PDF Report"**
3. Wait for processing (5-10 seconds)
4. Click **"Download PDF Report"**
5. Open the PDF to see comprehensive analysis

### Key Features to Try

#### 1. Transaction Management
- **CSV Upload**: Use `sample_transactions.csv`
- **Manual Entry**: Add individual transactions
- **Simulation**: Generate random orders
- **Gmail Sync**: Test with simulated data

#### 2. Financial Health Score
- Calculated from 4 components
- Ranges from 0-100
- Updates with each transaction
- Shows historical comparison

#### 3. Chatbot Features
Quick commands:
- `score` → View health score
- `risk` → Check overspending risk
- `summary` → Get overview
- `delivery` → Delivery analysis
- `help` → See all commands

#### 4. ML Predictions
- Overspending probability
- Risk factors identification
- Personalized recommendations
- Feature importance analysis

#### 5. Anomaly Detection
- Z-score based detection
- Category-wise analysis
- Overspending alerts
- Unusual pattern identification

### Navigation Guide

```
📍 Sidebar Navigation
├── 🏠 Dashboard       → Overview and metrics
├── 💬 Chat Assistant  → AI chatbot
├── 💰 Transactions    → Add/manage transactions
├── 📊 Insights        → Analytics and predictions
└── 📄 Reports         → Download reports
```

### Understanding Your Score

**Health Score Components:**
- **Delivery Ratio (30%)**: Lower is better
- **Volatility (25%)**: Lower is better
- **Anomaly Frequency (25%)**: Lower is better
- **Overspending (20%)**: Lower is better

**Score Interpretation:**
- **90-100**: Excellent financial health
- **80-89**: Good, minor improvements needed
- **70-79**: Fair, some attention required
- **60-69**: Needs improvement
- **Below 60**: Critical, immediate action needed

### Tips for Best Results

1. **Add Diverse Transactions**: Mix categories for better insights
2. **Use Real Dates**: Spread transactions across multiple days
3. **Consistent Usage**: Add transactions regularly
4. **Check Dashboard Daily**: Monitor score changes
5. **Follow Recommendations**: Act on AI suggestions

### Sample Chat Conversations

**Example 1: Check Score**
```
You: What's my financial health score?
AI: [Shows detailed breakdown with 82.5/100]
```

**Example 2: Risk Analysis**
```
You: Am I at risk of overspending?
AI: [Shows risk level, probability, and factors]
```

**Example 3: Get Summary**
```
You: Give me a summary of my spending
AI: [Shows transactions, categories, and trends]
```

### Troubleshooting

**App won't start?**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Database issues?**
- Delete `database/finance_coach.db`
- Restart the app (auto-recreates)

**No data showing?**
- Add at least 3-5 transactions
- Refresh the page

**Score shows 0?**
- Add more transactions (minimum 3)
- Wait for calculation
- Refresh dashboard

### Advanced Features

#### CSV Format
```csv
date,category,amount,description
2024-02-20,Food Delivery,450.00,Swiggy Order
2024-02-21,Groceries,1200.50,Monthly groceries
```

#### Available Categories
- Food Delivery
- Groceries
- Transportation
- Entertainment
- Utilities
- Healthcare
- Shopping
- Education
- Investment
- Other

#### Transaction Sources
- `csv_upload`: Imported from CSV
- `gmail_sync`: Synced from Gmail
- `manual_entry`: Added manually
- `simulation`: Generated for testing

### Next Steps

1. **Customize Settings**: Edit `config.py` for thresholds
2. **Add Real Data**: Import your actual transactions
3. **Set Goals**: Use insights to create budgets
4. **Track Progress**: Monitor score improvements
5. **Generate Reports**: Regular PDF reports for review

### Getting Help

- Check `README.md` for detailed documentation
- Review code comments in Python files
- Examine sample data in `sample_transactions.csv`

---

## 🎉 You're Ready!

Start by adding transactions and exploring the dashboard. The more data you add, the better the insights become!

**Happy Coaching! 🚀**
