#!/usr/bin/env python3
"""Test tempmail-python package"""
try:
    from tempmail import EMail
    
    print("Testing tempmail-python...")
    email = EMail()
    
    print(f"✓ Email created: {email.address}")
    print(f"✓ Domain: {email.address.split('@')[1] if '@' in email.address else 'unknown'}")
    
    # Try to get messages
    messages = email.get_inbox()
    print(f"✓ Inbox check works: {len(messages)} messages")
    
    print("\n✓ tempmail-python is working!")
    
except ImportError as e:
    print(f"✗ tempmail not available: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()