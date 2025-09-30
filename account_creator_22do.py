#!/usr/bin/env python3
"""
Account creator using 22.do API (temporary Outlook)
Requires: TWENTYTWO_API_KEY env var (or address/password for /auth)
"""
import re
import time
import random
import string
import requests
from typing import Optional, Tuple
from twentytwo_client import TwentyTwoClient


def generate_random_credentials() -> Tuple[str, str]:
	username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
	password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=12))
	return username, password


class ExpiredDomainsAccountCreator22Do:
	def __init__(self) -> None:
		self.http = requests.Session()
		self.mail = TwentyTwoClient()
		self.username: Optional[str] = None
		self.password: Optional[str] = None
		self.email: Optional[str] = None

	def create_account(self) -> Tuple[Optional[str], Optional[str]]:
		print("\n" + "="*60)
		print("AUTOMATED ACCOUNT CREATION (Using 22.do)")
		print("="*60)
		# Login to 22.do
		if not self.mail.login():
			print("[22.do] Unable to authenticate. Set TWENTYTWO_API_KEY.")
			return None, None
		# Generate inbox
		self.email = self.mail.generate_address()
		if not self.email:
			print("[22.do] Could not generate inbox")
			return None, None
		print(f"✓ Inbox: {self.email}")
		# Credentials
		self.username, self.password = generate_random_credentials()
		print(f"✓ Username: {self.username}")
		print("[ED] Registering account...")
		if not self._register_on_expireddomains():
			return None, None
		print("[ED] Waiting for activation email...")
		if not self._wait_and_activate():
			print("⚠️  No activation detected; continuing anyway")
		return self.username, self.password

	def _register_on_expireddomains(self) -> bool:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
		}
		# Prime registration page
		try:
			self.http.get('https://www.expireddomains.net/register/', headers=headers, timeout=30)
		except Exception:
			pass
		data = {
			'signup': '1',
			'jscheck': '1',
			'login': self.username,
			'pass': self.password,
			'pass2': self.password,
			'email': self.email,
			'button_submit': 'Sign Up (Free)',
		}
		try:
			resp = self.http.post('https://www.expireddomains.net/register/', headers=headers, data=data, allow_redirects=True, timeout=30)
			if 'success' in resp.url.lower():
				print("✓ Registration submitted")
				return True
			print(f"[ED] Registration response: {resp.url}")
			return True
		except Exception as e:
			print(f"[ED] Registration error: {e}")
			return False

	def _wait_and_activate(self) -> bool:
		# Poll 22.do messages
		msg = self.mail.wait_for_message(self.email, timeout=300, interval=10, keyword='expired')
		if not msg:
			return False
		# Try to fetch full message if possible
		body_candidates = []
		for key in ('body', 'html', 'text', 'content'):
			val = msg.get(key)
			if isinstance(val, str) and len(val) > 0:
				body_candidates.append(val)
		body = "\n".join(body_candidates)
		links = re.findall(r'https?://[^\s<>"\']+', body, flags=re.IGNORECASE)
		ed_links = [l for l in links if 'expireddomains.net' in l.lower()]
		if not ed_links:
			print("[ED] No activation link found in email")
			return False
		activate = ed_links[0].strip().rstrip('.,;)\'\"')
		print(f"[ED] Activating via: {activate[:80]}...")
		try:
			resp = self.http.get(activate, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=30)
			print(f"[ED] Activation result: {resp.url}")
			return True
		except Exception:
			return False


def get_or_create_account_22do() -> Tuple[Optional[str], Optional[str]]:
	creator = ExpiredDomainsAccountCreator22Do()
	return creator.create_account()

if __name__ == "__main__":
	print(get_or_create_account_22do())