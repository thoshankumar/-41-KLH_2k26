"""
Authentication Module for AI Behavioral Finance Coach
Handles user registration, login, logout, and session management
"""

import streamlit as st
from database.db import get_user_by_email, create_user, verify_password
from config import SESSION_KEYS


def initialize_session():
    """Initialize session state variables"""
    if SESSION_KEYS["logged_in"] not in st.session_state:
        st.session_state[SESSION_KEYS["logged_in"]] = False
    if SESSION_KEYS["user_id"] not in st.session_state:
        st.session_state[SESSION_KEYS["user_id"]] = None
    if SESSION_KEYS["user_name"] not in st.session_state:
        st.session_state[SESSION_KEYS["user_name"]] = None
    if SESSION_KEYS["user_email"] not in st.session_state:
        st.session_state[SESSION_KEYS["user_email"]] = None


def is_logged_in():
    """Check if user is logged in"""
    return st.session_state.get(SESSION_KEYS["logged_in"], False)


def get_current_user_id():
    """Get current logged-in user ID"""
    return st.session_state.get(SESSION_KEYS["user_id"])


def get_current_user_name():
    """Get current logged-in user name"""
    return st.session_state.get(SESSION_KEYS["user_name"])


def get_current_user_email():
    """Get current logged-in user email"""
    return st.session_state.get(SESSION_KEYS["user_email"])


def login(email, password):
    """
    Authenticate user and create session
    
    Args:
        email: User email
        password: Plain text password
    
    Returns:
        (success: bool, message: str)
    """
    if not email or not password:
        return False, "Please enter both email and password"
    
    # Retrieve user from database
    user = get_user_by_email(email)
    
    if not user:
        return False, "Invalid email or password"
    
    # Verify password
    if not verify_password(password, user['password_hash']):
        return False, "Invalid email or password"
    
    # Create session
    st.session_state[SESSION_KEYS["logged_in"]] = True
    st.session_state[SESSION_KEYS["user_id"]] = user['user_id']
    st.session_state[SESSION_KEYS["user_name"]] = user['name']
    st.session_state[SESSION_KEYS["user_email"]] = user['email']
    
    return True, f"Welcome back, {user['name']}!"


def register(name, email, password, confirm_password):
    """
    Register new user
    
    Args:
        name: User full name
        email: User email
        password: Password
        confirm_password: Password confirmation
    
    Returns:
        (success: bool, message: str)
    """
    # Validation
    if not all([name, email, password, confirm_password]):
        return False, "Please fill in all fields"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    
    if '@' not in email or '.' not in email:
        return False, "Please enter a valid email address"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if password != confirm_password:
        return False, "Passwords do not match"
    
    # Check if user already exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return False, "Email already registered. Please login instead."
    
    # Create user
    user_id = create_user(name, email, password)
    
    if user_id:
        return True, "Registration successful! Please login."
    else:
        return False, "Registration failed. Please try again."


def logout():
    """Logout current user and clear session"""
    st.session_state[SESSION_KEYS["logged_in"]] = False
    st.session_state[SESSION_KEYS["user_id"]] = None
    st.session_state[SESSION_KEYS["user_name"]] = None
    st.session_state[SESSION_KEYS["user_email"]] = None
    
    # Clear other session data
    for key in list(st.session_state.keys()):
        if key not in SESSION_KEYS.values():
            del st.session_state[key]


def require_login():
    """
    Decorator/helper to require authentication
    Call at the start of protected pages
    """
    if not is_logged_in():
        st.warning("⚠️ Please login to access this page")
        st.stop()


def render_login_page():
    """Render modern login and registration UI"""
    
    # Create split-screen layout
    st.markdown("""
    <div class="login-container">
        <div class="login-glass-card">
            <div class="login-split">
                <div class="login-left">
                    <div class="login-brand">
                        <h1>🏦 AI Finance Coach</h1>
                        <p>Transform your financial behavior with intelligent insights powered by AI</p>
                    </div>
                    <div class="login-features">
                        <div class="feature-item">
                            <div class="feature-icon">💯</div>
                            <div class="feature-text">
                                <h3>Financial Health Score</h3>
                                <p>Real-time scoring from 0-100 based on your spending patterns</p>
                            </div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🤖</div>
                            <div class="feature-text">
                                <h3>AI-Powered Chatbot</h3>
                                <p>Natural conversations about your finances, anytime</p>
                            </div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🔮</div>
                            <div class="feature-text">
                                <h3>Predictive Analytics</h3>
                                <p>Machine learning forecasts your overspending risks</p>
                            </div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">📊</div>
                            <div class="feature-text">
                                <h3>Interactive Dashboards</h3>
                                <p>Beautiful visualizations with actionable insights</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="login-right">
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab selection
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = 'login'
    
    # Header
    st.markdown("""
    <div class="login-header">
        <h2>Welcome Back!</h2>
        <p>Sign in to access your personalized financial dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔐 Login", key="login_tab", use_container_width=True, 
                     type="primary" if st.session_state.auth_tab == 'login' else "secondary"):
            st.session_state.auth_tab = 'login'
            st.rerun()
    
    with col2:
        if st.button("📝 Register", key="register_tab", use_container_width=True,
                     type="primary" if st.session_state.auth_tab == 'register' else "secondary"):
            st.session_state.auth_tab = 'register'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Login Form
    if st.session_state.auth_tab == 'login':
        with st.form("login_form", clear_on_submit=False):
            st.markdown('<p class="form-label">📧 Email Address</p>', unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Enter your email", label_visibility="collapsed")
            
            st.markdown('<p class="form-label">🔒 Password</p>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 Sign In", use_container_width=True, type="primary")
            
            if submit:
                if email and password:
                    success, message = login(email, password)
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please fill in all fields")
        
        # Demo credentials
        st.markdown("""
        <div class="demo-card">
            <h4>💡 Try Demo Account</h4>
            <div class="demo-credentials">
                <div class="credential-item">📧 Email: demo@financecoach.ai</div>
                <div class="credential-item">🔑 Password: demo123</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Register Form
    else:
        with st.form("register_form", clear_on_submit=False):
            st.markdown('<p class="form-label">👤 Full Name</p>', unsafe_allow_html=True)
            name = st.text_input("Name", placeholder="Enter your full name", label_visibility="collapsed")
            
            st.markdown('<p class="form-label">📧 Email Address</p>', unsafe_allow_html=True)
            reg_email = st.text_input("Email", placeholder="Enter your email", label_visibility="collapsed", key="reg_email")
            
            st.markdown('<p class="form-label">🔒 Password</p>', unsafe_allow_html=True)
            reg_password = st.text_input("Password", type="password", placeholder="Min 6 characters", label_visibility="collapsed", key="reg_password")
            
            st.markdown('<p class="form-label">🔒 Confirm Password</p>', unsafe_allow_html=True)
            confirm_password = st.text_input("Confirm", type="password", placeholder="Re-enter password", label_visibility="collapsed", key="confirm_password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            register_submit = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")
            
            if register_submit:
                if all([name, reg_email, reg_password, confirm_password]):
                    success, message = register(name, reg_email, reg_password, confirm_password)
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.session_state.auth_tab = 'login'
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please fill in all fields")
        
        # Info message
        st.info("🔐 Your data is encrypted and secure. We take privacy seriously.")
    
    # Footer
    st.markdown("""
    <div class="login-footer">
        <p>🛡️ Secured with bcrypt encryption | 🚀 Powered by Streamlit & AI</p>
    </div>
    """, unsafe_allow_html=True)
