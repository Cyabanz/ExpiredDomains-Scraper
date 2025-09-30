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
        
        # Step 4: Wait for and process activation email
        print("\n[4/4] Waiting for account activation email...")
        print("(Account status: not activated - email verification required)")
        
        if self._handle_email_verification():
            print("\n✅ Account activated successfully!")
        else:
            print("\n⚠️  No activation email received")
            print("   Account created but may need manual activation")
        
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
            # First, get the registration page
            reg_page = self.session.get('https://www.expireddomains.net/register/', headers=headers)
            
            # Prepare registration data with CORRECT field names
            data = {
                'signup': '1',
                'jscheck': '1',
                'login': self.username,
                'pass': self.password,
                'pass2': self.password,
                'email': self.email,
                'button_submit': 'Sign Up (Free)',
            }
            
            # Submit registration
            response = self.session.post(
                'https://www.expireddomains.net/register/',
                headers=headers,
                data=data,
                allow_redirects=True
            )
            
            # Check if registration was successful
            # If redirected away from /register/, it likely succeeded
            if '/register/' not in response.url:
                print(f"✓ Registration successful! Redirected to: {response.url}")
                return True
            elif "successfully" in response.text.lower() or "thank you" in response.text.lower():
                print("✓ Registration submitted successfully")
                return True
            elif "already" in response.text.lower() and "exists" in response.text.lower():
                print("⚠ Username or email already exists, generating new credentials...")
                self.username, self.password = generate_random_credentials()
                print(f"New username: {self.username}")
                return self._register_account()
            elif len(response.text) == 7217:
                # Same size as registration page = form validation error
                print("⚠ Registration form returned, checking for errors...")
                # Look for error messages
                if "invalid" in response.text.lower():
                    print("✗ Invalid input detected")
                return False
            else:
                print("✓ Registration response received")
                return True
                
        except Exception as e:
            print(f"✗ Error during registration: {e}")
            return False
    
    def _handle_email_verification(self):
        """
        Check for and handle email verification - EXTENDED WAIT
        """
        print("⏳ Waiting for activation email from expireddomains.net...")
        print("   (Checking every 10 seconds for up to 5 minutes)")
        
        # Check for emails - longer wait, less frequent checks
        max_attempts = 30  # 30 * 10 = 5 minutes
        check_interval = 10
        
        for attempt in range(max_attempts):
            time.sleep(check_interval)
            emails = self.email_client.check_email()
            
            if emails:
                print(f"\n📧 Checking {len(emails)} email(s)... [Attempt {attempt + 1}/{max_attempts}]")
                
                # Look through ALL emails
                for email_summary in emails:
                    email_from = email_summary.get('mail_from', '').lower()
                    email_subject = email_summary.get('mail_subject', '')
                    email_id = email_summary.get('mail_id')
                    
                    print(f"  📩 From: {email_from}")
                    print(f"     Subject: {email_subject}")
                    
                    # Check if it's from expireddomains (very broad check)
                    if ('expireddomains' in email_from or 
                        'expired' in email_from or
                        'domain' in email_from or
                        'activat' in email_subject.lower() or
                        'verif' in email_subject.lower() or
                        'confirm' in email_subject.lower() or
                        'expired' in email_subject.lower()):
                        
                        print(f"  ✓ This looks like an activation email!")
                        
                        # Fetch full email
                        email_data = self.email_client.fetch_email(email_id)
                        if email_data:
                            email_body = email_data.get('mail_body', '')
                            
                            # Look for ANY link to expireddomains.net
                            all_links = re.findall(r'https?://[^\s<>"\']+', email_body, re.IGNORECASE)
                            ed_links = [l for l in all_links if 'expireddomains.net' in l.lower()]
                            
                            print(f"  Found {len(ed_links)} link(s) to expireddomains.net")
                            
                            if ed_links:
                                for link in ed_links:
                                    verification_link = link.strip().rstrip('.,;)\'\"')
                                    print(f"  🔗 Trying link: {verification_link[:80]}...")
                                    
                                    try:
                                        headers = {
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                                        }
                                        response = self.session.get(verification_link, headers=headers, allow_redirects=True)
                                        print(f"     Response: {response.status_code} -> {response.url[:80]}")
                                        
                                        if 'activated' in response.url.lower() or 'success' in response.url.lower():
                                            print("  ✅ ACCOUNT ACTIVATED!")
                                            time.sleep(3)
                                            return True
                                    except Exception as e:
                                        print(f"     Error: {e}")
                                        continue
            else:
                print(f"⏳ No emails yet... [Attempt {attempt + 1}/{max_attempts}]", end='\r')
        
        print("\n\n⚠️  No activation email received after 5 minutes")
        print("💡 The site may be blocking temporary email addresses")
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