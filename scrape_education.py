#!/usr/bin/env python3
"""Scrape education domains using manual credentials"""
import config
from expireddomains import User

print("[INFO] Scraping education domains")
print(f"[INFO] Using credentials: {config.username}")

user = User("education", config.username, config.password)

print("\n[1/3] Logging in...")
login = user.get_cookie()

if not login:
    print("[ERROR] Login failed")
    exit(1)

print("[SUCCESS] Login successful!")

print("\n[2/3] Searching for domains...")
data = user.get_result_data()

if not data:
    print("[ERROR] No records matching keyword 'education'")
    exit(1)

print(f"[SUCCESS] Found {user.result_max} total domains matching 'education'!")

print("\n[3/3] Starting scrape...")
user.scrape()

print("\n" + "="*60)
print("SCRAPING COMPLETED!")
print("="*60)
print(f"Results saved to: domains/education.txt")
print("="*60)