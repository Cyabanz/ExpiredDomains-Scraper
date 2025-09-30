#!/usr/bin/env python3
"""Test if temp-mail.io receives activation emails from expireddomains.net"""
import requests
import time
import re
from tempmailio_client import TempMailIOClient
import random
import string

print("="*70)
print("TESTING: temp-mail.io with ExpiredDomains Activation")
print("="*70)

# Create temp email
email_client = TempMailIOClient()
email = email_client.get_email_address()

if not email:
    print("✗ Failed to create email")
    exit(1)

# Generate credentials
username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$', k=12))

print(f"\n✓ Email: {email}")
print(f"✓ Username: {username}")
print(f"✓ Password: {password}")
print(f"✓ Domain: {email.split('@')[1]}")

# Register on expireddomains.net
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}

print("\n[1/3] Registering account...")
reg_data = {
    'signup': '1',
    'jscheck': '1',
    'login': username,
    'pass': password,
    'pass2': password,
    'email': email,
    'button_submit': 'Sign Up (Free)',
}

reg_resp = session.post(
    'https://www.expireddomains.net/register/',
    headers=headers,
    data=reg_data,
    allow_redirects=True
)

if 'success' in reg_resp.url:
    print("✓ Registration successful!")
else:
    print(f"? Registration: {reg_resp.url}")

# Try immediate login
print("\n[2/3] Testing immediate login...")
time.sleep(2)

login_data = {
    'login': username,
    'password': password,
    'redirect_to_url': '/home',
}

login_resp = session.post(
    'https://www.expireddomains.net/logincheck/',
    headers=headers,
    data=login_data,
    allow_redirects=True
)

print(f"Login status: {login_resp.url}")

if 'accountnotactivated' in login_resp.url:
    print("⚠️  Account needs activation (expected)")
    
    # Wait for activation email
    print("\n[3/3] Waiting for activation email...")
    print("Checking every 10 seconds for up to 2 minutes...\n")
    
    for i in range(12):  # 2 minutes
        time.sleep(10)
        
        messages = email_client.check_email()
        
        print(f"Check {i+1}/12: ", end="")
        
        if messages:
            print(f"✓ Found {len(messages)} email(s)!")
            
            for msg in messages:
                sender = msg.get('from', msg.get('sender', 'unknown'))
                subject = msg.get('subject', 'no subject')
                body = msg.get('body', msg.get('text', msg.get('html', '')))
                
                print(f"\n  📧 From: {sender}")
                print(f"     Subject: {subject}")
                
                if 'expired' in sender.lower() or 'expired' in subject.lower():
                    print(f"  ✓✓✓ ACTIVATION EMAIL FROM EXPIREDDOMAINS!")
                    
                    # Extract links
                    links = re.findall(r'https?://[^\s<>"\']+', str(body))
                    ed_links = [l for l in links if 'expireddomains.net' in l]
                    
                    if ed_links:
                        link = ed_links[0].strip()
                        print(f"  ✓ Found activation link: {link[:80]}...")
                        
                        # Click it
                        activate_resp = session.get(link, headers=headers, allow_redirects=True)
                        print(f"  ✓ Clicked link: {activate_resp.url}")
                        
                        if 'activated' in activate_resp.url or 'success' in activate_resp.url:
                            print("\n  ✅✅✅ ACCOUNT ACTIVATED!")
                            
                            # Test login again
                            time.sleep(2)
                            test_login = session.post(
                                'https://www.expireddomains.net/logincheck/',
                                headers=headers,
                                data=login_data
                            )
                            
                            if 'unknown' not in test_login.text.lower():
                                print("  ✅ LOGIN NOW WORKS!")
                                print("\n" + "="*70)
                                print("🎉 SUCCESS - FULL AUTOMATION WORKING!")
                                print("="*70)
                                print(f"Service: temp-mail.io")
                                print(f"Username: {username}")
                                print(f"Password: {password}")
                                print("="*70)
                                exit(0)
                    break
        else:
            print("No emails yet")
    
    print("\n⚠️  No activation email received")
    
else:
    print("✓ Account might be active or login worked!")
    
    # Test member access
    member_resp = session.get('https://member.expireddomains.net/', headers=headers, allow_redirects=True)
    if 'login' not in member_resp.url:
        print("✅ Can access member area - account is active!")

print("\n" + "="*70)