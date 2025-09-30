#!/usr/bin/env python3
"""Quick test of account creation with pytempbox"""
import requests
import time
from tempmail_client import TempMailClient
import random
import string

# Generate credentials
username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$', k=12))

# Create temp email
email_client = TempMailClient()
email = email_client.get_email_address()

print(f"\n✓ Email: {email}")
print(f"✓ Username: {username}")
print(f"✓ Password: {password}")
print(f"✓ Domain: {email.split('@')[1]}")

# Register
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}

print("\n[1] Registering...")
data = {
    'signup': '1',
    'jscheck': '1',
    'login': username,
    'pass': password,
    'pass2': password,
    'email': email,
    'button_submit': 'Sign Up (Free)',
}

reg_resp = session.post('https://www.expireddomains.net/register/', headers=headers, data=data, allow_redirects=True)
print(f"Registration: {reg_resp.url}")

if 'success' in reg_resp.url:
    print("✓ Registration successful!")
else:
    print("? Registration status unclear")

# Try login immediately
print("\n[2] Testing immediate login...")
time.sleep(2)

login_data = {
    'login': username,
    'password': password,
    'redirect_to_url': '/home',
}

login_resp = session.post('https://www.expireddomains.net/logincheck/', headers=headers, data=login_data, allow_redirects=True)
print(f"Login result: {login_resp.url}")

if 'accountnotactivated' in login_resp.url:
    print("⚠️  Account needs activation")
    
    # Wait for email
    print("\n[3] Waiting 60 seconds for activation email...")
    
    for i in range(6):
        time.sleep(10)
        messages = email_client.check_email()
        
        print(f"Check {i+1}/6: ", end="")
        
        if messages:
            print(f"Found {len(messages)} email(s)!")
            for msg in messages:
                if isinstance(msg, dict):
                    print(f"  From: {msg.get('from', 'unknown')}")
                    print(f"  Subject: {msg.get('subject', 'no subject')}")
                else:
                    print(f"  Message: {str(msg)[:100]}")
        else:
            print("No emails yet")
    
    print("\n✓ Test complete")
    
elif 'activated' in login_resp.url or 'deactivated' in login_resp.url:
    print(f"Status from URL: {login_resp.url.split('/')[-1]}")
else:
    print("✓ Login might have worked!")
    
    # Test member access
    member_resp = session.get('https://member.expireddomains.net/', headers=headers, allow_redirects=True)
    print(f"Member area: {member_resp.url}")

print("\n" + "="*60)