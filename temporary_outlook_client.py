#!/usr/bin/env python3
"""
Client for 22.do temporary Outlook email service
"""
import requests
import time
import re
import random
import string

class TemporaryOutlookClient:
    """
    Client for 22.do/temporary-outlook service
    """
    
    def __init__(self):
        self.base_url = "https://22.do"
        self.session = requests.Session()
        self.email_address = None
        self.cookies = {}
        
        # Set realistic headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://22.do/',
        }
    
    def get_email_address(self):
        """
        Get a temporary Outlook email address from 22.do
        """
        try:
            # Try to access the temporary-outlook page
            response = self.session.get(
                f"{self.base_url}/temporary-outlook",
                headers=self.headers,
                timeout=30
            )
            
            print(f"[22.do] Service status: {response.status_code}")
            
            if response.status_code == 200:
                # Look for email address in the response
                # The service might generate it on page load or via API
                
                # Try to find email in page content
                email_pattern = r'([a-zA-Z0-9._-]+@outlook\.com)'
                emails = re.findall(email_pattern, response.text)
                
                if emails:
                    self.email_address = emails[0]
                    print(f"[22.do] Found email: {self.email_address}")
                    return self.email_address
                
                # Check if there's an API endpoint
                api_pattern = r'/api/[^\s"\'<>]+'
                apis = re.findall(api_pattern, response.text)
                
                if apis:
                    print(f"[22.do] Found API endpoints: {apis[:3]}")
                    
                    # Try the first API endpoint
                    for api_path in apis[:3]:
                        try:
                            api_response = self.session.get(
                                f"{self.base_url}{api_path}",
                                headers=self.headers,
                                timeout=10
                            )
                            
                            if api_response.status_code == 200:
                                # Check if response contains email
                                data = api_response.json() if 'json' in api_response.headers.get('content-type', '') else None
                                if data:
                                    # Look for email in JSON response
                                    email_keys = ['email', 'address', 'mail', 'emailAddress']
                                    for key in email_keys:
                                        if key in data:
                                            self.email_address = data[key]
                                            print(f"[22.do] Got email from API: {self.email_address}")
                                            return self.email_address
                        except:
                            continue
                
                # If no email found, try to generate one using the service's method
                # Check if there's a JavaScript variable with the email
                js_email_pattern = r'email\s*[:=]\s*["\']([a-zA-Z0-9._-]+@outlook\.com)["\']'
                js_emails = re.findall(js_email_pattern, response.text, re.IGNORECASE)
                
                if js_emails:
                    self.email_address = js_emails[0]
                    print(f"[22.do] Extracted email from JS: {self.email_address}")
                    return self.email_address
                
                # Last resort: save page content for inspection
                with open('/workspace/22do_page.html', 'w') as f:
                    f.write(response.text[:5000])  # First 5000 chars
                print("[22.do] Saved page content to 22do_page.html for inspection")
                
                print("[22.do] Could not find email address automatically")
                print("[22.do] The service may require JavaScript or manual interaction")
                return None
            else:
                print(f"[22.do] Failed to access service: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[22.do] Error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def check_email(self):
        """
        Check for emails in the inbox
        """
        if not self.email_address:
            return []
        
        try:
            # Try to get inbox
            # This will depend on how the service exposes emails
            
            # Try common patterns
            endpoints = [
                f"/api/inbox/{self.email_address.split('@')[0]}",
                f"/api/messages",
                f"/inbox",
            ]
            
            for endpoint in endpoints:
                try:
                    response = self.session.get(
                        f"{self.base_url}{endpoint}",
                        headers=self.headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        if 'json' in response.headers.get('content-type', ''):
                            data = response.json()
                            if isinstance(data, list) and len(data) > 0:
                                print(f"[22.do] Found messages via {endpoint}")
                                return data
                except:
                    continue
            
            return []
            
        except Exception as e:
            print(f"[22.do] Error checking email: {e}")
            return []
    
    def wait_for_email(self, timeout=300, check_interval=15):
        """
        Wait for an email to arrive
        """
        print(f"[22.do] Waiting for email (timeout: {timeout}s, checking every {check_interval}s)...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.check_email()
            
            if messages:
                print(f"[22.do] Received {len(messages)} message(s)")
                return messages[0] if messages else None
            
            time.sleep(check_interval)
        
        print(f"[22.do] Timeout reached")
        return None


def test_22do():
    """Test the 22.do service"""
    print("="*70)
    print("Testing 22.do Temporary Outlook Service")
    print("="*70)
    
    client = TemporaryOutlookClient()
    email = client.get_email_address()
    
    if email:
        print(f"\n✓ Successfully obtained email: {email}")
        print(f"✓ Domain: {email.split('@')[1] if '@' in email else 'unknown'}")
        
        # Check for existing messages
        messages = client.check_email()
        print(f"✓ Current inbox: {len(messages)} message(s)")
        
        return True
    else:
        print("\n✗ Could not obtain email address")
        print("The service may require:")
        print("  - Browser automation (Selenium)")
        print("  - JavaScript execution")
        print("  - CAPTCHA solving")
        print("  - Or may not have a public API")
        return False


if __name__ == "__main__":
    test_22do()