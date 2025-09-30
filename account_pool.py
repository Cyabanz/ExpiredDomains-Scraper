#!/usr/bin/env python3
"""
Create a pool of accounts and save working credentials
This allows pre-creating accounts that may become active after verification
"""
import json
import os
import time
import requests
from guerrilla_mail import GuerrillaMailClient, generate_random_credentials

ACCOUNTS_FILE = "/workspace/account_pool.json"

def load_accounts():
    """Load saved accounts from file"""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_accounts(accounts):
    """Save accounts to file"""
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=2)

def create_account():
    """Create a single account"""
    email_client = GuerrillaMailClient()
    
    # Use sharklasers.com domain (more legitimate looking)
    email = email_client.get_email_address()
    if '@guerrillamailblock.com' in email:
        # Change to sharklasers
        username_part = email.split('@')[0]
        email_client.set_email_user(username_part)
        email = email_client.email_address
    
    username, password = generate_random_credentials()
    
    # Register
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    reg_data = {
        'signup': '1',
        'jscheck': '1',
        'login': username,
        'pass': password,
        'pass2': password,
        'email': email,
        'button_submit': 'Sign Up (Free)',
    }
    
    try:
        response = session.post(
            'https://www.expireddomains.net/register/',
            headers=headers,
            data=reg_data,
            allow_redirects=True,
            timeout=30
        )
        
        if 'success' in response.url.lower():
            return {
                'username': username,
                'password': password,
                'email': email,
                'created_at': time.time(),
                'status': 'pending_verification'
            }
    except Exception as e:
        print(f"Error creating account: {e}")
    
    return None

def test_account(username, password):
    """Test if an account can login"""
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    login_data = {
        'login': username,
        'password': password,
        'redirect_to_url': '/home',
    }
    
    try:
        response = session.post(
            'https://www.expireddomains.net/logincheck/',
            headers=headers,
            data=login_data,
            timeout=30
        )
        
        if "The supplied login information are unknown" not in response.text:
            # Login might have worked
            member_check = session.get('https://member.expireddomains.net/', headers=headers, timeout=30)
            if 'login' not in member_check.url.lower():
                return True
    except:
        pass
    
    return False

def get_working_account():
    """Get a working account from the pool"""
    accounts = load_accounts()
    
    # First, try existing accounts
    for account in accounts:
        if account.get('status') == 'verified' or account.get('status') == 'working':
            print(f"[Pool] Using existing verified account: {account['username']}")
            return account['username'], account['password']
    
    # Test pending accounts to see if any are now active
    for account in accounts:
        if account.get('status') == 'pending_verification':
            print(f"[Pool] Testing pending account: {account['username']}...")
            if test_account(account['username'], account['password']):
                account['status'] = 'working'
                save_accounts(accounts)
                print(f"[Pool] ✓ Account is now working!")
                return account['username'], account['password']
    
    print("[Pool] No working accounts in pool")
    return None, None

def create_account_pool(count=5):
    """Create multiple accounts for future use"""
    accounts = load_accounts()
    
    print(f"[Pool] Creating {count} accounts...")
    
    for i in range(count):
        print(f"\n[Pool] Creating account {i+1}/{count}...")
        account = create_account()
        
        if account:
            accounts.append(account)
            print(f"[Pool] ✓ Created: {account['username']} ({account['email']})")
        else:
            print(f"[Pool] ✗ Failed to create account")
        
        # Save after each creation
        save_accounts(accounts)
        
        # Wait between creations to avoid rate limiting
        if i < count - 1:
            time.sleep(3)
    
    print(f"\n[Pool] Pool now contains {len(accounts)} accounts")
    print(f"[Pool] Saved to {ACCOUNTS_FILE}")
    
    return accounts

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        create_account_pool(count)
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        accounts = load_accounts()
        print(f"Testing {len(accounts)} accounts...")
        for acc in accounts:
            result = "✓ WORKING" if test_account(acc['username'], acc['password']) else "✗ Not working yet"
            print(f"{acc['username']}: {result}")
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        accounts = load_accounts()
        print(f"\nAccount Pool ({len(accounts)} accounts):")
        for i, acc in enumerate(accounts, 1):
            print(f"{i}. {acc['username']} - {acc.get('status', 'unknown')} - {acc['email']}")
    else:
        print("Usage:")
        print("  python3 account_pool.py create [count]  - Create N accounts (default 5)")
        print("  python3 account_pool.py test            - Test all accounts")
        print("  python3 account_pool.py list            - List all accounts")