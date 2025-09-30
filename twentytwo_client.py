#!/usr/bin/env python3
"""
22.do Temporary Outlook API client
Docs: https://22.do/document
"""
import os
import time
import random
import string
import re
import requests
from typing import List, Optional, Dict, Any

class TwentyTwoClient:
	"""Client wrapper for 22.do API."""

	def __init__(self, address: Optional[str] = None, password: Optional[str] = None) -> None:
		self.base_url = "https://22.do"
		self.session = requests.Session()
		self.address = address or os.getenv("TWENTYTWO_ADDRESS")
		self.password = password or os.getenv("TWENTYTWO_PASSWORD")
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
		"""Authenticate and store bearer token."""
		if not self.address or not self.password:
			print("[22.do] Missing credentials. Set TWENTYTWO_ADDRESS and TWENTYTWO_PASSWORD env vars.")
			return False
		try:
			resp = self._request("POST", "/auth", json={"address": self.address, "password": self.password})
			data = resp.json().get("data", {})
			self.bearer_token = data.get("Bearer")
			if not self.bearer_token:
				print("[22.do] Auth failed: no token returned")
				return False
			print("[22.do] Authenticated successfully")
			return True
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

	def generate_address(self, preferred_domain: Optional[str] = None) -> Optional[str]:
		"""Generate an address using available domains."""
		domains = self.get_domains()
		if not domains:
			print("[22.do] No domains available")
			return None
		if preferred_domain:
			domain = preferred_domain
		else:
			domain = domains[0].get("domain") or domains[0]
		local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
		address = f"{local}@{domain}"
		print(f"[22.do] Generated address: {address}")
		return address

	def get_messages(self, inbox: str, page: int = 1) -> List[Dict[str, Any]]:
		"""Get messages for an inbox."""
		try:
			resp = self._request("GET", f"/messages", params={"inbox": inbox, "page": page})
			return resp.json().get("data", [])
		except Exception as e:
			print(f"[22.do] Messages error: {e}")
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
		"""Fetch a single message (if endpoint exists). Placeholder if API differs."""
		try:
			resp = self._request("GET", f"/messages/{message_id}")
			return resp.json().get("data")
		except Exception as e:
			print(f"[22.do] Fetch message error: {e}")
			return None


def test_client() -> None:
	client = TwentyTwoClient()
	if not client.login():
		return
	domains = client.get_domains()
	print(f"Domains: {domains[:2]}")
	addr = client.generate_address(domains[0].get("domain") if domains else None)
	if not addr:
		return
	print(f"Inbox ready: {addr}")
	msgs = client.get_messages(addr)
	print(f"Messages: {len(msgs)}")

if __name__ == "__main__":
	test_client()