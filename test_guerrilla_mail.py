#!/usr/bin/env python3
"""
Test script for Guerrilla Mail API functionality
This demonstrates how to create temporary email addresses and check for emails
"""

from guerrilla_mail import GuerrillaMailClient
import time

def test_guerrilla_mail():
    """
    Test the Guerrilla Mail API client
    """
    print("\n" + "="*60)
    print("GUERRILLA MAIL API TEST")
    print("="*60)
    
    # Create client
    client = GuerrillaMailClient()
    
    # Get a temporary email address
    print("\n[1] Creating temporary email address...")
    email = client.get_email_address()
    
    if email:
        print(f"✓ Successfully created: {email}")
    else:
        print("✗ Failed to create email address")
        return
    
    # Optionally set a custom username
    print("\n[2] Testing custom username...")
    custom_email = client.set_email_user("testuser123")
    
    if custom_email:
        print(f"✓ Updated to: {custom_email}")
    else:
        print("✗ Failed to set custom username")
    
    # Check for emails
    print("\n[3] Checking for emails...")
    emails = client.check_email()
    print(f"✓ Found {len(emails)} email(s)")
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60)
    print(f"\nYour temporary email: {client.email_address}")
    print("You can send test emails to this address.")
    print("\nWaiting 30 seconds to check for new emails...")
    
    # Wait a bit and check again
    time.sleep(30)
    emails = client.check_email()
    
    if emails:
        print(f"\n✓ Received {len(emails)} new email(s)!")
        for email_data in emails:
            print(f"\nFrom: {email_data.get('mail_from')}")
            print(f"Subject: {email_data.get('mail_subject')}")
            print(f"Time: {email_data.get('mail_timestamp')}")
    else:
        print("\n✓ No new emails received (this is normal for a test)")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_guerrilla_mail()