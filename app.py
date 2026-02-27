"""
AI Behavioral Finance Coach - Main Streamlit Application
A production-ready financial health coaching application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sqlite3

# Import modules
from modules.auth import (
    initialize_session, is_logged_in, render_login_page, 
    logout, get_current_user_id, get_current_user_name, get_current_user_email
)
from modules.transaction_manager import TransactionManager
from modules.analytics import FinancialAnalytics
from modules.anomaly import AnomalyDetector
from modules.health_score import HealthScoreEngine
from modules.prediction import OverspendPredictor
from modules.behavior_engine import BehaviorEngine
from modules.chatbot import FinanceChatbot
from modules.email_parser import EmailParser
from modules.report_generator import ReportGenerator
from config import APP_NAME, CATEGORIES, PAGES

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open("custom_styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Landing Page CSS
with open("landing_page.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Login Page CSS
with open("login_page.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session
initialize_session()

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

def render_landing_page():
    """Render professional landing page"""
    
    # Animated Floating Lines Background
    st.markdown("""
    <div class="floating-lines-bg">
        <div class="floating-line line-1"></div>
        <div class="floating-line line-2"></div>
        <div class="floating-line line-3"></div>
        <div class="floating-line line-4"></div>
        <div class="floating-line line-5"></div>
        <div class="floating-line line-6"></div>
        <div class="floating-line line-7"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login button in top right corner
    st.markdown("""
    <div class="login-btn-container">
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([5, 1, 1])
    with col3:
        if st.button("🔐 Login", key="top_login_btn", use_container_width=True, type="primary"):
            st.session_state.show_login = True
            st.rerun()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">�️ Real-time Budget Nudge Agent</div>
        <div class="hero-subtitle">Your Intelligent Companion for Smarter Financial Decisions</div>
        <p style="font-size:1.1rem; opacity:0.9; max-width:700px; margin:0 auto;">
            Harness the power of AI to understand your spending behavior, detect anomalies, 
            and receive personalized financial insights to achieve your goals.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Grid
    st.markdown('<h2 style="text-align:center; color:#ffffff; margin:3rem 0 2rem; text-shadow: 0 2px 8px rgba(0,0,0,0.5);">✨ Powerful Features</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💯</div>
            <div class="feature-title">Health Score</div>
            <div class="feature-description">
                Real-time financial health scoring (0-100) based on spending patterns, 
                delivery habits, and anomaly detection.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Chatbot</div>
            <div class="feature-description">
                Conversational AI assistant that answers questions about your finances, 
                provides tips, and offers personalized recommendations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔮</div>
            <div class="feature-title">ML Predictions</div>
            <div class="feature-description">
                Machine learning models predict overspending risks and identify 
                behavioral patterns before they become problems.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Analytics Dashboard</div>
            <div class="feature-description">
                Interactive visualizations with category breakdowns, spending trends, 
                and historical comparisons powered by Plotly.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚨</div>
            <div class="feature-title">Anomaly Detection</div>
            <div class="feature-description">
                Statistical Z-score analysis identifies unusual spending patterns 
                and alerts you to potential budget issues.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📧</div>
            <div class="feature-title">Multi-Input Methods</div>
            <div class="feature-description">
                Import transactions via CSV, Gmail sync, manual entry, or 
                AI-powered simulation for quick testing.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div class="stats-section">
        <h2 style="color:#ffffff; margin-bottom:1rem; text-shadow: 0 2px 8px rgba(0,0,0,0.5);">📈 Platform Capabilities</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">10+</div>
                <div class="stat-label">Transaction Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">Real-time Analysis</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">4</div>
                <div class="stat-label">Input Methods</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">AI</div>
                <div class="stat-label">Powered Insights</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown('<h2 style="text-align:center; color:#ffffff; margin:3rem 0 2rem; text-shadow: 0 2px 8px rgba(0,0,0,0.5);">🛠️ Built With Modern Technology</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align:center; padding:1rem;">
            <h3 style="color:#ffffff;">🎨 Streamlit</h3>
            <p style="color:rgba(255,255,255,0.8);">Interactive UI Framework</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:1rem;">
            <h3 style="color:#ffffff;">🧠 Scikit-Learn</h3>
            <p style="color:rgba(255,255,255,0.8);">ML Models & Predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align:center; padding:1rem;">
            <h3 style="color:#ffffff;">📊 Plotly</h3>
            <p style="color:rgba(255,255,255,0.8);">Interactive Charts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align:center; padding:1rem;">
            <h3 style="color:#ffffff;">🗄️ SQLite</h3>
            <p style="color:rgba(255,255,255,0.8);">Persistent Storage</p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="cta-section">
        <h2 style="color:#ffffff; margin-bottom:2rem; text-shadow: 0 2px 8px rgba(0,0,0,0.5);">Ready to Transform Your Financial Life?</h2>
        <p style="font-size:1.2rem; color:rgba(255,255,255,0.9); margin-bottom:2rem;">
            Join today and start making smarter financial decisions with AI-powered insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 Get Started", key="cta_btn", use_container_width=True, type="primary"):
            st.session_state.show_login = True
            st.rerun()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding:2rem; color:#888; border-top:1px solid #ddd; margin-top:3rem;">
        <p>© 2026 Real-time Budget Nudge Agent | Built with ❤️ using Streamlit & Python</p>
        <p style="font-size:0.9rem;">🔒 Your data is secure | 🎯 Personalized insights | 🚀 Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown(f"### 🏦 {APP_NAME}")
        st.markdown("---")
        
        if is_logged_in():
            # Clickable profile section
            if 'show_profile' not in st.session_state:
                st.session_state.show_profile = False
            
            # Get profile picture for sidebar
            from database.db import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            user_id = get_current_user_id()
            
            try:
                cursor.execute("SELECT profile_picture FROM users WHERE user_id = ?", (user_id,))
                result = cursor.fetchone()
                sidebar_profile_pic = result[0] if result else None
            except:
                sidebar_profile_pic = None
            conn.close()
            
            # Enhanced profile card with picture
            st.markdown("""
            <style>
            .sidebar-profile-card {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 16px;
                padding: 1rem;
                margin-bottom: 1rem;
                transition: all 0.3s ease;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            .sidebar-profile-card:hover {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%);
                border-color: rgba(102, 126, 234, 0.6);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
            .sidebar-avatar {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                flex-shrink: 0;
                border: 2px solid rgba(255, 255, 255, 0.3);
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            }
            .sidebar-profile-info {
                flex: 1;
                overflow: hidden;
            }
            .sidebar-profile-name {
                font-weight: 700;
                font-size: 0.95rem;
                color: white;
                margin-bottom: 0.2rem;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .sidebar-profile-email {
                font-size: 0.75rem;
                color: rgba(255, 255, 255, 0.7);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Profile card HTML
            if sidebar_profile_pic:
                avatar_html = f'<div class="sidebar-avatar" style="background-image: url(\'{sidebar_profile_pic}\'); background-size: cover; background-position: center; font-size: 0;"></div>'
            else:
                avatar_html = '<div class="sidebar-avatar">👤</div>'
            
            st.markdown(f"""
            <div class="sidebar-profile-card" title="Click to view/edit your profile">
                {avatar_html}
                <div class="sidebar-profile-info">
                    <div class="sidebar-profile-name">{get_current_user_name()}</div>
                    <div class="sidebar-profile-email">{get_current_user_email()}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden button for functionality
            profile_clicked = st.button(
                "View Profile",
                use_container_width=True,
                key="profile_button",
                type="secondary"
            )
            
            if profile_clicked:
                st.session_state.show_profile = True
                st.rerun()
            
            st.markdown("---")
            
            # Enhanced Navigation Section
            st.markdown("""
            <style>
            /* Navigation Header */
            .nav-header {
                font-size: 1.1rem;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea 0%, #f5576c 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            /* Hide default Streamlit radio styling */
            div[data-testid="stRadio"] > label {
                display: none;
            }
            
            /* Custom Radio Button Container */
            div[data-testid="stRadio"] > div {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }
            
            /* Individual Radio Options */
            div[data-testid="stRadio"] > div > label {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 0.8rem 1rem;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                display: flex;
                align-items: center;
                gap: 0.8rem;
                position: relative;
                overflow: hidden;
            }
            
            /* Hover Effect */
            div[data-testid="stRadio"] > div > label:hover {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-color: rgba(102, 126, 234, 0.4);
                transform: translateX(5px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
            }
            
            /* Active/Selected State */
            div[data-testid="stRadio"] > div > label:has(input:checked) {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.2) 100%);
                border: 2px solid rgba(102, 126, 234, 0.6);
                box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
                transform: translateX(5px);
            }
            
            /* Hide default radio circle */
            div[data-testid="stRadio"] input[type="radio"] {
                display: none;
            }
            
            /* Custom Radio Indicator */
            div[data-testid="stRadio"] > div > label::before {
                content: '';
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transition: all 0.3s ease;
            }
            
            div[data-testid="stRadio"] > div > label:has(input:checked)::before {
                background: linear-gradient(135deg, #667eea 0%, #f5576c 100%);
                box-shadow: 0 0 10px rgba(102, 126, 234, 0.6);
                animation: pulse 2s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.2); opacity: 0.8; }
            }
            
            /* Navigation Text Styling */
            div[data-testid="stRadio"] > div > label > div {
                font-weight: 600;
                font-size: 0.95rem;
                color: rgba(255, 255, 255, 0.8);
                transition: color 0.3s ease;
            }
            
            div[data-testid="stRadio"] > div > label:hover > div {
                color: rgba(255, 255, 255, 0.95);
            }
            
            div[data-testid="stRadio"] > div > label:has(input:checked) > div {
                color: white;
                font-weight: 700;
            }
            
            /* Shimmer Effect on Hover */
            div[data-testid="stRadio"] > div > label::after {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                transition: left 0.5s ease;
            }
            
            div[data-testid="stRadio"] > div > label:hover::after {
                left: 100%;
            }
            </style>
            
            <div class="nav-header">
                <span style="font-size: 1.3rem;">📍</span>
                <span>Navigation</span>
            </div>
            """, unsafe_allow_html=True)
            
            page = st.radio(
                "Go to:",
                [
                    "🏠 Dashboard",
                    "💬 Chat Assistant", 
                    "💳 Transactions",
                    "📊 Insights",
                    "📄 Reports"
                ],
                label_visibility="collapsed"
            )
            
            # Strip emoji for page name
            page_name = page.split(" ", 1)[1] if " " in page else page
            
            # Reset profile flag when navigating to other pages
            if st.session_state.get('page_selection') != page_name:
                st.session_state.show_profile = False
            st.session_state.page_selection = page_name
            
            st.markdown("---")
            
            # Enhanced Logout Button
            st.markdown("""
            <style>
            /* Custom Logout Button Styling */
            div.stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
                border: 2px solid rgba(255, 107, 107, 0.3);
                border-radius: 12px;
                padding: 0.8rem 1rem;
                font-weight: 700;
                color: white;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
            }
            
            div.stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #ff5252 0%, #e63946 100%);
                border-color: rgba(255, 107, 107, 0.6);
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5);
            }
            
            div.stButton > button[kind="primary"]:active {
                transform: translateY(0);
                box-shadow: 0 2px 8px rgba(255, 107, 107, 0.4);
            }
            </style>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True, type="primary"):
                logout()
                st.rerun()
            
            return page_name
        else:
            st.info("Please login to continue")
            return None


