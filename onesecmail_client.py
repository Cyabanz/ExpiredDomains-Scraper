#!/usr/bin/env python3
"""
1SecMail temporary email client
Uses the free 1secmail.com API
"""
import requests
import time
import re
import random

class OneSecMailClient:
    """
    Client for 1secmail.com temporary email service
    """
    
    def __init__(self):
        self.base_url = "https://www.1secmail.com/api/v1/"
        self.email_address = None
        self.login = None
        self.domain = None
    
    def get_email_address(self):
        """
        Generate a new random temporary email address
        """
        try:
            # Generate random email using 1secmail's genRandomMailbox
            response = requests.get(f"{self.base_url}?action=genRandomMailbox&count=1")
            emails = response.json()
            
            if emails and len(emails) > 0:
                self.email_address = emails[0]
                # Split email to get login and domain
                parts = self.email_address.split('@')
                if len(parts) == 2:
                    self.login = parts[0]
                    self.domain = parts[1]
                
                print(f"[1SecMail] Created temporary email: {self.email_address}")
                return self.email_address
            else:
                print("[1SecMail] Failed to generate email")
                return None
                
        except Exception as e:
            print(f"[1SecMail] Error creating email: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def check_email(self):
        """
        Check for new emails
        Returns list of email messages
        """
        if not self.login or not self.domain:
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}?action=getMessages&login={self.login}&domain={self.domain}"
            )
            messages = response.json()
            return messages if messages else []
            
        except Exception as e:
            print(f"[1SecMail] Error checking email: {e}")
            return []
    
    def fetch_email(self, email_id):
        """
        Fetch full content of an email by ID
        """
        if not self.login or not self.domain:
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}?action=readMessage&login={self.login}&domain={self.domain}&id={email_id}"
            )
            return response.json()
            
        except Exception as e:
            print(f"[1SecMail] Error fetching email: {e}")
            return None
    
    def wait_for_email(self, timeout=120, check_interval=10, keyword='expireddomains'):
        """
        Wait for an email containing specific keyword
        """
        print(f"[1SecMail] Waiting for email (timeout: {timeout}s)...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.check_email()
            
            if messages:
                print(f"[1SecMail] Found {len(messages)} message(s)")
                
                for msg in messages:
                    msg_from = msg.get('from', '')
                    msg_subject = msg.get('subject', '')
                    
                    if keyword.lower() in msg_from.lower() or keyword.lower() in msg_subject.lower():
                        # Fetch full message
                        full_msg = self.fetch_email(msg.get('id'))
                        return full_msg
                
                # Return first message if any
                if messages:
                    full_msg = self.fetch_email(messages[0].get('id'))
                    return full_msg
            
            time.sleep(check_interval)
        
        print(f"[1SecMail] Timeout reached")
        return None


def test_onesecmail():
    """Test the 1secmail client"""
    print("Testing 1SecMail...")
    
    try:
        client = OneSecMailClient()
        email = client.get_email_address()
        
        if email:
            print(f"✓ Successfully created: {email}")
            print(f"✓ Domain: {email.split('@')[1]}")
            
            # Check for messages
            messages = client.check_email()
            print(f"✓ Current messages: {len(messages)}")
            
            return True
        else:
            print("✗ Failed to create email")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    test_onesecmail()