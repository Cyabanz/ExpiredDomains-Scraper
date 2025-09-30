#!/usr/bin/env python3
"""
Scrape education domains - using best available method
"""
import sys
from expireddomains import User
from account_creator import get_or_create_account
import config

print("="*70)
print("EDUCATION DOMAIN SCRAPER - 200 Domains")
print("="*70)

print("\n🔍 Checking account options...")

# Try automated account first
print("\n[Option 1] Trying automated account creation...")
username, password = get_or_create_account()

if username and password:
    print(f"\n✅ Automated account created: {username}")
    print("🔐 Testing login...")
    
    user = User("education", username, password)
    if user.get_cookie():
        print("✅ Login successful!")
        
        # Try to search
        if user.get_result_data():
            print(f"✅ Found {user.result_max} domains!")
            print("\n📥 Scraping 200 education domains...")
            user.scrape(max_domains=200)
            
            print("\n" + "="*70)
            print("🎉 SUCCESS!")
            print("="*70)
            print(f"✅ Results saved to: domains/education.txt")
            print(f"✅ Used automated account: {username}")
            print("="*70)
            sys.exit(0)
        else:
            print("⚠️  Automated account cannot search yet (needs activation)")
    else:
        print("⚠️  Automated account login failed (needs activation)")

print("\n[Option 2] Trying manual account from config.py...")
print(f"Username: {config.username}")

user = User("education", config.username, config.password)
if user.get_cookie():
    print("✅ Manual account logged in!")
    
    if user.get_result_data():
        print(f"✅ Found {user.result_max} domains!")
        print("\n📥 Scraping 200 education domains...")
        user.scrape(max_domains=200)
        
        print("\n" + "="*70)
        print("🎉 SUCCESS!")
        print("="*70)
        print(f"✅ Results saved to: domains/education.txt")
        print(f"✅ Used manual account: {config.username}")
        print("="*70)
        sys.exit(0)
    else:
        print("⚠️  No search results available")
else:
    print("⚠️  Manual account deactivated or invalid")

print("\n" + "="*70)
print("📋 SUMMARY")
print("="*70)
print("❌ Unable to scrape education domains right now")
print("\n💡 This is because:")
print("   1. Automated accounts need email activation")
print("   2. Temp email services are blocked by the site")
print("   3. Manual account is deactivated")
print("\n🔧 SOLUTION:")
print("   Create a new account manually at expireddomains.net")
print("   with a real email, activate it, then update config.py:")
print(f"\n   # config.py")
print(f"   username = 'your_new_username'")
print(f"   password = 'your_new_password'")
print("\n   Then run this script again!")
print("="*70)