def render_dashboard():
    """Render main dashboard"""
    user_id = get_current_user_id()
    user_name = get_current_user_name()
    
    st.markdown(f'<div class="main-header">🏠 Welcome, {user_name}!</div>', unsafe_allow_html=True)
    
    # Initialize modules
    health_engine = HealthScoreEngine(user_id)
    predictor = OverspendPredictor(user_id)
    analytics = FinancialAnalytics(user_id)
    behavior_engine = BehaviorEngine(user_id)
    
    # Calculate metrics
    score_data = health_engine.calculate_health_score()
    risk_data = predictor.predict_overspend_risk()
    stats = analytics.get_summary_stats()
    delivery_metrics = analytics.get_delivery_metrics()
    
    # Save metrics to database
    health_engine.save_metrics()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💯 Health Score",
            f"{score_data['final_score']:.1f}/100",
            delta=None,
            help="Your overall financial health score"
        )
    
    with col2:
        st.metric(
            "⚠️ Risk Level",
            risk_data['risk_level'],
            delta=f"{risk_data['risk_percentage']:.1f}%",
            delta_color="inverse",
            help="Overspending risk assessment"
        )
    
    with col3:
        st.metric(
            "💰 Total Spent",
            f"₹{stats['total_spent']:,.0f}",
            delta=None,
            help="Total spending across all transactions"
        )
    
    with col4:
        st.metric(
            "🍕 Delivery %",
            f"{delivery_metrics['delivery_percentage']:.1f}%",
            delta=None,
            delta_color="inverse" if delivery_metrics['delivery_percentage'] > 25 else "normal",
            help="Percentage of spending on delivery"
        )
    
    st.markdown("---")
    
    # Score breakdown and insights
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📊 Health Score Breakdown")
        
        # Component scores
        components = score_data['components']
        component_df = pd.DataFrame([
            {"Component": "Delivery Ratio", "Score": components['delivery_ratio']['score']},
            {"Component": "Volatility", "Score": components['volatility']['score']},
            {"Component": "Anomaly Frequency", "Score": components['anomaly_frequency']['score']},
            {"Component": "Overspending Control", "Score": components['overspending']['score']}
        ])
        
        fig = px.bar(
            component_df,
            x="Component",
            y="Score",
            color="Score",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[0, 100],
            title="Component Scores"
        )
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Historical comparison
        previous_score = health_engine.get_previous_score()
        if previous_score:
            change = previous_score['change']
            if change > 0:
                st.success(f"📈 Your score improved by {change:.1f} points since last calculation!")
            elif change < 0:
                st.warning(f"📉 Your score decreased by {abs(change):.1f} points. Let's work on improvement!")
            else:
                st.info("➡️ Your score remained stable since last calculation.")
    
    with col_right:
        st.subheader("💡 Quick Insights")
        
        insights = behavior_engine.generate_summary_insights()
        
        if insights:
            for insight in insights[:3]:
                if insight['severity'] == 'high':
                    st.error(f"**{insight['category']}**\n\n{insight['message']}\n\n✅ {insight['action']}")
                elif insight['severity'] == 'medium':
                    st.warning(f"**{insight['category']}**\n\n{insight['message']}\n\n✅ {insight['action']}")
                else:
                    st.info(f"**{insight['category']}**\n\n{insight['message']}\n\n✅ {insight['action']}")
        else:
            st.success("✅ Everything looks good! Keep up the great work!")
        
        # Daily tip
        tip = behavior_engine.get_daily_tip()
        st.info(tip)
    
    st.markdown("---")
    
    # Category breakdown and spending trend
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📂 Spending by Category")
        category_breakdown = analytics.get_category_breakdown()
        
        if not category_breakdown.empty:
            fig_pie = px.pie(
                values=category_breakdown['Total'],
                names=category_breakdown.index,
                title="Category Distribution"
            )
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No transactions yet. Add some to see insights!")
    
    with col2:
        st.subheader("📈 Spending Trend")
        trend_df = analytics.get_spending_trend()
        
        if not trend_df.empty:
            fig_line = px.line(
                trend_df,
                x="Date",
                y="Amount",
                title="Daily Spending Over Time"
            )
            fig_line.update_layout(height=300)
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Not enough data for trend analysis yet.")


