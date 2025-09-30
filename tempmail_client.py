#!/usr/bin/env python3
"""
Temporary email client using pytempbox
Alternative to Guerrilla Mail that might not be blocked
"""
import time
import re

try:
    from pytempbox import PyTempBox
    PYTEMPBOX_AVAILABLE = True
except ImportError:
    PYTEMPBOX_AVAILABLE = False
    print("pytempbox not available, falling back to alternative")

class TempMailClient:
    """
    Temporary email client using pytempbox
    """
    
    def __init__(self):
        if PYTEMPBOX_AVAILABLE:
            self.client = PyTempBox()
            self.email_address = None
        else:
            raise ImportError("pytempbox not installed")
    
    def get_email_address(self):
        """
        Generate a new temporary email address
        """
        try:
            self.email_address = self.client.generate_email()
            print(f"[TempMail] Created temporary email: {self.email_address}")
            return self.email_address
        except Exception as e:
            print(f"[TempMail] Error creating email: {e}")
            return None
    
    def check_email(self):
        """
        Check for new emails
        Returns list of email messages
        """
        if not self.email_address:
            return []
        
        try:
            messages = self.client.get_messages(self.email_address)
            return messages if messages else []
        except Exception as e:
            print(f"[TempMail] Error checking email: {e}")
            return []
    
    def wait_for_email(self, timeout=120, check_interval=10, keyword='expireddomains'):
        """
        Wait for an email containing specific keyword
        """
        print(f"[TempMail] Waiting for email (timeout: {timeout}s)...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.check_email()
            
            if messages:
                print(f"[TempMail] Found {len(messages)} message(s)")
                
                # Look for messages from expireddomains
                for msg in messages:
                    sender = msg.get('from', '') if isinstance(msg, dict) else str(msg)
                    subject = msg.get('subject', '') if isinstance(msg, dict) else ''
                    
                    if keyword.lower() in sender.lower() or keyword.lower() in subject.lower():
                        return msg
                
                # Return first message if no specific match
                if messages:
                    return messages[0]
            
            time.sleep(check_interval)
        
        print(f"[TempMail] Timeout reached")
        return None


def test_tempmail():
    """Test the temp mail client"""
    print("Testing pytempbox...")
    
    try:
        client = TempMailClient()
        email = client.get_email_address()
        
        if email:
            print(f"✓ Successfully created: {email}")
            print("✓ Domain:", email.split('@')[1] if '@' in email else 'unknown')
            
            # Check for messages
            messages = client.check_email()
            print(f"✓ Messages: {len(messages)}")
            
            return True
        else:
            print("✗ Failed to create email")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    test_tempmail()