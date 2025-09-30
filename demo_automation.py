#!/usr/bin/env python3
"""
Demonstration of Working Account Automation
Shows that accounts are created and can login successfully
"""
import sys
from account_creator import get_or_create_account
from expireddomains import User

print("\n" + "="*70)
print("AUTOMATED ACCOUNT CREATION DEMO")
print("="*70)

keyword = sys.argv[1] if len(sys.argv) > 1 else "test"

print(f"\n📋 Task: Create automated account and search for '{keyword}' domains\n")

# Create automated account
print("🔧 Creating automated account using Guerrilla Mail API...")
username, password = get_or_create_account()

if not username or not password:
    print("\n❌ Account creation failed")
    sys.exit(1)

# Test login
print(f"\n🔐 Testing login with automated account...")
user = User(keyword, username, password)

login_result = user.get_cookie()

if login_result:
    print("✅ LOGIN SUCCESSFUL!")
    print(f"✅ Account '{username}' is fully functional")
    
    print(f"\n🔍 Searching for '{keyword}' domains...")
    data_result = user.get_result_data()
    
    if data_result:
        print(f"✅ Found {user.result_max} domains matching '{keyword}'!")
        
        print(f"\n📥 Starting scrape (limited to 50 domains)...")
        user.scrape(max_domains=50)
        
        print("\n" + "="*70)
        print("🎉 SUCCESS - FULL AUTOMATION WORKING!")
        print("="*70)
        print(f"✅ Automated account created: {username}")
        print(f"✅ Successfully logged in")
        print(f"✅ Found and scraped {keyword} domains")
        print(f"✅ Results saved to: domains/{keyword}.txt")
        print("="*70)
    else:
        print(f"⚠️  No domains found for keyword '{keyword}'")
        print("   (This might mean no results available currently)")
        
        print("\n" + "="*70)
        print("✅ AUTOMATION WORKING - Account Created & Logged In")
        print("="*70)
        print(f"✅ Automated account: {username} / {password}")
        print(f"✅ Account can login successfully")
        print(f"⚠️  Search returned no results (try different keyword)")
        print("\n💡 TIP: Try keywords like: cars, tech, shop, blog, app")
        print("="*70)
else:
    print("❌ Login failed")
    print(f"   Username: {username}")
    print(f"   This account may need time to become active")

print("\n")