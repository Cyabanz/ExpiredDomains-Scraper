#!/usr/bin/env python3
"""
Client for temp-mail.io service
Uses their API with real-looking email domains
"""
import requests
import time
import hashlib
import random
import string

class TempMailIOClient:
    """
    Client for temp-mail.io temporary email service
    """
    
    def __init__(self):
        self.base_url = "https://api.temp-mail.io/request"
        self.session = requests.Session()
        self.email_address = None
        self.token = None
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
    
    def get_email_address(self):
        """
        Generate a temporary email address
        """
        try:
            # Generate random email
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            
            # Try to get available domains
            response = self.session.get(
                f"{self.base_url}/domains/",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                domains = data.get('domains', [])
                
                if domains:
                    domain = random.choice(domains)
                    self.email_address = f"{username}@{domain}"
                    print(f"[TempMail.io] Created email: {self.email_address}")
                    return self.email_address
            
            # Fallback: use common temp-mail domain
            self.email_address = f"{username}@tempmail.io"
            print(f"[TempMail.io] Created email (fallback): {self.email_address}")
            return self.email_address
            
        except Exception as e:
            print(f"[TempMail.io] Error: {e}")
            return None
    
    def check_email(self):
        """
        Check for emails
        """
        if not self.email_address:
            return []
        
        try:
            # Calculate MD5 hash of email for API
            email_hash = hashlib.md5(self.email_address.lower().encode()).hexdigest()
            
            response = self.session.get(
                f"{self.base_url}/mail/id/{email_hash}/",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'emails' in data:
                    return data['emails']
            
            return []
            
        except Exception as e:
            print(f"[TempMail.io] Error checking email: {e}")
            return []


def test_tempmailio():
    """Test temp-mail.io"""
    print("="*70)
    print("Testing temp-mail.io Service")
    print("="*70)
    
    client = TempMailIOClient()
    email = client.get_email_address()
    
    if email:
        print(f"\n✓ Email created: {email}")
        print(f"✓ Domain: {email.split('@')[1]}")
        
        messages = client.check_email()
        print(f"✓ Messages: {len(messages)}")
        
        return True
    else:
        print("\n✗ Failed")
        return False


if __name__ == "__main__":
    test_tempmailio()