#!/usr/bin/env python3
"""
22.do Temporary Outlook API client
Docs: https://22.do/document
"""
import os
import time
import random
import string
import requests
from typing import List, Optional, Dict, Any

class TwentyTwoClient:
	"""Client wrapper for 22.do API."""

	def __init__(self, address: Optional[str] = None, password: Optional[str] = None, api_key: Optional[str] = None) -> None:
		self.base_url = "https://22.do/api/v2"
		self.session = requests.Session()
		self.address = address or os.getenv("TWENTYTWO_ADDRESS")
		self.password = password or os.getenv("TWENTYTWO_PASSWORD")
		self.api_key = api_key or os.getenv("TWENTYTWO_API_KEY")  # This is the 'token' per docs
		self.bearer_token: Optional[str] = None
		self.default_headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
			"Accept": "application/json, text/plain, */*",
		}

	def _request(self, method: str, path: str, **kwargs) -> requests.Response:
		url = f"{self.base_url}{path}"
		headers = {**self.default_headers, **kwargs.pop("headers", {})}
		if self.bearer_token:
			headers["Authorization"] = f"Bearer {self.bearer_token}"
		resp = self.session.request(method, url, headers=headers, timeout=30, **kwargs)
		resp.raise_for_status()
		return resp

	def login(self) -> bool:
		"""Authenticate and store bearer token using address/password or token via /token."""
		try:
			if self.api_key:
				# Exchange token for Bearer
				resp = self._request("POST", "/token", json={"token": self.api_key})
				data = resp.json().get("data", {})
				self.bearer_token = data.get("Bearer")
				if not self.bearer_token:
					print("[22.do] Token exchange failed: no Bearer returned")
					return False
				print("[22.do] Authenticated via token")
				return True
			elif self.address and self.password:
				resp = self._request("POST", "/auth", json={"address": self.address, "password": self.password})
				data = resp.json().get("data", {})
				self.bearer_token = data.get("Bearer")
				if not self.bearer_token:
					print("[22.do] Auth failed: no token returned")
					return False
				print("[22.do] Authenticated successfully")
				return True
			else:
				print("[22.do] Missing credentials. Provide TWENTYTWO_API_KEY or TWENTYTWO_ADDRESS/PASSWORD")
				return False
		except Exception as e:
			print(f"[22.do] Auth error: {e}")
			return False

	def get_domains(self) -> List[Dict[str, Any]]:
		"""Fetch available domains."""
		try:
			resp = self._request("GET", "/domains")
			return resp.json().get("data", [])
		except Exception as e:
			print(f"[22.do] Domains error: {e}")
			return []

	def create_account(self) -> Optional[Dict[str, Any]]:
		"""POST /account to get a temp email account."""
		try:
			resp = self._request("POST", "/account", json={})
			data = resp.json().get("data")
			return data
		except Exception as e:
			print(f"[22.do] Create account error: {e}")
			return None

	def get_account_premium(self) -> Optional[Dict[str, Any]]:
		try:
			resp = self._request("GET", "/account/premium")
			return resp.json().get("data")
		except Exception as e:
			print(f"[22.do] Account premium error: {e}")
			return None

	def get_account_private(self) -> Optional[Dict[str, Any]]:
		try:
			resp = self._request("GET", "/account/private")
			return resp.json().get("data")
		except Exception as e:
			print(f"[22.do] Account private error: {e}")
			return None

	def generate_address(self, preferred_domain: Optional[str] = None) -> Optional[str]:
		"""Use /account to get an address; fallback to /account/premium and /account/private."""
		acc = self.create_account()
		if acc and acc.get("email"):
			email = acc["email"]
			print(f"[22.do] Generated address: {email}")
			return email
		acc = self.get_account_premium()
		if acc and acc.get("email"):
			email = acc["email"]
			print(f"[22.do] Generated premium address: {email}")
			return email
		acc = self.get_account_private()
		if acc and acc.get("email"):
			email = acc["email"]
			print(f"[22.do] Generated private address: {email}")
			return email
		print("[22.do] No address returned from /account endpoints")
		return None

	def get_messages(self, inbox: str, since_unix: Optional[int] = None) -> List[Dict[str, Any]]:
		"""POST /inbox with email (and optional time)."""
		payload: Dict[str, Any] = {"email": inbox}
		if since_unix:
			payload["time"] = since_unix
		try:
			resp = self._request("POST", "/inbox", json=payload)
			return resp.json().get("data", [])
		except Exception as e:
			print(f"[22.do] Inbox error: {e}")
			return []

	def wait_for_message(self, inbox: str, timeout: int = 180, interval: int = 8, keyword: Optional[str] = None) -> Optional[Dict[str, Any]]:
		"""Poll for a message; optionally filter by keyword in subject or from."""
		end = time.time() + timeout
		while time.time() < end:
			msgs = self.get_messages(inbox)
			if msgs:
				if keyword:
					for m in msgs:
						subj = (m.get("subject") or "").lower()
						frm = (m.get("from") or "").lower()
						if keyword.lower() in subj or keyword.lower() in frm:
							return m
					return msgs[0]
			time.sleep(interval)
		return None

	def fetch_message(self, message_id: str) -> Optional[Dict[str, Any]]:
		"""POST /inbox/message with messageId"""
		try:
			resp = self._request("POST", "/inbox/message", json={"messageId": message_id})
			return resp.json().get("data")
		except Exception as e:
			print(f"[22.do] Fetch message error: {e}")
			return None


def test_client() -> None:
	client = TwentyTwoClient()
	if not client.login():
		return
	domains = client.get_domains()
	print(f"Domains (first 2): {domains[:2]}")
	addr = client.generate_address()
	if not addr:
		return
	print(f"Inbox ready: {addr}")
	msgs = client.get_messages(addr)
	print(f"Messages: {len(msgs)}")

if __name__ == "__main__":
	test_client()