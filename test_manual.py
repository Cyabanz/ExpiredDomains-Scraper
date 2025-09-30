#!/usr/bin/env python3
"""Quick test with manual credentials"""
import config
from expireddomains import User

print(f"[TEST] Testing with manual credentials from config.py")
print(f"Username: {config.username}")
print(f"Password: {config.password}")

user = User("education", config.username, config.password)
print("\n[TEST] Attempting login...")
login = user.get_cookie()

if login:
    print("[SUCCESS] Login successful with manual credentials!")
    print("[TEST] The site is accessible and working")
else:
    print("[FAIL] Login failed with manual credentials")
    print("[INFO] The site may have changed or credentials are incorrect")