#!/usr/bin/env python3
"""
Installation and Testing Script for AI Behavioral Finance Coach
Verifies all dependencies and performs basic system check
"""

import sys
import subprocess
import importlib

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_imports():
    """Verify all required modules can be imported"""
    print("\n🔍 Verifying module imports...")
    
    modules_to_check = [
        'streamlit',
        'pandas',
        'numpy',
        'sklearn',
        'plotly',
        'bcrypt',
        'reportlab',
        'scipy'
    ]
    
    all_ok = True
    for module in modules_to_check:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} - Not found")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Verify project structure"""
    print("\n🔍 Checking project structure...")
    
    import os
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'database/db.py',
        'database/schema.sql',
        'modules/auth.py',
        'modules/transaction_manager.py',
        'modules/analytics.py',
        'modules/anomaly.py',
        'modules/health_score.py',
        'modules/prediction.py',
        'modules/behavior_engine.py',
        'modules/chatbot.py',
        'modules/email_parser.py',
        'modules/report_generator.py'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Missing")
            all_ok = False
    
    return all_ok

def test_database_init():
    """Test database initialization"""
    print("\n🔍 Testing database initialization...")
    
    try:
        from database.db import initialize_database, get_user_by_email
        
        # Initialize database
        initialize_database()
        
        # Check if demo user exists
        demo_user = get_user_by_email("demo@financecoach.ai")
        if demo_user:
            print("  ✅ Database initialized")
            print("  ✅ Demo user created")
            return True
        else:
            print("  ❌ Demo user not found")
            return False
            
    except Exception as e:
        print(f"  ❌ Database initialization failed: {str(e)}")
        return False

def test_ml_model():
    """Test ML model creation"""
    print("\n🔍 Testing ML model...")
    
    try:
        import os
        # Create a dummy user ID for testing
        from modules.prediction import OverspendPredictor
        
        # This will create the model if it doesn't exist
        predictor = OverspendPredictor(user_id=1)
        
        if os.path.exists('models/overspend_model.pkl'):
            print("  ✅ ML model created/loaded successfully")
            return True
        else:
            print("  ❌ ML model file not created")
            return False
            
    except Exception as e:
        print(f"  ❌ ML model test failed: {str(e)}")
        return False

def print_summary():
    """Print final summary"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("  1. Run the application:")
    print("     streamlit run app.py")
    print("\n  2. Or use the run script:")
    print("     ./run.sh  (Mac/Linux)")
    print("     run.bat   (Windows)")
    print("\n  3. Login with demo account:")
    print("     Email: demo@financecoach.ai")
    print("     Password: demo123")
    print("\n  4. Add transactions and explore!")
    print("\n📖 Documentation:")
    print("  - README.md - Full documentation")
    print("  - QUICKSTART.md - Quick start guide")
    print("  - PROJECT_SUMMARY.md - Complete feature list")
    print("\n" + "="*60)

def main():
    """Main setup process"""
    print("="*60)
    print("🏦 AI BEHAVIORAL FINANCE COACH")
    print("   Installation & Setup Script")
    print("="*60)
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", install_requirements),
        ("Module Imports", check_imports),
        ("Project Structure", check_project_structure),
        ("Database", test_database_init),
        ("ML Model", test_ml_model)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} check failed with error: {str(e)}")
            results.append((name, False))
    
    # Print results summary
    print("\n" + "="*60)
    print("SETUP RESULTS")
    print("="*60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:.<40} {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✅ All checks passed!")
        print_summary()
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
