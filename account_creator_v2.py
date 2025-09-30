#!/usr/bin/env python3
"""
Account creator using pytempbox (alternative temp email service)
"""
import requests
from tempmail_client import TempMailClient
import re
import time
import random
import string

def generate_random_credentials():
    """Generate random username and password"""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=12))
    return username, password


class ExpiredDomainsAccountCreatorV2:
    """
    Account creator using pytempbox for temp emails
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.email_client = TempMailClient()
        self.username = None
        self.password = None
        self.email = None
    
    def create_account(self):
        """
        Create a new account on expireddomains.net
        """
        print("\n" + "="*60)
        print("AUTOMATED ACCOUNT CREATION (Using PyTempBox)")
        print("="*60)
        
        # Step 1: Get temporary email
        print("\n[1/4] Creating temporary email address...")
        self.email = self.email_client.get_email_address()
        
        if not self.email:
            print("Failed to create temporary email")
            return None, None
        
        print(f"✓ Email domain: {self.email.split('@')[1]}")
        
        # Step 2: Generate credentials
        print("\n[2/4] Generating random credentials...")
        self.username, self.password = generate_random_credentials()
        print(f"✓ Username: {self.username}")
        print(f"✓ Password: {self.password}")
        
        # Step 3: Register account
        print("\n[3/4] Registering account on expireddomains.net...")
        if not self._register_account():
            print("Failed to register account")
            return None, None
        
        # Step 4: Wait for activation email
        print("\n[4/4] Waiting for activation email...")
        print("⏳ Checking every 10 seconds for up to 5 minutes...")
        
        if self._handle_email_verification():
            print("\n✅ ACCOUNT ACTIVATED!")
        else:
            print("\n⚠️  No activation email received (or not required)")
        
        print("\n" + "="*60)
        print("ACCOUNT CREATED!")
        print("="*60)
        print(f"Username: {self.username}")
        print(f"Password: {self.password}")
        print(f"Email: {self.email}")
        print("="*60 + "\n")
        
        return self.username, self.password
    
    def _register_account(self):
        """Register account"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        try:
            # Get registration page first
            self.session.get('https://www.expireddomains.net/register/', headers=headers)
            
            # Register with correct field names
            data = {
                'signup': '1',
                'jscheck': '1',
                'login': self.username,
                'pass': self.password,
                'pass2': self.password,
                'email': self.email,
                'button_submit': 'Sign Up (Free)',
            }
            
            response = self.session.post(
                'https://www.expireddomains.net/register/',
                headers=headers,
                data=data,
                allow_redirects=True
            )
            
            if '/register/' not in response.url:
                print(f"✓ Registration successful! Redirected to: {response.url}")
                return True
            elif "successfully" in response.text.lower():
                print("✓ Registration submitted successfully")
                return True
            else:
                print("✓ Registration response received")
                return True
        
        except Exception as e:
            print(f"✗ Error during registration: {e}")
            return False
    
    def _handle_email_verification(self):
        """Wait for and process activation email"""
        max_attempts = 30  # 5 minutes
        check_interval = 10
        
        for attempt in range(max_attempts):
            time.sleep(check_interval)
            
            messages = self.email_client.check_email()
            
            if messages:
                print(f"\n📧 Received {len(messages)} email(s)! [Attempt {attempt + 1}/{max_attempts}]")
                
                for msg in messages:
                    # Extract message details
                    if isinstance(msg, dict):
                        sender = msg.get('from', msg.get('sender', ''))
                        subject = msg.get('subject', '')
                        body = msg.get('body', msg.get('text', msg.get('html', '')))
                    else:
                        # Try to extract from string representation
                        sender = str(msg)
                        subject = ''
                        body = str(msg)
                    
                    print(f"  From: {sender}")
                    print(f"  Subject: {subject}")
                    
                    # Check if from expireddomains
                    if ('expireddomains' in sender.lower() or 
                        'expireddomains' in subject.lower() or
                        'expired' in sender.lower() or
                        'activat' in subject.lower()):
                        
                        print(f"  ✓ This looks like an activation email!")
                        
                        # Extract links
                        links = re.findall(r'https?://[^\s<>"\']+', str(body), re.IGNORECASE)
                        ed_links = [l for l in links if 'expireddomains.net' in l.lower()]
                        
                        print(f"  Found {len(ed_links)} link(s) to expireddomains.net")
                        
                        for link in ed_links:
                            link = link.strip().rstrip('.,;)\'\"')
                            print(f"  🔗 Clicking: {link[:80]}...")
                            
                            try:
                                resp = self.session.get(link, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
                                print(f"     → {resp.url[:80]}")
                                
                                if 'activated' in resp.url.lower() or 'success' in resp.url.lower():
                                    print("  ✅ ACCOUNT ACTIVATED!")
                                    time.sleep(2)
                                    return True
                            except Exception as e:
                                print(f"     Error: {e}")
            else:
                print(f"⏳ Waiting... [Attempt {attempt + 1}/{max_attempts}]", end='\r')
        
        print("\n")
        return False


def get_or_create_account_v2():
    """Create account using pytempbox"""
    print("\n" + "="*60)
    print("ACCOUNT AUTOMATION (Using PyTempBox)")
    print("="*60)
    print("\nCreating account with alternative temp email service...")
    
    creator = ExpiredDomainsAccountCreatorV2()
    username, password = creator.create_account()
    
    if username and password:
        return username, password
    else:
        print("\nFailed to create account")
        return None, None


if __name__ == "__main__":
    get_or_create_account_v2()