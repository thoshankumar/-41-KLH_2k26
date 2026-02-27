"""
Email Parser Module
Parses delivery order emails from Gmail (Swiggy, Zomato, etc.)
"""

import re
from datetime import datetime
from config import DELIVERY_SERVICES, EMAIL_AMOUNT_PATTERNS
from modules.transaction_manager import TransactionManager


class EmailParser:
    """Parse delivery order emails and extract transaction data"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.transaction_manager = TransactionManager(user_id)
    
    def is_delivery_email(self, email_subject, email_sender):
        """Check if email is from a delivery service"""
        email_text = f"{email_subject} {email_sender}".lower()
        
        for service in DELIVERY_SERVICES:
            if service in email_text:
                return True, service
        
        return False, None
    
    def extract_amount(self, email_body):
        """
        Extract amount from email body using regex patterns
        
        Args:
            email_body: Email body text
        
        Returns:
            float amount or None
        """
        for pattern in EMAIL_AMOUNT_PATTERNS:
            matches = re.findall(pattern, email_body)
            if matches:
                # Get the last match (usually the total)
                amount_str = matches[-1]
                # Remove commas and convert to float
                amount = float(amount_str.replace(',', ''))
                return amount
        
        return None
    
    def parse_delivery_email(self, email_data):
        """
        Parse delivery email and extract transaction details
        
        Args:
            email_data: dict with 'subject', 'sender', 'body', 'date'
        
        Returns:
            dict with transaction data or None
        """
        subject = email_data.get('subject', '')
        sender = email_data.get('sender', '')
        body = email_data.get('body', '')
        email_date = email_data.get('date', datetime.now())
        
        # Check if it's a delivery email
        is_delivery, service = self.is_delivery_email(subject, sender)
        
        if not is_delivery:
            return None
        
        # Extract amount
        amount = self.extract_amount(body)
        
        if not amount:
            return None
        
        # Create transaction data
        transaction_data = {
            'date': email_date if isinstance(email_date, str) else email_date.strftime('%Y-%m-%d'),
            'category': 'Food Delivery',
            'amount': amount,
            'source': 'gmail_sync',
            'description': f"{service.title()} Order - {subject[:50]}"
        }
        
        return transaction_data
    
    def sync_gmail_orders(self, emails):
        """
        Sync multiple Gmail emails
        
        Args:
            emails: List of email dicts
        
        Returns:
            (success_count, skipped_count, message)
        """
        success_count = 0
        skipped_count = 0
        
        for email in emails:
            transaction_data = self.parse_delivery_email(email)
            
            if transaction_data:
                # Try to add transaction
                result = self.transaction_manager.add_transaction(
                    date=transaction_data['date'],
                    category=transaction_data['category'],
                    amount=transaction_data['amount'],
                    source=transaction_data['source'],
                    description=transaction_data['description']
                )
                
                if result:
                    success_count += 1
                else:
                    skipped_count += 1  # Duplicate
            else:
                skipped_count += 1
        
        return success_count, skipped_count, f"Synced {success_count} orders ({skipped_count} duplicates/non-delivery emails)"
    
    def simulate_gmail_sync(self):
        """
        Simulate Gmail sync with random sample data (for demo purposes)
        In production, this would use actual Gmail API
        
        Returns:
            (success_count, skipped_count, message)
        """
        import random
        from datetime import timedelta
        
        # Random delivery services
        services = [
            {'name': 'swiggy', 'sender': 'noreply@swiggy.in', 'subject_templates': [
                'Your Swiggy order has been delivered',
                'Swiggy Order #{order_id}',
                'Thank you for ordering with Swiggy'
            ]},
            {'name': 'zomato', 'sender': 'no-reply@zomato.com', 'subject_templates': [
                'Zomato Order Confirmation',
                'Your Zomato order #{order_id}',
                'Order delivered successfully'
            ]},
            {'name': 'ubereats', 'sender': 'uber@uber.com', 'subject_templates': [
                'Your Uber Eats order has arrived',
                'Uber Eats Order #{order_id}',
                'Thanks for ordering with Uber Eats'
            ]},
            {'name': 'dunzo', 'sender': 'hello@dunzo.in', 'subject_templates': [
                'Dunzo delivery completed',
                'Your Dunzo order #{order_id}',
                'Dunzo: Order delivered'
            ]}
        ]
        
        # Generate 2-4 random orders
        num_orders = random.randint(2, 4)
        sample_emails = []
        
        # Different price ranges for variety
        price_ranges = [
            (90, 250),      # Small orders (snacks, breakfast)
            (250, 450),     # Medium orders (lunch for 1-2)
            (450, 750),     # Large orders (dinner, multiple items)
            (750, 1200)     # Premium orders (party orders, multiple people)
        ]
        
        for i in range(num_orders):
            service = random.choice(services)
            order_id = random.randint(10000, 99999)
            
            # Randomly select a price range for this order
            min_price, max_price = random.choice(price_ranges)
            amount = random.randint(min_price, max_price)
            
            # Random date within last 5 days
            days_ago = random.randint(0, 5)
            order_date = datetime.now() - timedelta(days=days_ago)
            
            subject = random.choice(service['subject_templates']).format(order_id=order_id)
            body = f"Order total: ₹{amount}.00 has been charged. Thank you for ordering!"
            
            sample_emails.append({
                'subject': subject,
                'sender': service['sender'],
                'body': body,
                'date': order_date
            })
        
        return self.sync_gmail_orders(sample_emails)
    
    def get_gmail_sync_instructions(self):
        """Get instructions for setting up Gmail API"""
        instructions = """
### 📧 Gmail Sync Setup Instructions

To enable automatic delivery order sync from Gmail:

#### Step 1: Enable Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download `credentials.json`

#### Step 2: Configure Application
1. Place `credentials.json` in the project root
2. Install: `pip install google-api-python-client google-auth-oauthlib`
3. Run the sync to authenticate

#### Step 3: Automated Sync
- The app will scan for Swiggy, Zomato, Uber Eats emails
- Automatically extract order amounts
- Add to your transactions
- Prevent duplicates

#### Supported Services:
• Swiggy
• Zomato
• Uber Eats
• Dunzo

#### Demo Mode:
Click 'Simulate Gmail Sync' to test with sample data!
"""
        return instructions


# Gmail API Integration (Placeholder for production)
def setup_gmail_api():
    """
    Setup Gmail API connection (production implementation)
    This is a placeholder - actual implementation would use google-auth
    """
    try:
        # from google.auth.transport.requests import Request
        # from google.oauth2.credentials import Credentials
        # from google_auth_oauthlib.flow import InstalledAppFlow
        # from googleapiclient.discovery import build
        
        # SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        # Implementation would go here
        
        return None, "Gmail API not configured. Use simulation mode for demo."
    except Exception as e:
        return None, f"Gmail API error: {str(e)}"


def fetch_delivery_emails(gmail_service, days=30):
    """
    Fetch delivery emails from Gmail (production implementation)
    
    Args:
        gmail_service: Gmail API service object
        days: Number of days to look back
    
    Returns:
        List of email dicts
    """
    # Placeholder for actual Gmail API calls
    # Would query for emails from delivery services
    # Extract subject, sender, body, date
    
    return []