def render_chat_assistant():
    """Render chatbot interface"""
    user_id = get_current_user_id()
    user_name = get_current_user_name()
    
    st.markdown('<div class="main-header">💬 Chat Assistant</div>', unsafe_allow_html=True)
    st.caption("Your AI-powered finance coach. Ask me anything!")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = FinanceChatbot(user_id, user_name)
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": f"Hello {user_name}! 👋 I'm your AI finance coach. How can I help you today?"}
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about your finances..."):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = st.session_state.chatbot.process_message(prompt)
                response = response_data['response']
                st.markdown(response)
        
        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Sidebar with quick actions
    with st.sidebar:
        st.markdown("### 🎯 Quick Commands")
        
        if st.button("What's my score?", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "What's my score?"})
            st.rerun()
        
        if st.button("Show my risk", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Show my risk"})
            st.rerun()
        
        if st.button("Give me a summary", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Give me a summary"})
            st.rerun()
        
        if st.button("Check delivery spending", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": "Check my delivery spending"})
            st.rerun()
        
        if st.button("Clear chat", use_container_width=True):
            st.session_state.chat_history = [
                {"role": "assistant", "content": f"Chat cleared! How can I help you, {user_name}?"}
            ]
            st.rerun()


def render_transactions():
    """Render transactions page"""
    user_id = get_current_user_id()
    
    st.markdown('<div class="main-header">💰 Transaction Management</div>', unsafe_allow_html=True)
    
    # Initialize transaction manager
    tm = TransactionManager(user_id)
    
    # Tabs for different input methods
    tab1, tab2, tab3, tab4 = st.tabs(["📤 CSV Upload", "📧 Gmail Sync", "✍️ Manual Entry", "🎲 Simulation"])
    
    with tab1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; color: white;">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.5rem;">📤 Upload Transactions from CSV</h3>
            <p style="margin: 0; opacity: 0.9;">Import multiple transactions at once from a CSV file</p>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader with enhanced styling
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <p style="color: #2a5298; font-weight: 600; margin-bottom: 0.5rem;">📋 CSV Format Requirements:</p>
            <p style="color: #555; margin: 0; font-size: 0.95rem;">
                Your CSV must include: <strong>date</strong>, <strong>category</strong>, <strong>amount</strong>, and <strong>description</strong> (optional)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=['csv'],
            help="Upload a CSV file with your transactions",
            key="csv_uploader"
        )
        
        if uploaded_file is not None:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                        padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <p style="margin: 0; color: #2a5298; font-weight: 600;">✅ File Ready: {}</p>
            </div>
            """.format(uploaded_file.name), unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🚀 Import CSV", type="primary", use_container_width=True):
                    with st.spinner("Importing transactions..."):
                        success_count, error_count, message = tm.import_csv(uploaded_file)
                        if success_count > 0:
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)
        
        # Sample CSV format
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📋 View Sample CSV Format"):
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <p style="color: #666; margin: 0;">Download or copy this format for your CSV file:</p>
            </div>
            """, unsafe_allow_html=True)
            
            sample_df = pd.DataFrame({
                'date': ['2024-02-20', '2024-02-21'],
                'category': ['Food Delivery', 'Groceries'],
                'amount': [450.00, 1200.50],
                'description': ['Swiggy Order', 'Monthly groceries']
            })
            st.dataframe(sample_df, use_container_width=True)
    
    with tab2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 1.5rem 2rem; border-radius: 15px; margin-bottom: 1.5rem; color: white;">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.5rem;">📧 Gmail Sync</h3>
            <p style="margin: 0; opacity: 0.9;">Automatically import delivery orders from your email</p>
        </div>
        """, unsafe_allow_html=True)
        
        email_parser = EmailParser(user_id)
        
        col1, col2 = st.columns([3, 2], gap="small")
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                        padding: 2.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📬</div>
                <h4 style="color: #2a5298; margin-bottom: 1rem; font-size: 1.3rem;">Gmail Integration</h4>
                <p style="color: #555; margin-bottom: 1.5rem; line-height: 1.7; font-size: 1.05rem;">
                    Click the button below to import delivery orders from Swiggy, Zomato, Uber Eats, and Dunzo.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("🔄 Simulate Gmail Sync", type="primary", use_container_width=True):
                    with st.spinner("Syncing emails..."):
                        success_count, skipped_count, message = email_parser.simulate_gmail_sync()
                        if success_count > 0:
                            st.success(f"✅ {message}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.warning(f"⚠️ {message}")
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fbda61 0%, #f5a524 100%);
                        padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h4 style="color: #5a3e2f; margin: 0 0 1rem 0; font-size: 1.1rem;">✨ Supported Services</h4>
                <ul style="color: #5a3e2f; margin: 0; padding-left: 1.5rem; line-height: 2; font-size: 1.05rem;">
                    <li>🍕 Swiggy</li>
                    <li>🍔 Zomato</li>
                    <li>🚗 Uber Eats</li>
                    <li>📦 Dunzo</li>
                    <li>🥗 Amazon Fresh</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; color: white;">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.5rem;">✍️ Add Transaction Manually</h3>
            <p style="margin: 0; opacity: 0.9;">Enter transaction details one at a time</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                    padding: 2rem; border-radius: 12px;">
        """, unsafe_allow_html=True)
        
        with st.form("manual_transaction_form", clear_on_submit=True):
            st.markdown("<h4 style='color: #2a5298; margin-bottom: 1.5rem;'>📝 Transaction Details</h4>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<p style='font-weight: 600; color: #555; margin-bottom: 0.5rem;'>📅 Transaction Date</p>", unsafe_allow_html=True)
                date = st.date_input("Date", value=datetime.now(), label_visibility="collapsed")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<p style='font-weight: 600; color: #555; margin-bottom: 0.5rem;'>🏷️ Category</p>", unsafe_allow_html=True)
                category = st.selectbox("Category", CATEGORIES, label_visibility="collapsed")
            
            with col2:
                st.markdown("<p style='font-weight: 600; color: #555; margin-bottom: 0.5rem;'>💰 Amount (₹)</p>", unsafe_allow_html=True)
                amount = st.number_input("Amount", min_value=0.0, step=10.0, label_visibility="collapsed")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<p style='font-weight: 600; color: #555; margin-bottom: 0.5rem;'>📝 Description</p>", unsafe_allow_html=True)
                description = st.text_input("Description", placeholder="e.g., Swiggy Order, Gas Bill", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submitted = st.form_submit_button("➕ Add Transaction", type="primary", use_container_width=True)
            
            if submitted:
                if amount > 0:
                    success = tm.add_manual_transaction(date, category, amount, description)
                    if success:
                        st.success("✅ Transaction added successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("⚠️ Transaction already exists (duplicate detected)")
                else:
                    st.error("💡 Amount must be greater than 0")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; color: white;">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.5rem;">🎲 Simulate Transaction</h3>
            <p style="margin: 0; opacity: 0.9;">Generate random transactions for testing and demos</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                        padding: 3rem 2rem; border-radius: 12px; text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎲</div>
                <h4 style="color: #2a5298; margin-bottom: 1rem;">Random Transaction Generator</h4>
                <p style="color: #555; margin-bottom: 2rem; line-height: 1.6;">
                    Generate realistic delivery orders with random amounts, dates, and descriptions.
                    Perfect for testing and demonstrations.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🎯 Generate Random Transaction", type="primary", use_container_width=True):
                with st.spinner("Creating transaction..."):
                    success, message = tm.simulate_transaction()
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.warning(message)
            
            st.markdown("""
            <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; margin-top: 1.5rem;
                        border-left: 4px solid #ffc107;">
                <p style="margin: 0; color: #856404; font-size: 0.9rem;">
                    💡 <strong>Tip:</strong> Click multiple times to generate several transactions at once!
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display transactions
    st.subheader("📋 Your Transactions")
    
    transactions_df = tm.get_all_transactions()
    
    if not transactions_df.empty:
        # Enhanced Stats Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 16px; margin-bottom: 2rem; 
                    box-shadow: 0 8px 25px rgba(102,126,234,0.3);">
            <h3 style="color: white; margin: 0 0 1rem 0; font-size: 1.5rem;">
                📊 Transaction Statistics
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        stats = tm.get_transaction_stats()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 2.5rem; font-weight: 800; color: #2a5298;">
                    {count}
                </div>
                <div style="font-size: 1rem; color: #555; font-weight: 600; margin-top: 0.5rem;">
                    📋 Total Transactions
                </div>
            </div>
            """.format(count=stats['total_transactions']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fbda61 0%, #f5a524 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 2.5rem; font-weight: 800; color: #5a3e2f;">
                    ₹{amount:,.0f}
                </div>
                <div style="font-size: 1rem; color: #5a3e2f; font-weight: 600; margin-top: 0.5rem;">
                    💰 Total Spent
                </div>
            </div>
            """.format(amount=stats['total_spent']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #a6c1ee 0%, #fbc2eb 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="font-size: 2.5rem; font-weight: 800; color: #5a3e7d;">
                    ₹{avg:,.0f}
                </div>
                <div style="font-size: 1rem; color: #5a3e7d; font-weight: 600; margin-top: 0.5rem;">
                    📊 Average Transaction
                </div>
            </div>
            """.format(avg=stats['avg_transaction']), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced Filters Section with Professional Design
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem 2rem; border-radius: 15px; margin-bottom: 1.5rem; 
                    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem;">🔍</div>
                <div>
                    <h3 style="margin: 0; color: white; font-size: 1.5rem; font-weight: 700;">Filter Transactions</h3>
                    <p style="margin: 0.3rem 0 0 0; color: rgba(255,255,255,0.85); font-size: 0.95rem;">
                        Refine your view by category or source
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Filters with enhanced card design
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #2a2a40 0%, #1a1a2e 100%); 
                        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;
                        border: 1px solid rgba(102, 126, 234, 0.3);">
                <p style="color: #e0eafc; font-weight: 600; margin: 0 0 0.8rem 0; font-size: 1rem;">
                    📂 Filter by Category
                </p>
            </div>
            """, unsafe_allow_html=True)
            categories = ['All'] + list(transactions_df['category'].unique())
            selected_category = st.selectbox(
                "Category", 
                categories, 
                key="cat_filter",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #2a2a40 0%, #1a1a2e 100%); 
                        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;
                        border: 1px solid rgba(102, 126, 234, 0.3);">
                <p style="color: #e0eafc; font-weight: 600; margin: 0 0 0.8rem 0; font-size: 1rem;">
                    🔗 Filter by Source
                </p>
            </div>
            """, unsafe_allow_html=True)
            sources = ['All'] + list(transactions_df['source'].unique())
            # Create icons for source dropdown
            source_map = {
                'csv_upload': '📤 CSV Upload',
                'gmail_sync': '📧 Gmail Sync',
                'manual_entry': '✍️ Manual Entry',
                'simulation': '🎲 Simulation'
            }
            source_options = ['All'] + [source_map.get(s, s) for s in sources if s != 'All']
            selected_source_display = st.selectbox(
                "Source",
                source_options,
                label_visibility="collapsed"
            )
            
            # Map back to actual source value
            if selected_source_display == 'All':
                selected_source = 'All'
            else:
                reverse_map = {v: k for k, v in source_map.items()}
                selected_source = reverse_map.get(selected_source_display, selected_source_display)
        
        # Apply filters
        filtered_df = transactions_df.copy()
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        if selected_source != 'All':
            filtered_df = filtered_df[filtered_df['source'] == selected_source]
        
        # Enhanced transaction display
        st.markdown(f"""
        <div class="transaction-header">
            <h3>📋 All Transactions ({len(filtered_df)})</h3>
            <p>View and manage your financial transactions</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Category icon and color mapping
        def get_category_info(category):
            category_icons = {
                'Food Delivery': '🍕',
                'Groceries': '🛒',
                'Transportation': '🚗',
                'Entertainment': '🎬',
                'Utilities': '⚡',
                'Healthcare': '🏥',
                'Shopping': '🛍️',
                'Education': '📚',
                'Investment': '💰',
                'Other': '📌'
            }
            category_class = {
                'Food Delivery': 'category-food',
                'Groceries': 'category-groceries',
                'Transportation': 'category-transportation',
                'Entertainment': 'category-entertainment',
                'Utilities': 'category-utilities',
                'Healthcare': 'category-healthcare',
                'Shopping': 'category-shopping',
                'Education': 'category-education',
                'Investment': 'category-investment',
                'Other': 'category-other'
            }
            icon = category_icons.get(category, '📌')
            css_class = category_class.get(category, 'category-other')
            return f'<span class="category-badge {css_class}">{icon} {category}</span>'
        
        # Source badge with enhanced styling
        def render_source_badge(source):
            color_map = {
                'csv_upload': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'gmail_sync': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                'manual_entry': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                'simulation': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
            }
            label_map = {
                'csv_upload': '📤 CSV',
                'gmail_sync': '📧 Gmail',
                'manual_entry': '✍️ Manual',
                'simulation': '🎲 Sim'
            }
            gradient = color_map.get(source, 'linear-gradient(135deg, #888 0%, #666 100%)')
            label = label_map.get(source, source)
            return f'<span class="source-badge" style="background:{gradient}">{label}</span>'

        # Create styled table
        def create_enhanced_table(df):
            html = '<div class="transaction-container"><table>'
            
            # Header
            html += '<thead><tr>'
            html += '<th>📅 Date</th>'
            html += '<th>📝 Description</th>'
            html += '<th>🏷️ Category</th>'
            html += '<th>🔗 Source</th>'
            html += '<th>💵 Amount</th>'
            html += '</tr></thead>'
            
            # Body
            html += '<tbody>'
            for _, row in df.iterrows():
                html += '<tr>'
                html += f'<td><strong>{row["date"]}</strong></td>'
                html += f'<td>{row["description"]}</td>'
                html += f'<td>{get_category_info(row["category"])}</td>'
                html += f'<td>{render_source_badge(row["source"])}</td>'
                html += f'<td><strong>₹{row["amount"]:,.0f}</strong></td>'
                html += '</tr>'
            html += '</tbody></table></div>'
            return html
        
        st.markdown(create_enhanced_table(filtered_df[['date', 'description', 'category', 'source', 'amount']]), unsafe_allow_html=True)
        
        # Export Section - Download filtered transactions
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Prepare download filename based on filters
        filename = "transactions"
        if selected_category != 'All':
            filename += f"_{selected_category.lower().replace(' ', '_')}"
        if selected_source != 'All':
            filename += f"_{selected_source}"
        filename += ".csv"
        
        # Convert filtered dataframe to CSV
        csv_data = filtered_df.to_csv(index=False)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.download_button(
                f"📥 Download ({len(filtered_df)} rows)",
                csv_data,
                filename,
                "text/csv",
                key='download-csv',
                use_container_width=True,
                type="primary"
            )
        
        # Show filter info
        if selected_category != 'All' or selected_source != 'All':
            filter_info = []
            if selected_category != 'All':
                filter_info.append(f"Category: {selected_category}")
            if selected_source != 'All':
                source_display = source_map.get(selected_source, selected_source)
                filter_info.append(f"Source: {source_display}")
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%); 
                        padding: 0.8rem 1.5rem; border-radius: 10px; text-align: center; margin-top: 1rem;
                        border-left: 4px solid #5cb85c;">
                <p style="margin: 0; color: #2d5016; font-weight: 600;">
                    ✅ Filtered by: {' • '.join(filter_info)}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); 
                    padding: 3rem; border-radius: 16px; text-align: center; margin: 2rem 0;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #2a5298; margin-bottom: 1rem;">No Transactions Yet</h3>
            <p style="color: #666; font-size: 1.1rem;">
                Get started by adding your first transaction using the tabs above!
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_insights():
    """Render insights and analytics page"""
    user_id = get_current_user_id()
    
    # Enhanced page header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2.5rem 2rem; border-radius: 20px; margin-bottom: 2rem;
                box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);">
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <div style="font-size: 3.5rem;">📊</div>
            <div>
                <h1 style="margin: 0; color: white; font-size: 2.5rem; font-weight: 800;">Financial Insights</h1>
                <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 1.1rem;">
                    Deep dive into your spending patterns and predictions
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize modules
    analytics = FinancialAnalytics(user_id)
    anomaly_detector = AnomalyDetector(user_id)
    predictor = OverspendPredictor(user_id)
    
    if analytics.transactions_df.empty:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                    padding: 4rem 2rem; border-radius: 16px; text-align: center; margin: 3rem 0;">
            <div style="font-size: 5rem; margin-bottom: 1.5rem;">📊</div>
            <h3 style="color: #2a5298; margin-bottom: 1rem; font-size: 1.8rem;">No Data Available</h3>
            <p style="color: #666; font-size: 1.2rem;">
                Add some transactions to unlock powerful insights!
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Enhanced Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Analytics", "🔍 Anomalies", "🔮 Predictions", "🍕 Delivery Analysis"])
    
    with tab1:
        # Enhanced Analytics Header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    padding: 1.5rem 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <h3 style="margin: 0; color: white; font-size: 1.8rem; font-weight: 700;">💰 Financial Analytics</h3>
            <p style="margin: 0.3rem 0 0 0; color: rgba(255,255,255,0.9);">Key metrics and spending patterns</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced Summary stats with gradient cards
        stats = analytics.get_summary_stats()
        
        col1, col2, col3, col4 = st.columns(4, gap="small")
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 6px 20px rgba(102,126,234,0.3);">
                <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0 0 0.5rem 0; font-weight: 600;">Total Spent</p>
                <h2 style="color: white; margin: 0; font-size: 2rem; font-weight: 800;">₹{stats['total_spent']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 6px 20px rgba(240,147,251,0.3);">
                <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0 0 0.5rem 0; font-weight: 600;">Avg per Transaction</p>
                <h2 style="color: white; margin: 0; font-size: 2rem; font-weight: 800;">₹{stats['average_transaction']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                        padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 6px 20px rgba(79,172,254,0.3);">
                <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0 0 0.5rem 0; font-weight: 600;">Median Transaction</p>
                <h2 style="color: white; margin: 0; font-size: 2rem; font-weight: 800;">₹{stats['median_transaction']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                        padding: 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 6px 20px rgba(250,112,154,0.3);">
                <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0 0 0.5rem 0; font-weight: 600;">Volatility</p>
                <h2 style="color: white; margin: 0; font-size: 2rem; font-weight: 800;">₹{analytics.calculate_volatility():,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Enhanced Charts Section
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="color: #2a5298; margin: 0;">📊 Category Breakdown</h4>
            </div>
            """, unsafe_allow_html=True)
            
            category_breakdown = analytics.get_category_breakdown()
            
            fig = px.bar(
                category_breakdown.reset_index(),
                x='category',
                y='Total',
                color='Total',
                title="Spending by Category",
                color_continuous_scale=['#667eea', '#764ba2']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, color='#2a5298'),
                title_font=dict(size=16, color='#2a5298', family='Arial Black')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="color: #2a5298; margin: 0;">📈 Weekly Comparison</h4>
            </div>
            """, unsafe_allow_html=True)
            
            weekly_comp = analytics.get_weekly_comparison()
            
            week_df = pd.DataFrame({
                'Week': ['Previous Week', 'Current Week'],
                'Amount': [weekly_comp['previous_week'], weekly_comp['current_week']]
            })
            
            fig = px.bar(
                week_df,
                x='Week',
                y='Amount',
                color='Week',
                title=f"Trend: {weekly_comp['trend'].title()}",
                color_discrete_sequence=['#667eea', '#4facfe']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, color='#2a5298'),
                title_font=dict(size=16, color='#2a5298', family='Arial Black')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Enhanced Spending Trend
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;">
            <h4 style="color: white; margin: 0;">📉 Spending Trend Over Time</h4>
        </div>
        """, unsafe_allow_html=True)
        
        trend_df = analytics.get_spending_trend()
        
        fig = px.line(
            trend_df,
            x='Date',
            y='Amount',
            title="Daily Spending",
            line_shape='spline'
        )
        fig.update_traces(line=dict(color='#667eea', width=3))
        fig.add_hline(
            y=trend_df['Amount'].mean(), 
            line_dash="dash",
            annotation_text="Average", 
            line_color="#f5576c",
            line_width=2
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#2a5298'),
            title_font=dict(size=16, color='#2a5298', family='Arial Black'),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # New Advanced Analytics Section
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Weekly Spending Pattern & Monthly Trend
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;
                        box-shadow: 0 6px 20px rgba(102,126,234,0.25);">
                <h4 style="color: white; margin: 0;">📊 Weekly Spending Pattern</h4>
            </div>
            """, unsafe_allow_html=True)
            
            weekly_pattern = analytics.get_weekly_spending_pattern()
            
            if not weekly_pattern.empty:
                # Highlight max day
                max_amount = weekly_pattern['Amount'].max()
                colors = ['#1abc9c' if amt == max_amount else '#95a5a6' for amt in weekly_pattern['Amount']]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=weekly_pattern['DayOfWeek'],
                        y=weekly_pattern['Amount'],
                        marker=dict(
                            color=colors,
                            line=dict(color='#2c3e50', width=1)
                        ),
                        text=[f'₹{amt:,.0f}' for amt in weekly_pattern['Amount']],
                        textposition='outside',
                        hovertemplate='<b>%{x}</b><br>Spending: ₹%{y:,.0f}<extra></extra>'
                    )
                ])
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    font=dict(size=11, color='#2a5298', family='Arial'),
                    xaxis=dict(
                        title='',
                        showgrid=False,
                        zeroline=False
                    ),
                    yaxis=dict(
                        title='Amount (₹)',
                        showgrid=True,
                        gridcolor='rgba(0,0,0,0.05)',
                        zeroline=False
                    ),
                    margin=dict(t=10, b=40, l=50, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show max day info
                max_day = weekly_pattern.loc[weekly_pattern['Amount'] == max_amount, 'DayOfWeek'].iloc[0]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
                            padding: 0.8rem 1.2rem; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; color: #2d5016; font-weight: 600;">
                        🎯 Peak Day: <strong>{max_day}</strong> (₹{max_amount:,.0f})
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Not enough data for weekly pattern analysis")
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;
                        box-shadow: 0 6px 20px rgba(79,172,254,0.25);">
                <h4 style="color: white; margin: 0;">📈 Monthly Trend & Projection</h4>
            </div>
            """, unsafe_allow_html=True)
            
            monthly_trend = analytics.get_monthly_trend_with_projection()
            
            if not monthly_trend.empty:
                actual_data = monthly_trend[monthly_trend['Type'] == 'Actual']
                projected_data = monthly_trend[monthly_trend['Type'] == 'Projected']
                
                fig = go.Figure()
                
                # Actual spending line
                fig.add_trace(go.Scatter(
                    x=actual_data['Week'],
                    y=actual_data['Amount'],
                    mode='lines+markers',
                    name='Actual',
                    line=dict(color='#1abc9c', width=3),
                    marker=dict(size=8, color='#1abc9c'),
                    hovertemplate='<b>Week %{x}</b><br>Amount: ₹%{y:,.0f}<extra></extra>'
                ))
                
                # Projected spending line
                if not projected_data.empty:
                    # Connect last actual to first projection
                    connection_df = pd.concat([
                        actual_data.tail(1),
                        projected_data.head(1)
                    ])
                    
                    fig.add_trace(go.Scatter(
                        x=connection_df['Week'],
                        y=connection_df['Amount'],
                        mode='lines',
                        name='',
                        line=dict(color='#95a5a6', width=2, dash='dot'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=projected_data['Week'],
                        y=projected_data['Amount'],
                        mode='lines+markers',
                        name='Projected',
                        line=dict(color='#95a5a6', width=3, dash='dash'),
                        marker=dict(size=8, color='#95a5a6', symbol='diamond'),
                        hovertemplate='<b>Week %{x}</b><br>Projected: ₹%{y:,.0f}<extra></extra>'
                    ))
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    font=dict(size=11, color='#2a5298', family='Arial'),
                    xaxis=dict(
                        title='Week',
                        showgrid=True,
                        gridcolor='rgba(0,0,0,0.05)',
                        zeroline=False
                    ),
                    yaxis=dict(
                        title='Amount (₹)',
                        showgrid=True,
                        gridcolor='rgba(0,0,0,0.05)',
                        zeroline=False
                    ),
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=1.02,
                        xanchor='right',
                        x=1
                    ),
                    margin=dict(t=40, b=40, l=50, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data for trend projection")
        
        # Budget vs Actual Spending
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                    padding: 1.2rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;
                    box-shadow: 0 6px 20px rgba(250,112,154,0.25);">
            <h4 style="color: white; margin: 0;">💰 Budget vs Actual Spending</h4>
        </div>
        """, unsafe_allow_html=True)
        
        budget_comparison = analytics.get_budget_comparison()
        
        if not budget_comparison.empty:
            for _, row in budget_comparison.iterrows():
                category = row['Category']
                actual = row['Actual']
                budget = row['Budget']
                percentage = row['Percentage']
                
                # Determine color based on percentage
                if percentage > 100:
                    bar_color = '#e74c3c'  # Red for over budget
                    bg_gradient = 'linear-gradient(135deg, #fee 0%, #fdd 100%)'
                    border_color = '#e74c3c'
                elif percentage > 80:
                    bar_color = '#f39c12'  # Orange for near budget
                    bg_gradient = 'linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%)'
                    border_color = '#f39c12'
                else:
                    bar_color = '#1abc9c'  # Green for under budget
                    bg_gradient = 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)'
                    border_color = '#1abc9c'
                
                st.markdown(f"""
                <div style="background: {bg_gradient}; padding: 1.2rem 1.5rem; border-radius: 10px; 
                            margin-bottom: 1rem; border-left: 4px solid {border_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <h5 style="margin: 0; color: #2c3e50; font-size: 1.1rem; font-weight: 600;">{category}</h5>
                        <div style="text-align: right;">
                            <span style="color: #2c3e50; font-weight: 700; font-size: 1.1rem;">₹{actual:,.0f}</span>
                            <span style="color: #7f8c8d; font-size: 0.9rem;"> / ₹{budget:,.0f}</span>
                            <span style="color: {bar_color}; font-weight: 700; font-size: 1.1rem; margin-left: 1rem;">{percentage:.0f}%</span>
                        </div>
                    </div>
                    <div style="background: #ecf0f1; height: 12px; border-radius: 6px; overflow: hidden;">
                        <div style="background: {bar_color}; height: 100%; width: {min(percentage, 100)}%; 
                                    border-radius: 6px; transition: width 0.5s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Summary stats
            total_budget = budget_comparison['Budget'].sum()
            total_actual = budget_comparison['Actual'].sum()
            overall_percentage = (total_actual / total_budget * 100) if total_budget > 0 else 0
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1.5rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 4px 15px rgba(102,126,234,0.3);">
                    <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0 0 0.5rem 0;">Total Budget</p>
                    <h3 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 800;">₹{total_budget:,.0f}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                            padding: 1.5rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 4px 15px rgba(79,172,254,0.3);">
                    <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0 0 0.5rem 0;">Total Spent</p>
                    <h3 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 800;">₹{total_actual:,.0f}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                overall_color = '#e74c3c' if overall_percentage > 100 else '#1abc9c'
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                            padding: 1.5rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 4px 15px rgba(250,112,154,0.3);">
                    <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0 0 0.5rem 0;">Overall Usage</p>
                    <h3 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 800;">{overall_percentage:.0f}%</h3>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📊 Add more transactions to see budget comparison")
    
    with tab2:
        # Enhanced Anomaly Detection Header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 1.5rem 2rem; border-radius: 15px; margin-bottom: 1.5rem;">
            <h3 style="margin: 0; color: white; font-size: 1.8rem; font-weight: 700;">🔍 Anomaly Detection</h3>
            <p style="margin: 0.3rem 0 0 0; color: rgba(255,255,255,0.9);">Unusual spending patterns and outliers</p>
        </div>
        """, unsafe_allow_html=True)
        
        # How It Works Section
        with st.expander("📖 How Anomaly Detection Works", expanded=False):
            col1, col2, col3 = st.columns(3, gap="medium")
            with col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 2rem 1.5rem; border-radius: 15px; min-height: 280px;
                            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
                            display: flex; flex-direction: column; align-items: center; justify-content: center;
                            text-align: center;">
                    <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1.2rem;">📊</div>
                    <h4 style="color: white; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700;">Step 1: Data Collection</h4>
                    <p style="color: rgba(255,255,255,0.95); font-size: 0.95rem; line-height: 1.7; margin: 0;">
                        System collects all your transaction amounts and calculates average & standard deviation
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                            padding: 2rem 1.5rem; border-radius: 15px; min-height: 280px;
                            box-shadow: 0 4px 15px rgba(79,172,254,0.3);
                            display: flex; flex-direction: column; align-items: center; justify-content: center;
                            text-align: center;">
                    <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1.2rem;">🔢</div>
                    <h4 style="color: white; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700;">Step 2: Z-Score Analysis</h4>
                    <p style="color: rgba(255,255,255,0.95); font-size: 0.95rem; line-height: 1.7; margin: 0;">
                        Each transaction gets a Z-Score showing how many standard deviations it is from average
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                            padding: 2rem 1.5rem; border-radius: 15px; min-height: 280px;
                            box-shadow: 0 4px 15px rgba(250,112,154,0.3);
                            display: flex; flex-direction: column; align-items: center; justify-content: center;
                            text-align: center;">
                    <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1.2rem;">🚨</div>
                    <h4 style="color: white; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700;">Step 3: Flag Outliers</h4>
                    <p style="color: rgba(255,255,255,0.95); font-size: 0.95rem; line-height: 1.7; margin: 0;">
                        Transactions with Z-Score > 2 are flagged as anomalies (unusually high spending)
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        anomalies = anomaly_detector.detect_amount_anomalies()
        anomaly_summary = anomaly_detector.get_anomaly_summary()
        
        # Results Section
        col_r1, col_r2 = st.columns([2, 1], gap="large")
        
        with col_r1:
            if anomalies:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                            padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                            border-left: 4px solid #f39c12; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <h4 style="margin: 0; color: #856404;">⚠️ Found {len(anomalies)} unusual transaction(s)</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #856404; font-size: 0.9rem;">These transactions are significantly higher than your average spending</p>
                </div>
                """, unsafe_allow_html=True)
                
                for idx, anomaly in enumerate(anomalies, 1):
                    with st.expander(f"🔍 Anomaly {idx}: ₹{anomaly['amount']:,.2f} on {anomaly['date']} - {anomaly['category']}", expanded=idx==1):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"""
                            <div style="background: #f8f9fa; padding: 1.2rem; border-radius: 8px; margin-bottom: 0.5rem;">
                                <p style="margin: 0.5rem 0;"><strong>📝 Description:</strong><br>{anomaly['description']}</p>
                                <p style="margin: 0.5rem 0;"><strong>📅 Date:</strong> {anomaly['date']}</p>
                                <p style="margin: 0.5rem 0;"><strong>🏷️ Category:</strong> {anomaly['category']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_b:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                        padding: 1.2rem; border-radius: 8px; text-align: center;">
                                <p style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin: 0.3rem 0;">Z-Score</p>
                                <h3 style="color: white; margin: 0.3rem 0; font-size: 1.8rem;">{anomaly['z_score']:.2f}</h3>
                                <p style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin: 0.3rem 0;">Deviation</p>
                                <p style="color: white; margin: 0; font-size: 1.1rem;">{anomaly['deviation']}</p>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
                            padding: 2.5rem; border-radius: 12px; text-align: center;
                            border-left: 4px solid #5cb85c; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
                    <h4 style="margin: 0; color: #2d5016; font-size: 1.3rem;">No anomalies detected</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #2d5016;">Your spending patterns look normal and consistent!</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_r2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                        padding: 1.2rem; border-radius: 12px; text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #2a5298; margin: 0 0 0.8rem 0; font-size: 1rem;">📚 Understanding Z-Score</h4>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: left;">
                    <p style="margin: 0.5rem 0; color: #2a5298; font-size: 0.85rem;">
                        <strong>Z-Score < 2:</strong><br>Normal spending ✅
                    </p>
                    <p style="margin: 0.5rem 0; color: #856404; font-size: 0.85rem;">
                        <strong>Z-Score 2-3:</strong><br>Unusual spending ⚠️
                    </p>
                    <p style="margin: 0.5rem 0; color: #721c24; font-size: 0.85rem;">
                        <strong>Z-Score > 3:</strong><br>Highly unusual 🚨
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Overspending Analysis
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;">
            <h4 style="color: white; margin: 0;">💸 Budget Breach Analysis</h4>
            <p style="color: rgba(255,255,255,0.85); margin: 0.3rem 0 0 0; font-size: 0.9rem;">
                Periods when spending exceeded recommended category budgets
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        overspend_periods = anomaly_detector.detect_overspending_periods()
        
        if overspend_periods:
            st.markdown(f"""
            <div style="background: #fff3cd; padding: 1.2rem; border-radius: 8px; margin-bottom: 1rem;
                        border-left: 4px solid #ffc107; box-shadow: 0 3px 10px rgba(0,0,0,0.08);">
                <p style="margin: 0; color: #856404; font-weight: 600; font-size: 1.05rem;">
                    ⚠️ Found {len(overspend_periods)} budget breach(es)
                </p>
                <p style="margin: 0.5rem 0 0 0; color: #856404; font-size: 0.9rem;">
                    These are periods where spending significantly exceeded typical amounts
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            overspend_df = pd.DataFrame(overspend_periods)
            st.dataframe(overspend_df, use_container_width=True, height=200)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
                        padding: 1.8rem; border-radius: 12px; text-align: center;
                        border-left: 4px solid #5cb85c; box-shadow: 0 3px 10px rgba(0,0,0,0.08);">
                <p style="margin: 0; color: #2d5016; font-weight: 600; font-size: 1.1rem;">✅ No budget breaches detected!</p>
                <p style="margin: 0.5rem 0 0 0; color: #2d5016; font-size: 0.9rem;">Your spending stays within healthy limits</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Get prediction data first
        risk_data = predictor.predict_overspend_risk()
        risk_factors = predictor.get_risk_factors()
        recommendations = predictor.get_recommendations()
        
        # Pre-calculate all dynamic values
        risk_percentage = risk_data['risk_percentage']
        risk_level = risk_data['risk_level']
        risk_probability = risk_data['risk_probability']
        
        # Determine color scheme based on risk level
        if risk_level == 'High':
            header_gradient = "linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)"
            ring_color = "#ff6b6b"
            status_message = "⚠️ Immediate attention required - High spending risk detected"
            status_icon = "🚨"
        elif risk_level == 'Moderate':
            header_gradient = "linear-gradient(135deg, #feca57 0%, #ff9ff3 100%)"
            ring_color = "#feca57"
            status_message = "⚡ Monitor your spending - Moderate risk level"
            status_icon = "⚠️"
        else:
            header_gradient = "linear-gradient(135deg, #48c6ef 0%, #6dd5fa 100%)"
            ring_color = "#48c6ef"
            status_message = "✅ Excellent! Your spending habits are healthy"
            status_icon = "🎉"
        
        # Enhanced Predictions Header
        st.markdown(f"""
        <div style="background: {header_gradient};
                    padding: 3rem 2rem; border-radius: 20px; margin-bottom: 2rem;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.15); text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 0.5rem;">{status_icon}</div>
            <h3 style="margin: 0; color: white; font-size: 2rem; font-weight: 800; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                ML Prediction & Risk Analysis
            </h3>
            <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.95); font-size: 1.1rem;">
                AI-powered spending predictions and risk assessment
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Score Card - Prominent Display
        st.markdown(f"""
        <div style="background: white; padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                    box-shadow: 0 8px 30px rgba(0,0,0,0.1); text-align: center;
                    border: 3px solid {ring_color};">
            <p style="color: #666; font-size: 0.9rem; margin: 0 0 0.5rem 0; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">
                Your Overspending Risk Score
            </p>
            <h1 style="color: {ring_color}; font-size: 5rem; font-weight: 900; margin: 0; line-height: 1;">
                {risk_percentage:.1f}%
            </h1>
            <div style="display: inline-block; background: {header_gradient}; padding: 0.8rem 2rem; 
                        border-radius: 50px; margin-top: 1rem;">
                <p style="color: white; font-size: 1.2rem; font-weight: 700; margin: 0;">
                    {risk_level} Risk Level
                </p>
            </div>
            <p style="color: #666; font-size: 1rem; margin: 1.5rem 0 0 0; max-width: 600px; margin-left: auto; margin-right: auto;">
                {status_message}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # How ML Prediction Works
        with st.expander("📖 How ML Risk Prediction Works", expanded=False):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                        padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <h4 style="color: #2a5298; margin: 0 0 1rem 0; font-size: 1.2rem;">🧠 Machine Learning Workflow</h4>
                <p style="color: #2a5298; margin: 0; line-height: 1.8; font-size: 1rem;">
                    Our AI model uses <strong>Logistic Regression</strong> to predict overspending risk by analyzing 4 key behavioral factors
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 2rem 1.8rem; border-radius: 15px; min-height: 240px;
                            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
                            display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1rem;">📊</div>
                        <h4 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 700;">Feature 1: Delivery Ratio</h4>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px;">
                        <p style="color: white; font-size: 0.9rem; line-height: 1.7; margin: 0;">
                            <strong>What:</strong> % of spending on deliveries<br>
                            <strong>Risk if:</strong> >25% (Moderate), >40% (High)<br>
                            <strong>Why:</strong> High delivery = impulsive spending
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                            padding: 2rem 1.8rem; border-radius: 15px; min-height: 240px;
                            box-shadow: 0 4px 15px rgba(79,172,254,0.3);
                            display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1rem;">📈</div>
                        <h4 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 700;">Feature 2: Spending Volatility</h4>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px;">
                        <p style="color: white; font-size: 0.9rem; line-height: 1.7; margin: 0;">
                            <strong>What:</strong> Standard deviation of amounts<br>
                            <strong>Risk if:</strong> >₹300 (Moderate), >₹500 (High)<br>
                            <strong>Why:</strong> Erratic spending = poor budgeting
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                            padding: 2rem 1.8rem; border-radius: 15px; min-height: 240px;
                            box-shadow: 0 4px 15px rgba(250,112,154,0.3);
                            display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1rem;">🚨</div>
                        <h4 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 700;">Feature 3: Anomaly Count</h4>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px;">
                        <p style="color: white; font-size: 0.9rem; line-height: 1.7; margin: 0;">
                            <strong>What:</strong> Number of unusual transactions<br>
                            <strong>Risk if:</strong> >3 anomalies (Moderate), >6 (High)<br>
                            <strong>Why:</strong> Frequent outliers = impulse buys
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            padding: 2rem 1.8rem; border-radius: 15px; min-height: 240px;
                            box-shadow: 0 4px 15px rgba(240,147,251,0.3);
                            display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1rem;">💰</div>
                        <h4 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 700;">Feature 4: Budget Breaches</h4>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px;">
                        <p style="color: white; font-size: 0.9rem; line-height: 1.7; margin: 0;">
                            <strong>What:</strong> Times exceeded budget limits<br>
                            <strong>Risk if:</strong> >1 breach (Moderate), >3 (High)<br>
                            <strong>Why:</strong> Regular violations = poor control
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
                        padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h4 style="color: #2d5016; margin: 0 0 1.2rem 0; font-size: 1.2rem; text-align: center;">🎯 How Risk is Calculated</h4>
                <div style="background: white; padding: 1.5rem; border-radius: 10px;">
                    <p style="color: #2d5016; margin: 0; font-size: 0.95rem; line-height: 2;">
                        <strong>Step 1:</strong> Extract 4 features from your spending data<br>
                        <strong>Step 2:</strong> Normalize features using statistical scaling<br>
                        <strong>Step 3:</strong> Feed into trained Logistic Regression model<br>
                        <strong>Step 4:</strong> Model outputs probability (0-100%)<br>
                        <strong>Step 5:</strong> Classify: 0-30% Low, 30-60% Moderate, 60-100% High
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feature Analysis - 4 Column Grid
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #2a5298; margin: 0 0 1rem 0; font-size: 1.3rem;">📊 Feature Analysis Breakdown</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4, gap="medium")
        
        # Feature 1: Delivery Ratio
        with col_f1:
            delivery_status = "🔴 High" if risk_data['features']['delivery_ratio'] > 0.25 else "🟡 Moderate" if risk_data['features']['delivery_ratio'] > 0.15 else "🟢 Good"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.8rem 1.5rem; border-radius: 15px; text-align: center;
                        box-shadow: 0 6px 20px rgba(102,126,234,0.25);
                        transition: transform 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🍕</div>
                <p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 600;">Delivery Ratio</p>
                <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 2rem; font-weight: 800;">
                    {risk_data['features']['delivery_ratio']*100:.1f}%
                </h3>
                <p style="color: rgba(255,255,255,0.85); font-size: 0.8rem; margin: 0;">{delivery_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature 2: Volatility
        with col_f2:
            volatility_status = "🔴 High" if risk_data['features']['volatility'] > 500 else "🟡 Moderate" if risk_data['features']['volatility'] > 300 else "🟢 Low"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                        padding: 1.8rem 1.5rem; border-radius: 15px; text-align: center;
                        box-shadow: 0 6px 20px rgba(79,172,254,0.25);
                        transition: transform 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">📈</div>
                <p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 600;">Volatility</p>
                <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 2rem; font-weight: 800;">
                    ₹{risk_data['features']['volatility']:.0f}
                </h3>
                <p style="color: rgba(255,255,255,0.85); font-size: 0.8rem; margin: 0;">{volatility_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature 3: Anomalies
        with col_f3:
            anomaly_status = "🔴 High" if risk_data['features']['anomaly_count'] > 6 else "🟡 Moderate" if risk_data['features']['anomaly_count'] > 3 else "🟢 Low"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                        padding: 1.8rem 1.5rem; border-radius: 15px; text-align: center;
                        box-shadow: 0 6px 20px rgba(250,112,154,0.25);
                        transition: transform 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🚨</div>
                <p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 600;">Anomalies</p>
                <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 2rem; font-weight: 800;">
                    {risk_data['features']['anomaly_count']}
                </h3>
                <p style="color: rgba(255,255,255,0.85); font-size: 0.8rem; margin: 0;">{anomaly_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature 4: Budget Breaches
        with col_f4:
            breach_status = "🔴 High" if risk_data['features']['budget_breach_count'] > 3 else "🟡 Moderate" if risk_data['features']['budget_breach_count'] > 1 else "🟢 None"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        padding: 1.8rem 1.5rem; border-radius: 15px; text-align: center;
                        box-shadow: 0 6px 20px rgba(240,147,251,0.25);
                        transition: transform 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">💰</div>
                <p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 600;">Budget Breaches</p>
                <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 2rem; font-weight: 800;">
                    {risk_data['features']['budget_breach_count']}
                </h3>
                <p style="color: rgba(255,255,255,0.85); font-size: 0.8rem; margin: 0;">{breach_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Enhanced Gauge Chart and Risk Interpretation Section
        col_gauge, col_info = st.columns([2, 1], gap="large")
        
        with col_gauge:
            # Animation based on risk level
            pulse_animation = ""
            if risk_level == "High":
                pulse_animation = """
                @keyframes pulse-glow {
                    0%, 100% { box-shadow: 0 0 20px rgba(255, 107, 107, 0.4), 0 0 40px rgba(255, 107, 107, 0.2); }
                    50% { box-shadow: 0 0 30px rgba(255, 107, 107, 0.6), 0 0 60px rgba(255, 107, 107, 0.3); }
                }
                .gauge-container { animation: pulse-glow 2s ease-in-out infinite; }
                """
            elif risk_level == "Moderate":
                pulse_animation = """
                @keyframes soft-glow {
                    0%, 100% { box-shadow: 0 0 15px rgba(254, 202, 87, 0.3), 0 0 30px rgba(254, 202, 87, 0.15); }
                    50% { box-shadow: 0 0 25px rgba(254, 202, 87, 0.4), 0 0 45px rgba(254, 202, 87, 0.2); }
                }
                .gauge-container { animation: soft-glow 3s ease-in-out infinite; }
                """
            
            st.markdown(f"""
            <style>
            {pulse_animation}
            @keyframes shimmer {{
                0% {{ background-position: -1000px 0; }}
                100% {{ background-position: 1000px 0; }}
            }}
            @keyframes rotate-gradient {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            @keyframes gauge-glow {{
                0%, 100% {{ filter: drop-shadow(0 0 15px {ring_color}40); }}
                50% {{ filter: drop-shadow(0 0 25px {ring_color}60); }}
            }}
            .gauge-container {{
                background: linear-gradient(135deg, 
                    rgba(255,255,255,1) 0%, 
                    rgba(248,249,250,1) 30%,
                    rgba(255,255,255,1) 60%,
                    rgba(248,249,250,1) 100%);
                background-size: 400% 400%;
                animation: rotate-gradient 8s ease infinite;
                padding: 2.5rem 2rem;
                border-radius: 28px;
                position: relative;
                overflow: visible;
                border: 3px solid {ring_color};
                box-shadow: 
                    0 15px 45px rgba(0,0,0,0.12),
                    0 5px 15px rgba(0,0,0,0.08),
                    inset 0 1px 0 rgba(255,255,255,0.8),
                    inset 0 -1px 0 rgba(0,0,0,0.05);
            }}
            .gauge-container::before {{
                content: '';
                position: absolute;
                top: -4px;
                left: -4px;
                right: -4px;
                bottom: -4px;
                background: linear-gradient(
                    135deg, 
                    {ring_color}60 0%, 
                    transparent 30%, 
                    {ring_color}40 50%, 
                    transparent 70%, 
                    {ring_color}60 100%
                );
                border-radius: 30px;
                opacity: 0.4;
                z-index: -1;
                animation: rotate-gradient 4s linear infinite;
                background-size: 300% 300%;
                filter: blur(8px);
            }}
            .gauge-container::after {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 40%;
                background: linear-gradient(180deg, rgba(255,255,255,0.6), transparent);
                border-radius: 28px 28px 0 0;
                pointer-events: none;
            }}
            .gauge-header {{
                background: linear-gradient(
                    135deg, 
                    {ring_color}15 0%, 
                    {ring_color}30 50%, 
                    {ring_color}15 100%
                );
                padding: 1.4rem 1.2rem;
                border-radius: 18px;
                margin-bottom: 1.8rem;
                border-left: 5px solid {ring_color};
                border-right: 1px solid {ring_color}40;
                position: relative;
                overflow: hidden;
                box-shadow: 
                    0 4px 15px {ring_color}20,
                    inset 0 1px 0 rgba(255,255,255,0.5);
            }}
            .gauge-header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(255,255,255,0.5), 
                    transparent);
                animation: shimmer 3s ease-in-out infinite;
            }}
            .gauge-header::after {{
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 4px;
                height: 100%;
                background: linear-gradient(180deg, {ring_color}, transparent);
                opacity: 0.6;
            }}
            </style>
            <div class="gauge-container">
                <div class="gauge-header">
                    <h4 style="color: #2a5298; margin: 0; text-align: center; 
                               font-size: 1.3rem; font-weight: 800; 
                               text-transform: uppercase; letter-spacing: 1px;
                               text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                        📊 Risk Score Analysis
                    </h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Advanced creative gauge chart with professional styling
            # Create gradient color based on risk level
            if risk_probability * 100 <= 30:
                gradient_colors = ['#48c6ef', '#0abfbc', '#48c6ef']
            elif risk_probability * 100 <= 60:
                gradient_colors = ['#feca57', '#ff9ff3', '#feca57']
            else:
                gradient_colors = ['#ff6b6b', '#ee5a6f', '#ff6b6b']
            
            fig = go.Figure()
            
            # Add the main indicator with enhanced styling
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=risk_probability * 100,
                title={'text': ""},
                number={
                    'font': {
                        'size': 56, 
                        'color': ring_color, 
                        'family': 'Arial Black, Arial, sans-serif'
                    }, 
                    'suffix': '%',
                    'valueformat': '.1f',
                    'prefix': ''
                },
                gauge={
                    'shape': 'angular',
                    'axis': {
                        'range': [None, 100],
                        'tickwidth': 3,
                        'tickcolor': ring_color,
                        'tickfont': {
                            'size': 14, 
                            'color': '#2c3e50', 
                            'family': 'Arial'
                        },
                        'tickmode': 'array',
                        'tickvals': [0, 20, 40, 60, 80, 100],
                        'ticktext': ['0', '20', '40', '60', '80', '100'],
                        'ticklen': 12,
                        'showticklabels': True
                    },
                    'bar': {
                        'color': ring_color, 
                        'thickness': 0.75,
                        'line': {
                            'color': 'white', 
                            'width': 3
                        }
                    },
                    'bgcolor': "white",
                    'borderwidth': 3,
                    'bordercolor': ring_color,
                    'steps': [
                        {
                            'range': [0, 30], 
                            'color': "rgba(72, 198, 239, 0.3)"
                        },
                        {
                            'range': [30, 60], 
                            'color': "rgba(254, 202, 87, 0.3)"
                        },
                        {
                            'range': [60, 100], 
                            'color': "rgba(255, 107, 107, 0.3)"
                        }
                    ],
                    'threshold': {
                        'line': {'color': 'white', 'width': 6},
                        'thickness': 0.9,
                        'value': risk_probability * 100
                    }
                }
            ))
            
            # Update layout for professional appearance
            fig.update_layout(
                height=330,
                margin=dict(l=30, r=30, t=30, b=30),
                paper_bgcolor='rgba(255,255,255,0)',
                plot_bgcolor='rgba(255,255,255,0)',
                font={
                    'family': 'Arial, sans-serif',
                    'color': '#2c3e50'
                },
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Enhanced risk level badge with depth and animation
            badge_icon = "🔥" if risk_level == "High" else ("⚡" if risk_level == "Moderate" else "✅")
            
            st.markdown(f"""
            <style>
            @keyframes badge-pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.03); }}
            }}
            @keyframes gradient-shift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            .risk-badge {{
                text-align: center;
                margin-top: 1.5rem;
                padding: 1.5rem;
                background: {header_gradient};
                background-size: 200% 200%;
                border-radius: 16px;
                position: relative;
                animation: badge-pulse 2s ease-in-out infinite, gradient-shift 4s ease infinite;
                box-shadow: 0 8px 32px rgba(0,0,0,0.15),
                           inset 0 1px 0 rgba(255,255,255,0.3);
                border: 2px solid rgba(255,255,255,0.4);
            }}
            .risk-badge::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 50%;
                background: linear-gradient(180deg, rgba(255,255,255,0.3), transparent);
                border-radius: 16px 16px 0 0;
            }}
            .risk-level-text {{
                color: white;
                margin: 0;
                font-size: 1.4rem;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 2px;
                text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
                position: relative;
                z-index: 1;
            }}
            .risk-status-text {{
                color: rgba(255,255,255,0.95);
                margin: 0.5rem 0 0 0;
                font-size: 0.95rem;
                font-weight: 600;
                text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
                position: relative;
                z-index: 1;
            }}
            </style>
            <div class="risk-badge">
                <div style="font-size: 2rem; margin-bottom: 0.5rem; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">
                    {badge_icon}
                </div>
                <p class="risk-level-text">
                    {risk_level} Risk Level
                </p>
                <p class="risk-status-text">
                    {status_icon} {status_message}
                </p>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info:
            # Enhanced Risk Scale Guide
            st.markdown(f"""
            <style>
            @keyframes float-up {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
            }}
            @keyframes card-shine {{
                0% {{ left: -100%; }}
                100% {{ left: 200%; }}
            }}
            .info-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.8rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(102,126,234,0.35),
                           inset 0 1px 0 rgba(255,255,255,0.2);
                margin-bottom: 1.5rem;
                position: relative;
                overflow: hidden;
                border: 2px solid rgba(255,255,255,0.3);
            }}
            .info-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 50%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                animation: card-shine 4s infinite;
            }}
            .risk-scale-item {{
                background: rgba(255,255,255,0.25);
                padding: 1rem;
                border-radius: 12px;
                margin-bottom: 0.8rem;
                border-left: 4px solid white;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                position: relative;
                backdrop-filter: blur(10px);
            }}
            .risk-scale-item:hover {{
                transform: translateX(5px);
                background: rgba(255,255,255,0.35);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }}
            .risk-scale-item.active {{
                background: rgba(255,255,255,0.4);
                border-left-width: 6px;
                animation: float-up 2s ease-in-out infinite;
            }}
            </style>
            <div class="info-card">
                <h4 style="color: white; margin: 0 0 1.2rem 0; font-size: 1.1rem; 
                           font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                    🎯 Risk Scale Guide
                </h4>
                <div class="risk-scale-item {'active' if risk_level == 'Low' else ''}">
                    <p style="color: white; margin: 0; font-size: 0.9rem; line-height: 1.6;">
                        <strong style="font-size: 1.05rem;">🟢 0-30%</strong><br>
                        <span style="opacity: 0.95; font-weight: 500;">Low Risk - Healthy spending</span>
                    </p>
                </div>
                <div class="risk-scale-item {'active' if risk_level == 'Moderate' else ''}">
                    <p style="color: white; margin: 0; font-size: 0.9rem; line-height: 1.6;">
                        <strong style="font-size: 1.05rem;">🟡 30-60%</strong><br>
                        <span style="opacity: 0.95; font-weight: 500;">Moderate Risk - Monitor closely</span>
                    </p>
                </div>
                <div class="risk-scale-item {'active' if risk_level == 'High' else ''}" style="margin-bottom: 0;">
                    <p style="color: white; margin: 0; font-size: 0.9rem; line-height: 1.6;">
                        <strong style="font-size: 1.05rem;">🔴 60-100%</strong><br>
                        <span style="opacity: 0.95; font-weight: 500;">High Risk - Take action now</span>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced ML Insights
            st.markdown(f"""
            <style>
            .ml-insights-card {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 1.8rem;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(240,147,251,0.35),
                           inset 0 1px 0 rgba(255,255,255,0.2);
                position: relative;
                overflow: hidden;
                border: 2px solid rgba(255,255,255,0.3);
            }}
            .ml-insights-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 50%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                animation: card-shine 4s infinite 1s;
            }}
            .insight-item {{
                background: rgba(255,255,255,0.25);
                padding: 1rem;
                border-radius: 12px;
                margin-bottom: 0.8rem;
                border-left: 4px solid white;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }}
            .insight-item:hover {{
                transform: scale(1.03);
                background: rgba(255,255,255,0.35);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }}
            .insight-value {{
                font-size: 1.15rem;
                font-weight: 800;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
            }}
            </style>
            <div class="ml-insights-card">
                <h4 style="color: white; margin: 0 0 1.2rem 0; font-size: 1.1rem; 
                           font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                    ⚡ ML Intelligence
                </h4>
                <div class="insight-item">
                    <p style="color: white; margin: 0; font-size: 0.85rem;">
                        <strong>Risk Classification</strong><br>
                        <span class="insight-value">{risk_data['risk_class']}</span>
                    </p>
                </div>
                <div class="insight-item">
                    <p style="color: white; margin: 0; font-size: 0.85rem;">
                        <strong>ML Probability Score</strong><br>
                        <span class="insight-value">{risk_data['risk_probability']:.3f}</span>
                    </p>
                </div>
                <div class="insight-item" style="margin-bottom: 0;">
                    <p style="color: white; margin: 0; font-size: 0.85rem;">
                        <strong>Analysis Features</strong><br>
                        <span class="insight-value">4 factors evaluated</span>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Risk Factors Section - Enhanced Cards
        if risk_factors:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem; border-radius: 20px; margin-bottom: 2rem;
                        box-shadow: 0 8px 30px rgba(102,126,234,0.35);">
                <div style="text-align: center;">
                    <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.8rem; font-weight: 700;">⚡ Identified Risk Factors</h3>
                    <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 1.05rem;">
                        These factors are elevating your overspending risk score
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display risk factors in an attractive grid
            cols_per_row = 2 if len(risk_factors) <= 4 else 3
            rows = [risk_factors[i:i+cols_per_row] for i in range(0, len(risk_factors), cols_per_row)]
            
            for row in rows:
                cols = st.columns(len(row), gap="large")
                for idx, (col, factor) in enumerate(zip(cols, row)):
                    with col:
                        if factor['severity'] == 'High':
                            icon = "🚨"
                            gradient = "linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)"
                            shadow = "rgba(255, 107, 107, 0.3)"
                            text_color = "white"
                        else:
                            icon = "⚠️"
                            gradient = "linear-gradient(135deg, #feca57 0%, #ff9ff3 100%)"
                            shadow = "rgba(254, 202, 87, 0.3)"
                            text_color = "white"
                        
                        st.markdown(f"""
                        <div style="background: {gradient};
                                    padding: 2rem 1.8rem; border-radius: 18px;
                                    box-shadow: 0 8px 25px {shadow};
                                    transition: all 0.3s ease;
                                    margin-bottom: 1rem;
                                    text-align: center;">
                            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
                            <h4 style="color: {text_color}; margin: 0 0 1rem 0; font-size: 1.15rem; font-weight: 700;">
                                {factor['factor']}
                            </h4>
                            <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 12px;">
                                <p style="color: {text_color}; margin: 0; font-size: 1.8rem; font-weight: 800;">
                                    {factor['value']}
                                </p>
                            </div>
                            <div style="margin-top: 1rem; padding: 0.6rem; background: rgba(255,255,255,0.15); border-radius: 8px;">
                                <p style="color: {text_color}; margin: 0; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                                    {factor['severity']} Severity
                                </p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #48c6ef 0%, #6dd5fa 100%);
                        padding: 3rem 2rem; border-radius: 20px; text-align: center;
                        box-shadow: 0 8px 30px rgba(72, 198, 239, 0.3); margin-bottom: 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
                <h3 style="color: white; margin: 0 0 0.8rem 0; font-size: 1.8rem; font-weight: 700;">
                    No Risk Factors Detected!
                </h3>
                <p style="color: white; margin: 0; font-size: 1.1rem;">
                    Your spending behavior is healthy across all metrics. Keep up the excellent work!
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations Section - Enhanced Grid
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                    padding: 2rem; border-radius: 20px; margin-bottom: 1.5rem;
                    box-shadow: 0 8px 30px rgba(168, 237, 234, 0.35);">
            <div style="text-align: center;">
                <h3 style="color: #2a5298; margin: 0 0 0.5rem 0; font-size: 1.8rem; font-weight: 700;">💡 AI-Powered Recommendations</h3>
                <p style="color: #2a5298; margin: 0; font-size: 1.05rem;">
                    Personalized suggestions to improve your financial wellness
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display recommendations in card grid
        rec_cols = st.columns(2, gap="large")
        for i, rec in enumerate(recommendations):
            with rec_cols[i % 2]:
                # Determine icon based on recommendation text
                if '🍕' in rec or 'delivery' in rec.lower():
                    icon = "🍕"
                    gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                elif '📊' in rec or 'budget' in rec.lower():
                    icon = "📊"
                    gradient = "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
                elif '🔍' in rec or 'review' in rec.lower():
                    icon = "🔍"
                    gradient = "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
                elif '💰' in rec or 'alert' in rec.lower() or 'saving' in rec.lower():
                    icon = "💰"
                    gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
                elif '📱' in rec or 'notification' in rec.lower():
                    icon = "📱"
                    gradient = "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
                else:
                    icon = "✨"
                    gradient = "linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)"
                
                st.markdown(f"""
                <div style="background: white;
                            padding: 1.8rem; border-radius: 15px;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                            margin-bottom: 1rem;
                            border-left: 5px solid transparent;
                            border-image: {gradient} 1;
                            transition: all 0.3s ease;">
                    <div style="display: flex; align-items: flex-start; gap: 1rem;">
                        <div style="background: {gradient};
                                    min-width: 50px; height: 50px; border-radius: 12px;
                                    display: flex; align-items: center; justify-content: center;
                                    font-size: 1.5rem; flex-shrink: 0;">
                            {icon}
                        </div>
                        <div style="flex: 1;">
                            <p style="color: #2a5298; margin: 0; font-size: 0.95rem; line-height: 1.7; font-weight: 500;">
                                {rec}
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        # Enhanced Delivery Analysis Header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 1.5rem 2rem; border-radius: 15px; margin-bottom: 1.5rem;">
            <h3 style="margin: 0; color: white; font-size: 1.8rem; font-weight: 700;">🍕 Food Delivery Analysis</h3>
            <p style="margin: 0.3rem 0 0 0; color: rgba(255,255,255,0.9);">Track your food delivery spending habits</p>
        </div>
        """, unsafe_allow_html=True)
        
        # How Delivery Analysis Works
        with st.expander("📖 How Delivery Analysis Works", expanded=False):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem; border-radius: 15px; margin-bottom: 1.5rem;
                        box-shadow: 0 4px 15px rgba(102,126,234,0.3);">
                <h4 style="color: white; margin: 0 0 1rem 0; font-size: 1.2rem; text-align: center;">🔍 Analysis Methodology</h4>
                <p style="color: rgba(255,255,255,0.95); line-height: 1.8; margin: 0; text-align: center; font-size: 1rem;">
                    This section analyzes your food delivery spending from platforms like Swiggy, Zomato, Uber Eats, and Dunzo
                    to help you understand convenience spending patterns.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3, gap="medium")
            
            with col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                            padding: 2rem 1.5rem; border-radius: 15px; min-height: 280px;
                            box-shadow: 0 4px 15px rgba(79,172,254,0.3);
                            display: flex; flex-direction: column; align-items: center; justify-content: center;
                            text-align: center;">
                    <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1.2rem;">📊</div>
                    <h4 style="color: white; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700;">Step 1: Identify Delivery Orders</h4>
                    <p style="color: rgba(255,255,255,0.95); font-size: 0.95rem; line-height: 1.7; margin: 0;">
                        Filters transactions by "Food Delivery" category from sources like Swiggy, Zomato, Uber Eats, Dunzo
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                            padding: 2rem 1.5rem; border-radius: 15px; min-height: 280px;
                            box-shadow: 0 4px 15px rgba(250,112,154,0.3);
                            display: flex; flex-direction: column; align-items: center; justify-content: center;
                            text-align: center;">
                    <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1.2rem;">💰</div>
                    <h4 style="color: white; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700;">Step 2: Calculate Metrics</h4>
                    <p style="color: rgba(255,255,255,0.95); font-size: 0.95rem; line-height: 1.7; margin: 0;">
                        Computes: Total spent, Number of orders, % of total spending, Average order value, Frequency patterns
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            padding: 2rem 1.5rem; border-radius: 15px; min-height: 280px;
                            box-shadow: 0 4px 15px rgba(240,147,251,0.3);
                            display: flex; flex-direction: column; align-items: center; justify-content: center;
                            text-align: center;">
                    <div style="font-size: 3.5rem; line-height: 1; margin-bottom: 1.2rem;">📈</div>
                    <h4 style="color: white; margin-bottom: 1rem; font-size: 1.15rem; font-weight: 700;">Step 3: Risk Assessment</h4>
                    <p style="color: rgba(255,255,255,0.95); font-size: 0.95rem; line-height: 1.7; margin: 0;">
                        Compares to thresholds: >25% = High risk, 15-25% = Moderate, <15% = Healthy
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
                        padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h4 style="color: #2d5016; margin: 0 0 1.2rem 0; font-size: 1.2rem; text-align: center;">🎯 Why This Matters</h4>
                <div style="background: white; padding: 1.5rem; border-radius: 10px;">
                    <p style="color: #2d5016; margin: 0; font-size: 0.95rem; line-height: 2;">
                        <strong>🍔 Convenience Cost:</strong> Delivery orders typically cost 1.5-2x more than cooking<br>
                        <strong>💸 Budget Impact:</strong> Regular delivery spending can silently drain budgets<br>
                        <strong>🌙 Behavioral Pattern:</strong> Late-night orders often indicate poor planning<br>
                        <strong>📊 Benchmark:</strong> Financial experts recommend keeping delivery spending under 15% of total
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        delivery_metrics = analytics.get_delivery_metrics()
        
        # Enhanced Metrics Cards
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 6px 20px rgba(102,126,234,0.3);">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">💵</div>
                <p style="color: rgba(255,255,255,0.85); font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 600; text-transform: uppercase;">Total Delivery Spending</p>
                <h2 style="color: white; margin: 0; font-size: 2.2rem; font-weight: 800;">₹{delivery_metrics['delivery_total']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                        padding: 2rem 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 6px 20px rgba(79,172,254,0.3);">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">🍽️</div>
                <p style="color: rgba(255,255,255,0.85); font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 600; text-transform: uppercase;">Number of Orders</p>
                <h2 style="color: white; margin: 0; font-size: 2.2rem; font-weight: 800;">{delivery_metrics['delivery_count']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Dynamic color based on percentage
            if delivery_metrics['delivery_percentage'] > 25:
                percentage_gradient = "linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%)"
            elif delivery_metrics['delivery_percentage'] > 15:
                percentage_gradient = "linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%)"
            else:
                percentage_gradient = "linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)"
            
            st.markdown(f"""
            <div style="background: {percentage_gradient};
                        padding: 2rem 1.5rem; border-radius: 12px; text-align: center;
                        box-shadow: 0 6px 20px rgba(250,112,154,0.3);">
                <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">📊</div>
                <p style="color: rgba(0,0,0,0.7); font-size: 0.85rem; margin: 0 0 0.5rem 0; font-weight: 600; text-transform: uppercase;">% of Total Spending</p>
                <h2 style="color: #333; margin: 0; font-size: 2.2rem; font-weight: 800;">{delivery_metrics['delivery_percentage']:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Enhanced Delivery Insights
        col_insight1, col_insight2 = st.columns([2, 1], gap="large")
        
        with col_insight1:
            if delivery_metrics['delivery_percentage'] > 25:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
                            padding: 2.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                            border-left: 4px solid #dc3545; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <div style="font-size: 3.5rem; margin-bottom: 1rem;">🚨</div>
                    <h4 style="color: #721c24; margin-bottom: 0.8rem; font-size: 1.3rem;">High Delivery Spending Alert</h4>
                    <p style="color: #721c24; margin: 0; font-size: 1.05rem; line-height: 1.6;">
                        Your delivery spending <strong>({delivery_metrics['delivery_percentage']:.1f}%)</strong> is significantly above 
                        the recommended threshold of <strong>15-20%</strong> of total spending.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
                            padding: 2rem; border-radius: 12px; border-left: 4px solid #17a2b8;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                    <h4 style="color: #0c5460; margin: 0 0 1rem 0;">💡 Action Plan</h4>
                    <ul style="color: #0c5460; margin: 0; padding-left: 1.5rem; line-height: 2;">
                        <li>Cook at home 3-4 times per week</li>
                        <li>Meal prep on weekends to reduce weekday temptation</li>
                        <li>Set a monthly delivery budget (e.g., ₹3,000-₹4,000)</li>
                        <li>Uninstall delivery apps for 1-2 weeks as a reset</li>
                        <li>Track savings from home-cooked meals</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
            elif delivery_metrics['delivery_percentage'] > 15:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                            padding: 2.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                            border-left: 4px solid #ffc107; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <div style="font-size: 3.5rem; margin-bottom: 1rem;">⚠️</div>
                    <h4 style="color: #856404; margin-bottom: 0.8rem; font-size: 1.3rem;">Moderate Delivery Spending</h4>
                    <p style="color: #856404; margin: 0; font-size: 1.05rem; line-height: 1.6;">
                        Your delivery spending <strong>({delivery_metrics['delivery_percentage']:.1f}%)</strong> is in the moderate range. 
                        A few adjustments can optimize this further.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
                            padding: 2rem; border-radius: 12px; border-left: 4px solid #17a2b8;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                    <h4 style="color: #0c5460; margin: 0 0 1rem 0;">💡 Optimization Tips</h4>
                    <ul style="color: #0c5460; margin: 0; padding-left: 1.5rem; line-height: 2;">
                        <li>Plan meals on Sunday for the week ahead</li>
                        <li>Batch cook and freeze portions for busy days</li>
                        <li>Reserve delivery for special occasions only</li>
                        <li>Try meal kit services as a middle ground</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
                            padding: 2.5rem; border-radius: 12px; text-align: center;
                            border-left: 4px solid #5cb85c; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
                    <h4 style="color: #2d5016; margin-bottom: 0.8rem; font-size: 1.4rem;">Excellent Control!</h4>
                    <p style="color: #2d5016; margin: 0; font-size: 1.05rem; line-height: 1.6;">
                        Your delivery spending <strong>({delivery_metrics['delivery_percentage']:.1f}%)</strong> is well-controlled 
                        and within healthy limits. Keep up the great work!
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_insight2:
            # Average Order Value
            if delivery_metrics['delivery_count'] > 0:
                avg_order = delivery_metrics['delivery_total'] / delivery_metrics['delivery_count']
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1rem;">
                    <p style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin: 0 0 0.5rem 0;">Avg Order Value</p>
                    <h3 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 700;">₹{avg_order:.2f}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Delivery Spending Breakdown
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
                        padding: 1.5rem; border-radius: 12px;">
                <h4 style="color: #2a5298; margin: 0 0 1rem 0; font-size: 1rem;">📋 Healthy Benchmarks</h4>
                <div style="background: white; padding: 1rem; border-radius: 8px;">
                    <p style="margin: 0.5rem 0; color: #2d5016; font-size: 0.85rem;">
                        <strong>✅ Optimal:</strong> <15%
                    </p>
                    <p style="margin: 0.5rem 0; color: #856404; font-size: 0.85rem;">
                        <strong>⚠️ Moderate:</strong> 15-25%
                    </p>
                    <p style="margin: 0.5rem 0; color: #721c24; font-size: 0.85rem;">
                        <strong>🚨 High:</strong> >25%
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Late night orders
        st.markdown("<br>", unsafe_allow_html=True)
        late_night = analytics.detect_late_night_orders()
        if late_night:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="color: white; margin: 0;">🌙 Late Night Ordering Pattern Detected</h4>
                <p style="color: rgba(255,255,255,0.85); margin: 0.3rem 0 0 0; font-size: 0.9rem;">
                    Orders placed between 10 PM - 2 AM often indicate poor meal planning
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col_ln1, col_ln2 = st.columns([2, 1])
            with col_ln1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                            padding: 1.8rem; border-radius: 10px;
                            border-left: 4px solid #ffc107; box-shadow: 0 3px 10px rgba(0,0,0,0.08);">
                    <p style="margin: 0; color: #856404; font-weight: 600; font-size: 1.05rem;">
                        🌛 Found {len(late_night)} late-night order(s)
                    </p>
                    <p style="margin: 0.5rem 0 0 0; color: #856404; font-size: 0.9rem;">
                        Planning meals ahead can help reduce these unplanned expenses!
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with col_ln2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                            padding: 1.5rem; border-radius: 10px; text-align: center;">
                    <p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 0;">💡 Quick Tip</p>
                    <p style="color: white; font-size: 0.9rem; margin: 0.5rem 0 0 0; line-height: 1.5;">
                        Keep healthy snacks ready for late-night cravings
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Close insights container
    st.markdown('</div>', unsafe_allow_html=True)


def render_profile():
    """Render user profile page with modern dark theme"""
    user_id = get_current_user_id()
    user_name = get_current_user_name()
    user_email = get_current_user_email()
    
    # Modern Profile Styles
    st.markdown("""
    <style>
    .profile-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .profile-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: profilePulse 4s ease-in-out infinite;
    }
    @keyframes profilePulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    .profile-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        margin: 0 auto 0.8rem;
        border: 4px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.25);
        position: relative;
        z-index: 1;
        animation: avatarFloat 3s ease-in-out infinite;
    }
    @keyframes avatarFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .profile-name {
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    .profile-email {
        font-size: 1.1rem;
        text-align: center;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    .profile-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        position: relative;
        overflow: hidden;
    }
    .profile-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.08) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .profile-card:hover::before {
        opacity: 1;
    }
    .profile-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 10px 32px rgba(102, 126, 234, 0.3), 0 0 20px rgba(245, 87, 108, 0.15);
        border-color: rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(245, 87, 108, 0.08) 100%);
    }
    .profile-card-header {
        font-size: 0.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        position: relative;
        z-index: 1;
    }
    .profile-card-icon {
        font-size: 1.6rem;
        filter: drop-shadow(0 2px 6px rgba(102, 126, 234, 0.25));
        transition: all 0.3s ease;
    }
    .profile-card:hover .profile-card-icon {
        transform: scale(1.15) rotate(8deg);
        filter: drop-shadow(0 4px 10px rgba(245, 87, 108, 0.4));
    }
    .profile-card-value {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    .profile-card:hover .profile-card-value {
        transform: scale(1.1);
        filter: brightness(1.2);
    }
    .stat-badge {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.2rem;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.25);
        transition: all 0.3s ease;
    }
    .stat-badge:hover {
        transform: scale(1.03);
        box-shadow: 0 5px 16px rgba(102, 126, 234, 0.4);
    }
    .activity-item {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.06) 0%, rgba(118, 75, 162, 0.06) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid;
        border-image: linear-gradient(180deg, #667eea 0%, #f5576c 100%) 1;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        animation: slideInLeft 0.4s ease-out;
    }
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    .activity-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08), transparent);
        transition: left 0.4s ease;
    }
    .activity-item:hover::before {
        left: 100%;
    }
    .activity-item:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(245, 87, 108, 0.12) 100%);
        border-image: linear-gradient(180deg, #f5576c 0%, #667eea 100%) 1;
        transform: translateX(5px) translateY(-2px) scale(1.01);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3), 0 0 15px rgba(245, 87, 108, 0.15);
    }
    .activity-category-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 8px;
        font-size: 1.2rem;
        margin-right: 0.8rem;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.12);
        transition: all 0.3s ease;
    }
    .activity-item:hover .activity-category-icon {
        transform: rotate(8deg) scale(1.08);
        box-shadow: 0 5px 16px rgba(0, 0, 0, 0.2);
    }
    .activity-category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .activity-item:hover .activity-category-badge {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .activity-amount {
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    .activity-item:hover .activity-amount {
        transform: scale(1.08);
        filter: brightness(1.2);
    }
    .activity-date {
        font-weight: 700;
        color: #667eea;
        text-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
    }
    .activity-description {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        line-height: 1.5;
        transition: color 0.3s ease;
    }
    .activity-item:hover .activity-description {
        color: rgba(255, 255, 255, 0.9);
    }
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    .danger-button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
    }
    .danger-button:hover {
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Back button
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Back", key="back_to_dashboard"):
            st.session_state.show_profile = False
            st.rerun()
    
    # Get user data from database
    from database.db import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, created_at FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        st.error("User data not found")
        return
    
    name, email, created_at = user_data
    
    # Calculate account age
    from datetime import datetime
    created_date = datetime.strptime(created_at.split()[0], "%Y-%m-%d")
    days_active = (datetime.now() - created_date).days
    
    # Get profile picture from database
    try:
        cursor.execute("SELECT profile_picture FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        profile_picture = result[0] if result else None
    except sqlite3.OperationalError:
        # Column doesn't exist, add it
        cursor.execute("ALTER TABLE users ADD COLUMN profile_picture TEXT")
        conn.commit()
        profile_picture = None
    
    # Profile Hero Section with Picture Upload - Reorganized Layout
    st.markdown("""
    <style>
    /* Main Profile Container */
    .profile-main-wrapper {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0.5rem;
    }
    
    /* Profile Header Section */
    .profile-header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .profile-header-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        animation: profilePulse 4s ease-in-out infinite;
    }
    
    .profile-content-grid {
        display: grid;
        grid-template-columns: 100px 1fr;
        gap: 1.5rem;
        align-items: center;
        position: relative;
        z-index: 1;
    }
    
    .profile-avatar-wrapper {
        text-align: center;
    }
    
    .profile-info-wrapper {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }
    
    .profile-name-large {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        line-height: 1.2;
        margin: 0;
    }
    
    .profile-email-large {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.85);
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    /* Status Badges Container */
    .status-badges-wrapper {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.6rem;
        margin: 1.5rem 0 1rem;
        padding: 0 1rem;
    }
    
    /* Stats Section Container */
    .stats-container {
        margin: 1.5rem 0;
        clear: both;
    }
    
    /* Activity and Actions Container */
    .content-sections-wrapper {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 1.5rem;
        margin-top: 1.5rem;
        clear: both;
    }
    
    .section-column {
        min-height: 300px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Section Headers */
    .section-header-custom {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.2rem;
        padding-bottom: 0.6rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.15);
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateX(3px);
    }
    
    /* Responsive Design */
    @media (max-width: 1024px) {
        .content-sections-wrapper {
            grid-template-columns: 1fr;
            gap: 1.2rem;
        }
        
        .profile-content-grid {
            grid-template-columns: 90px 1fr;
            gap: 1.2rem;
        }
        
        .profile-name-large {
            font-size: 1.75rem;
        }
    }
    
    @media (max-width: 768px) {
        .profile-content-grid {
            grid-template-columns: 80px 1fr;
            gap: 1rem;
        }
        
        .profile-email-large {
            justify-content: flex-start;
        }
        
        .profile-name-large {
            font-size: 1.5rem;
        }
        
        .status-badges-wrapper {
            justify-content: center;
            gap: 0.5rem;
        }
        
        .profile-main-wrapper {
            padding: 0.3rem;
        }
        
        .section-column {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Profile Header Section
    st.markdown('<div class="profile-main-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="profile-header-section"><div class="profile-content-grid">', unsafe_allow_html=True)
    
    # Left column: Avatar and change picture
    col_avatar, col_info = st.columns([1, 4])
    
    with col_avatar:
        st.markdown('<div class="profile-avatar-wrapper">', unsafe_allow_html=True)
        # Display profile picture or default avatar
        if profile_picture:
            st.markdown(f"""
            <div class="profile-avatar" style="background-image: url('{profile_picture}'); background-size: cover; background-position: center; font-size: 0; margin: 0 auto;">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="profile-avatar" style="margin: 0 auto;">\ud83d\udc64</div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upload profile picture - compact expander
        with st.expander("📸 Photo", expanded=False):
            uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg', 'gif'], key="profile_pic_upload", label_visibility="collapsed")
            
            if uploaded_file is not None:
                import base64
                from io import BytesIO
                from PIL import Image
                
                # Read and resize image
                image = Image.open(uploaded_file)
                image.thumbnail((400, 400), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                data_url = f"data:image/png;base64,{img_str}"
                
                # Save to database
                cursor.execute("UPDATE users SET profile_picture = ? WHERE user_id = ?", (data_url, user_id))
                conn.commit()
                st.success("✅ Updated!")
                st.rerun()
            
            if profile_picture:
                if st.button("🗑️ Remove", use_container_width=True, type="secondary", key="remove_pic"):
                    cursor.execute("UPDATE users SET profile_picture = NULL WHERE user_id = ?", (user_id,))
                    conn.commit()
                    st.rerun()
    
    with col_info:
        st.markdown(f'''
        <div class="profile-info-wrapper">
            <h1 class="profile-name-large">{name}</h1>
            <div class="profile-email-large">
                <span style="font-size: 1.4rem;">\u2709\ufe0f</span>
                <span>{email}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)  # Close grid and header section
    
    # Account Status Badges - Outside the header
    st.markdown(f"""
    <div class="status-badges-wrapper">
        <span class="stat-badge">📅 {days_active} Days Active</span>
        <span class="stat-badge">💼 Standard Account</span>
        <span class="stat-badge">✅ Active</span>
        <span class="stat-badge">🎯 Member Since {created_at.split()[0]}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Account Statistics with compact header
    st.markdown('''
    <div style="text-align: center; margin: 1.5rem 0 1rem;">
        <h2 style="
            font-size: 1.6rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.8rem;
            display: inline-block;
        ">📊 Account Statistics</h2>
        <div style="
            width: 80px;
            height: 3px;
            background: linear-gradient(90deg, #667eea 0%, #f5576c 100%);
            border-radius: 2px;
            margin: 0 auto;
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.5);
        "></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Initialize modules
    tm = TransactionManager(user_id)
    analytics = FinancialAnalytics(user_id)
    health_engine = HealthScoreEngine(user_id)
    
    transactions_df = tm.get_all_transactions()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_trans = len(transactions_df) if not transactions_df.empty else 0
        st.markdown(f"""
        <div class="profile-card" style="animation: slideInUp 0.5s ease-out 0.1s both;">
            <div class="profile-card-icon">💳</div>
            <div class="profile-card-header">Transactions</div>
            <div class="profile-card-value">{total_trans}</div>
        </div>
        <style>
        @keyframes slideInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    with col2:
        if not transactions_df.empty:
            stats = analytics.get_summary_stats()
            total_spent = f"₹{stats['total_spent']:,.0f}"
        else:
            total_spent = "₹0"
        st.markdown(f"""
        <div class="profile-card" style="animation: slideInUp 0.5s ease-out 0.2s both;">
            <div class="profile-card-icon">💰</div>
            <div class="profile-card-header">Total Spending</div>
            <div class="profile-card-value">{total_spent}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if not transactions_df.empty:
            score_data = health_engine.calculate_health_score()
            health_score = f"{score_data['final_score']:.1f}/100"
        else:
            health_score = "N/A"
        st.markdown(f"""
        <div class="profile-card" style="animation: slideInUp 0.5s ease-out 0.3s both;">
            <div class="profile-card-icon">💯</div>
            <div class="profile-card-header">Health Score</div>
            <div class="profile-card-value">{health_score}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if not transactions_df.empty:
            delivery_metrics = analytics.get_delivery_metrics()
            delivery_count = delivery_metrics['delivery_count']
        else:
            delivery_count = 0
        st.markdown(f"""
        <div class="profile-card" style="animation: slideInUp 0.5s ease-out 0.4s both;">
            <div class="profile-card-icon">🍕</div>
            <div class="profile-card-header">Deliveries</div>
            <div class="profile-card-value">{delivery_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two-Column Layout: Recent Activity + Account Actions
    st.markdown('<div class="content-sections-wrapper">', unsafe_allow_html=True)
    
    col_activity, col_actions = st.columns([1.5, 1])
    
    with col_activity:
        st.markdown('<div class="section-column">', unsafe_allow_html=True)
        st.markdown('''
        <h3 class="section-header-custom">
            <span style="font-size: 1.5rem;">🕐</span>
            <span>Recent Activity</span>
        </h3>
        ''', unsafe_allow_html=True)
        
        if not transactions_df.empty:
            recent_df = transactions_df.head(5)
            
            # Category styling
            category_styles = {
                'Food Delivery': {'icon': '🍕', 'bg': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', 'badge_bg': '#f5576c'},
                'Entertainment': {'icon': '🎬', 'bg': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'badge_bg': '#764ba2'},
                'Shopping': {'icon': '🛍️', 'bg': 'linear-gradient(135deg, #48c6ef 0%, #6f86d6 100%)', 'badge_bg': '#48c6ef'},
                'Transportation': {'icon': '🚗', 'bg': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', 'badge_bg': '#43e97b'},
                'Bills & Utilities': {'icon': '💡', 'bg': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', 'badge_bg': '#fa709a'},
                'Healthcare': {'icon': '⚕️', 'bg': 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)', 'badge_bg': '#30cfd0'},
                'Education': {'icon': '📚', 'bg': 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)', 'badge_bg': '#89d8f5'},
                'Other': {'icon': '💰', 'bg': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'badge_bg': '#667eea'}
            }
            
            # Display recent transactions
            for idx, row in enumerate(recent_df.iterrows()):
                _, row = row
                category = row['category']
                style = category_styles.get(category, category_styles['Other'])
                
                st.markdown(f"""
                <div class="activity-item" style="animation-delay: {idx * 0.1}s;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;">
                        <div style="display: flex; align-items: center; flex: 1;">
                            <div class="activity-category-icon" style="background: {style['bg']};">
                                {style['icon']}
                            </div>
                            <div>
                                <div style="margin-bottom: 0.4rem;">
                                    <span class="activity-date">{row['date']}</span>
                                </div>
                                <div class="activity-category-badge" style="background: {style['badge_bg']};">
                                    {category}
                                </div>
                            </div>
                        </div>
                        <div class="activity-amount">
                            ₹{row['amount']:,.2f}
                        </div>
                    </div>
                    <div class="activity-description" style="margin-top: 1rem; padding-left: 56px;">
                        {row['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No transactions yet. Start adding transactions to see your activity!")
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close section-column
    
    with col_actions:
        st.markdown('<div class="section-column">', unsafe_allow_html=True)
        st.markdown('''
        <h3 class="section-header-custom">
            <span style="font-size: 1.5rem;">⚙️</span>
            <span>Account Actions</span>
        </h3>
        ''', unsafe_allow_html=True)
        
        # Edit Name Section
        with st.expander("✏️ Edit Full Name", expanded=False):
            with st.form("edit_name_form"):
                new_name = st.text_input("New Name", value=name, max_chars=100)
                submit_name = st.form_submit_button("Update Name", use_container_width=True, type="primary")
                
                if submit_name:
                    if new_name and new_name.strip():
                        cursor.execute(
                            "UPDATE users SET name = ? WHERE user_id = ?",
                            (new_name.strip(), user_id)
                        )
                        conn.commit()
                        # Update session state
                        st.session_state.user_name = new_name.strip()
                        st.success("✅ Name updated successfully!")
                        st.rerun()
                    else:
                        st.error("Name cannot be empty")
        
        with st.expander("🔒 Change Password"):
            with st.form("change_password_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                submit = st.form_submit_button("Update Password", use_container_width=True, type="primary")
                
                if submit:
                    if not current_password or not new_password or not confirm_password:
                        st.error("All fields are required")
                    elif new_password != confirm_password:
                        st.error("New passwords don't match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        # Verify current password
                        from database.db import verify_password
                        if verify_password(email, current_password):
                            # Update password
                            import bcrypt
                            new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                            cursor.execute(
                                "UPDATE users SET password_hash = ? WHERE user_id = ?",
                                (new_hash, user_id)
                            )
                            conn.commit()
                            st.success("✅ Password updated successfully!")
                        else:
                            st.error("Current password is incorrect")
        
        with st.expander("📤 Export Account Data"):
            st.caption("Download all your data in CSV format")
            
            if st.button("📥 Download My Data", use_container_width=True, type="primary"):
                if not transactions_df.empty:
                    csv = tm.export_csv()
                    st.download_button(
                        label="Click to Download",
                        data=csv,
                        file_name=f"{name}_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.info("No data to export yet")
        
        with st.expander("🗑️ Delete Account", expanded=False):
            st.warning("⚠️ This action cannot be undone!")
            st.caption("Deleting your account will permanently remove all your data.")
            
            if st.button("Delete My Account", type="secondary", use_container_width=True):
                st.error("Account deletion feature is disabled in demo mode")
    
    # Close all layout wrapper divs
    st.markdown('</div>', unsafe_allow_html=True)  # Close account actions section-column
    st.markdown('</div>', unsafe_allow_html=True)  # Close content-sections-wrapper
    st.markdown('</div>', unsafe_allow_html=True)  # Close profile-main-wrapper
    
    conn.close()


def render_reports():
    """Render reports page"""
    user_id = get_current_user_id()
    user_name = get_current_user_name()
    user_email = get_current_user_email()
    
    st.markdown('<div class="main-header">📄 Financial Reports</div>', unsafe_allow_html=True)
    
    st.write("Generate comprehensive financial health reports with all your analytics and insights.")
    
    # Report options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Available Reports")
        
        with st.container():
            st.markdown("### PDF Financial Health Report")
            st.caption("Comprehensive report including:")
            st.markdown("""
            - Executive summary
            - Financial health score breakdown
            - Overspending risk analysis
            - Spending breakdown by category
            - Historical comparison
            - Behavioral insights and nudges
            - Personalized recommendations
            """)
            
            if st.button("📥 Generate PDF Report", type="primary", use_container_width=True):
                with st.spinner("Generating report..."):
                    try:
                        report_gen = ReportGenerator(user_id, user_name, user_email)
                        pdf_buffer = report_gen.generate_pdf_report()
                        
                        st.success("✅ Report generated successfully!")
                        
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_buffer,
                            file_name=f"financial_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
        
        st.markdown("---")
        
        with st.container():
            st.markdown("### CSV Transaction Export")
            st.caption("Export all your transactions for further analysis")
            
            tm = TransactionManager(user_id)
            csv = tm.export_csv()
            
            st.download_button(
                label="📥 Download Transactions CSV",
                data=csv,
                file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        st.subheader("📈 Quick Stats")
        
        health_engine = HealthScoreEngine(user_id)
        score_data = health_engine.calculate_health_score()
        
        st.metric("Health Score", f"{score_data['final_score']:.1f}/100")
        st.metric("Grade", score_data['grade'])
        st.metric("Status", score_data['status'])
        
        st.markdown("---")
        
        # Recent reports
        st.caption("Reports are generated on-demand and contain your latest financial data.")


def main():
    """Main application entry point"""
    
    # Check if user is logged in
    if not is_logged_in():
        # Show landing page or login page
        if st.session_state.get('show_login', False):
            # Back to landing button
            if st.button("← Back to Home", key="back_to_landing"):
                st.session_state.show_login = False
                st.rerun()
            render_login_page()
        else:
            render_landing_page()
        return
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Check if profile should be shown
    if st.session_state.get('show_profile', False):
        render_profile()
    # Render selected page
    elif page == "Dashboard":
        render_dashboard()
    elif page == "Chat Assistant":
        render_chat_assistant()
    elif page == "Transactions":
        render_transactions()
    elif page == "Insights":
        render_insights()
    elif page == "Reports":
        render_reports()


if __name__ == "__main__":
    main()
