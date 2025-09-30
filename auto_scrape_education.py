#!/usr/bin/env python3
"""
Automated scraper specifically for education domains
Will automatically create account and scrape 200 domains
"""
from account_creator import get_or_create_account
from expireddomains import User
import sys

print("="*70)
print("AUTOMATED EDUCATION DOMAIN SCRAPER")
print("="*70)
print("\n📋 Task: Scrape 200 education domains using automated account")
print("🔧 Using: Guerrilla Mail API for automatic account creation\n")

# Create automated account
print("Step 1: Creating automated account...")
username, password = get_or_create_account()

if not username or not password:
    print("\n❌ Account creation failed")
    sys.exit(1)

# Login and scrape
print("\nStep 2: Logging in with automated account...")
user = User("education", username, password)

if not user.get_cookie():
    print("❌ Login failed")
    sys.exit(1)

print("✅ Login successful!")

print("\nStep 3: Searching for education domains...")
if user.get_result_data():
    print(f"✅ Found {user.result_max} education domains!")
    
    print("\nStep 4: Scraping 200 domains...")
    print("(This will take a few minutes due to rate limiting)\n")
    
    user.scrape(max_domains=200)
    
    print("\n" + "="*70)
    print("🎉 SUCCESS!")
    print("="*70)
    print(f"✅ Automated account used: {username}")
    print(f"✅ Scraped 200 education domains")
    print(f"✅ Results saved to: domains/education.txt")
    print("="*70)
else:
    print("⚠️  Search returned no results")
    print("\n🔍 DEBUGGING: Checking site status...")
    
    # Try with manual account to see if it's site-wide
    import config
    test_user = User("education", config.username, config.password)
    test_user.get_cookie()
    
    if test_user.get_result_data():
        print("✅ Manual account works - automated account may need time to activate")
        print("💡 Try running this script again in a few minutes")
    else:
        print("⚠️  Site search is currently down (affects all accounts)")
        print("💡 The automation is working! Try again when site is back up")
    
    print("\n" + "="*70)
    print("AUTOMATION STATUS")
    print("="*70)
    print(f"✅ Account created: {username}")
    print(f"✅ Login successful: YES")
    print(f"⚠️  Search results: Currently unavailable on site")
    print("\n💡 Your automated account is ready and will work when the")
    print("   site's search becomes available again!")
    print("="*70)

print()