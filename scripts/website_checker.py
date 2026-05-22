"""Check website reachability and classify status."""
from __future__ import annotations

import re
import socket
from typing import Any
from urllib.parse import urlparse

import requests

USER_AGENT = (
    "Mozilla/5.0 (compatible; IndiaSchoolLeadBot/1.0; +https://github.com/cursor-automation)"
)
TIMEOUT = 12

PARKED_HINTS = (
    "domain is for sale",
    "buy this domain",
    "parked",
    "godaddy",
    "namecheap",
    "coming soon",
    "under construction",
)


def normalize_url(url: str | None) -> str | None:
    if not url or str(url).lower() in {"unknown", "none", "n/a", ""}:
        return None
    u = str(url).strip()
    if u.startswith("www."):
        u = "https://" + u
    if not u.startswith(("http://", "https://")):
        if "." in u and " " not in u:
            u = "https://" + u
        else:
            return None
    return u


def check_website(url: str | None) -> dict[str, Any]:
    """Return status dict: status, http_code, ssl, notes."""
    normalized = normalize_url(url)
    if not normalized:
        return {
            "website_status": "no_website",
            "http_code": None,
            "has_ssl": False,
            "notes": "No URL provided",
        }

    parsed = urlparse(normalized)
    host = parsed.netloc or parsed.path.split("/")[0]
    has_ssl = parsed.scheme == "https"

    try:
        resp = requests.get(
            normalized,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
        )
        code = resp.status_code
        body_lower = (resp.text or "")[:8000].lower()
        final_url = str(resp.url).lower()

        if code >= 400:
            status = "broken"
        elif any(h in body_lower for h in PARKED_HINTS):
            status = "parked_domain"
        elif "facebook.com" in final_url and "facebook.com" not in normalized.lower():
            status = "facebook_redirect"
        elif len(body_lower.strip()) < 80:
            status = "blank_page"
        elif "wordpress" in body_lower and "just another wordpress site" in body_lower:
            status = "wordpress_default"
        else:
            status = "active"

        return {
            "website_status": status,
            "http_code": code,
            "has_ssl": has_ssl or final_url.startswith("https"),
            "notes": f"Final URL: {resp.url}",
        }
    except requests.exceptions.SSLError:
        return {
            "website_status": "ssl_error",
            "http_code": None,
            "has_ssl": False,
            "notes": "SSL handshake failed",
        }
    except (requests.exceptions.ConnectionError, socket.gaierror):
        return {
            "website_status": "unreachable",
            "http_code": None,
            "has_ssl": has_ssl,
            "notes": "DNS or connection failure",
        }
    except requests.exceptions.Timeout:
        return {
            "website_status": "timeout",
            "http_code": None,
            "has_ssl": has_ssl,
            "notes": "Request timed out",
        }
    except requests.RequestException as exc:
        return {
            "website_status": "error",
            "http_code": None,
            "has_ssl": has_ssl,
            "notes": str(exc)[:200],
        }


def is_generic_email(email: str | None) -> bool:
    if not email or email.lower() == "unknown":
        return False
    e = email.lower()
    return any(
        d in e
        for d in (
            "@gmail.com",
            "@yahoo.com",
            "@yahoo.in",
            "@hotmail.com",
            "@rediffmail.com",
            "@outlook.com",
        )
    )


def is_domain_email(email: str | None, website: str | None) -> bool:
    if not email or "@" not in email:
        return False
    domain = email.split("@", 1)[1].lower()
    if domain in {"gmail.com", "yahoo.com", "yahoo.in", "hotmail.com"}:
        return False
    site = normalize_url(website)
    if site:
        host = urlparse(site).netloc.lower().replace("www.", "")
        if host and (host in domain or domain in host):
            return True
    return "." in domain and "school" in domain
