import requests
import time
import random
import string

class GuerrillaMailClient:
    """
    Client for interacting with Guerrilla Mail API to create temporary email addresses
    """
    
    def __init__(self):
        self.base_url = "https://api.guerrillamail.com/ajax.php"
        self.session = requests.Session()
        self.email_address = None
        self.sid_token = None
        
    def get_email_address(self, preferred_domain='sharklasers.com'):
        """
        Get a new temporary email address from Guerrilla Mail
        Uses sharklasers.com by default (looks more legitimate than guerrillamailblock.com)
        Returns the email address
        """
        params = {
            'f': 'get_email_address',
            'ip': '127.0.0.1',
            'agent': 'Mozilla/5.0'
        }
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            self.email_address = data.get('email_addr')
            self.sid_token = data.get('sid_token')
            
            # Try to change to a more legitimate-looking domain
            if preferred_domain and '@guerrillamailblock.com' in self.email_address:
                email_user = self.email_address.split('@')[0]
                # set_email_user changes the domain to sharklasers automatically for custom users
                self.set_email_user(email_user)
            
            print(f"[GuerrillaMail] Created temporary email: {self.email_address}")
            return self.email_address
            
        except Exception as e:
            print(f"[GuerrillaMail] Error creating email address: {e}")
            return None
    
    def set_email_user(self, username):
        """
        Set a custom username for the email address
        """
        params = {
            'f': 'set_email_user',
            'email_user': username,
            'sid_token': self.sid_token
        }
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            self.email_address = data.get('email_addr')
            print(f"[GuerrillaMail] Updated email to: {self.email_address}")
            return self.email_address
            
        except Exception as e:
            print(f"[GuerrillaMail] Error setting email user: {e}")
            return None
    
    def check_email(self, seq=0):
        """
        Check for new emails
        seq: sequence number to get emails after
        Returns list of emails
        """
        params = {
            'f': 'check_email',
            'seq': seq,
            'sid_token': self.sid_token
        }
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data.get('list', [])
            
        except Exception as e:
            print(f"[GuerrillaMail] Error checking email: {e}")
            return []
    
    def fetch_email(self, email_id):
        """
        Fetch the full content of an email by ID
        """
        params = {
            'f': 'fetch_email',
            'email_id': email_id,
            'sid_token': self.sid_token
        }
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return data
            
        except Exception as e:
            print(f"[GuerrillaMail] Error fetching email: {e}")
            return None
    
    def wait_for_email(self, timeout=120, check_interval=5):
        """
        Wait for an email to arrive
        Returns the first email received
        """
        print(f"[GuerrillaMail] Waiting for email (timeout: {timeout}s)...")
        start_time = time.time()
        seq = 0
        
        while time.time() - start_time < timeout:
            emails = self.check_email(seq)
            
            if emails:
                print(f"[GuerrillaMail] Received {len(emails)} email(s)")
                # Fetch full content of first email
                email_data = self.fetch_email(emails[0]['mail_id'])
                return email_data
            
            time.sleep(check_interval)
        
        print(f"[GuerrillaMail] Timeout reached, no email received")
        return None


def generate_random_credentials():
    """
    Generate random username and password for account creation
    """
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=12))
    
    return username, password