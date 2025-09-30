#!/usr/bin/env python3
"""
Fully automated scraper - no prompts, just runs with auto-created account
Usage: python auto_scrape.py <keyword>
Example: python auto_scrape.py cars
"""

import sys
from expireddomains import User
from account_creator import get_or_create_account

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_scrape.py <keyword>")
        print("Example: python auto_scrape.py cars")
        sys.exit(1)
    
    keyword = sys.argv[1]
    
    print(f"\n[INFO] Starting automated scrape for keyword: {keyword}")
    
    # Automatically create account
    username, password = get_or_create_account()
    
    if not username or not password:
        print("\n[ERROR] Failed to create account automatically")
        sys.exit(1)
    
    # Create user and scrape
    user = User(keyword, username, password)
    
    print(f"\n[INFO] Logging in with automated account...")
    login = user.get_cookie()
    
    if not login:
        print('[ERROR] Login failed')
        sys.exit(1)
    
    print(f"[INFO] Searching for domains with keyword: {keyword}")
    data = user.get_result_data()
    
    if not data:
        print('[ERROR] No records matching keyword')
        sys.exit(1)
    
    print(f"[INFO] Starting scrape...")
    user.scrape()
    
    print(f"\n[SUCCESS] Scraping completed! Check domains/{keyword}.txt")

if __name__ == "__main__":
    main()