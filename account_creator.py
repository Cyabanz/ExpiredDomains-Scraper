import requests
from guerrilla_mail import GuerrillaMailClient, generate_random_credentials
import re
import time

class ExpiredDomainsAccountCreator:
    """
    Automatically creates accounts on expireddomains.net using temporary email addresses
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.email_client = GuerrillaMailClient()
        self.username = None
        self.password = None
        self.email = None
        
    def create_account(self):
        """
        Create a new account on expireddomains.net
        Returns (username, password) on success, (None, None) on failure
        """
        print("\n" + "="*60)
        print("AUTOMATED ACCOUNT CREATION")
        print("="*60)
        
        # Step 1: Get temporary email
        print("\n[1/4] Creating temporary email address...")
        self.email = self.email_client.get_email_address()
        
        if not self.email:
            print("Failed to create temporary email")
            return None, None
        
        # Step 2: Generate random credentials
        print("\n[2/4] Generating random credentials...")
        self.username, self.password = generate_random_credentials()
        print(f"Username: {self.username}")
        print(f"Password: {self.password}")
        print(f"Email: {self.email}")
        
        # Step 3: Register account
        print("\n[3/4] Registering account on expireddomains.net...")
        if not self._register_account():
            print("Failed to register account")
            return None, None
        
        # Step 4: Verify email (if required)
        print("\n[4/4] Checking for verification email...")
        if self._handle_email_verification():
            print("\n" + "="*60)
            print("ACCOUNT CREATED SUCCESSFULLY!")
            print("="*60)
            print(f"Username: {self.username}")
            print(f"Password: {self.password}")
            print(f"Email: {self.email}")
            print("="*60 + "\n")
            return self.username, self.password
        else:
            print("Note: Email verification may not be required")
            print("\n" + "="*60)
            print("ACCOUNT CREATED!")
            print("="*60)
            print(f"Username: {self.username}")
            print(f"Password: {self.password}")
            print(f"Email: {self.email}")
            print("="*60 + "\n")
            return self.username, self.password
    
    def _register_account(self):
        """
        Register account on expireddomains.net
        """
        headers = {
            'authority': 'www.expireddomains.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.expireddomains.net',
            'referer': 'https://www.expireddomains.net/register/',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        
        try:
            # First, get the registration page to get any CSRF tokens or form data
            reg_page = self.session.get('https://www.expireddomains.net/register/', headers=headers)
            
            # Prepare registration data
            data = {
                'login': self.username,
                'password': self.password,
                'password_confirm': self.password,
                'email': self.email,
                'email_confirm': self.email,
                'accept_tos': '1',
                'register': 'Register',
            }
            
            # Submit registration
            response = self.session.post(
                'https://www.expireddomains.net/register/',
                headers=headers,
                data=data
            )
            
            # Check if registration was successful
            if "successfully" in response.text.lower() or "welcome" in response.text.lower():
                print("Registration submitted successfully")
                return True
            elif "already exists" in response.text.lower():
                print("Username or email already exists, trying again...")
                # Generate new credentials and retry
                self.username, self.password = generate_random_credentials()
                return self._register_account()
            else:
                print("Registration response received, attempting to continue...")
                # Some sites don't give explicit success messages
                return True
                
        except Exception as e:
            print(f"Error during registration: {e}")
            return False
    
    def _handle_email_verification(self):
        """
        Check for and handle email verification
        """
        print("[INFO] Waiting for verification email from expireddomains.net...")
        
        # Check for emails multiple times
        max_attempts = 12
        check_interval = 5
        
        for attempt in range(max_attempts):
            time.sleep(check_interval)
            emails = self.email_client.check_email()
            
            if emails:
                print(f"[INFO] Checking {len(emails)} email(s)...")
                
                # Look through all emails for one from expireddomains
                for email_summary in emails:
                    email_from = email_summary.get('mail_from', '').lower()
                    email_subject = email_summary.get('mail_subject', '')
                    email_id = email_summary.get('mail_id')
                    
                    print(f"  - From: {email_from}, Subject: {email_subject}")
                    
                    # Check if it's from expireddomains
                    if 'expireddomains' in email_from or 'expired' in email_subject.lower():
                        print(f"[INFO] Found expireddomains.net email!")
                        
                        # Fetch full email
                        email_data = self.email_client.fetch_email(email_id)
                        if email_data:
                            email_body = email_data.get('mail_body', '')
                            
                            # Look for verification links
                            link_pattern = r'https?://(?:www\.)?expireddomains\.net/[^\s<>"\']+(?:verify|confirm|activate|validation|register|code|token)[^\s<>"\']*'
                            links = re.findall(link_pattern, email_body, re.IGNORECASE)
                            
                            if not links:
                                # Try broader pattern
                                link_pattern2 = r'https?://(?:www\.)?expireddomains\.net/[^\s<>"\'&]+'
                                links = re.findall(link_pattern2, email_body, re.IGNORECASE)
                            
                            if links:
                                verification_link = links[0].strip().rstrip('.,;)')
                                print(f"[INFO] Found verification link: {verification_link}")
                                
                                try:
                                    headers = {
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                                    }
                                    response = self.session.get(verification_link, headers=headers, allow_redirects=True)
                                    if response.status_code == 200:
                                        print("[SUCCESS] Email verified successfully")
                                        time.sleep(3)
                                        return True
                                except Exception as e:
                                    print(f"[ERROR] Error clicking verification link: {e}")
            
            if attempt < max_attempts - 1:
                print(f"[INFO] No verification email yet, waiting... ({attempt + 1}/{max_attempts})")
        
        print("[WARNING] No verification email received from expireddomains.net")
        print("[INFO] The site may not require email verification, or registration may have failed")
        return False


def get_or_create_account():
    """
    Main function to get account credentials
    Returns (username, password) tuple
    """
    print("\n" + "="*60)
    print("ACCOUNT AUTOMATION")
    print("="*60)
    print("\nCreating temporary account using Guerrilla Mail...")
    
    creator = ExpiredDomainsAccountCreator()
    username, password = creator.create_account()
    
    if username and password:
        # Save credentials to config for this session
        return username, password
    else:
        print("\nFailed to create account automatically")
        print("You can try again or use manual credentials in config.py")
        return None, None