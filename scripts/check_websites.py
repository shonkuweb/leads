#!/usr/bin/env python3
"""Check website reachability and classify status for school leads."""
from __future__ import annotations

import re
import socket
from urllib.parse import urlparse

import requests

USER_AGENT = "IndiaSchoolLeadBot/1.0 (+https://github.com/shonkuweb/leads)"
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
    if not url or str(url).strip().lower() in {"", "none", "unknown", "n/a"}:
        return None
    u = str(url).strip()
    if u.startswith("www."):
        u = "https://" + u
    if not u.startswith(("http://", "https://")):
        u = "https://" + u
    return u


def classify_website(url: str | None) -> tuple[str, str]:
    """
    Returns (website_status, notes).
    Status: none | active | broken | parked | facebook_only | timeout
    """
    normalized = normalize_url(url)
    if not normalized:
        return "none", "No website URL on record"

    host = (urlparse(normalized).netloc or "").lower()
    if "facebook.com" in host or "instagram.com" in host:
        return "facebook_only", "Social URL used instead of owned domain"

    try:
        resp = requests.get(
            normalized,
            timeout=TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        )
    except requests.exceptions.SSLError:
        try:
            http_url = normalized.replace("https://", "http://", 1)
            resp = requests.get(
                http_url,
                timeout=TIMEOUT,
                allow_redirects=True,
                headers={"User-Agent": USER_AGENT},
            )
        except requests.RequestException as exc:
            return "broken", f"SSL/HTTP error: {exc.__class__.__name__}"
    except (requests.RequestException, socket.timeout) as exc:
        return "broken", f"Unreachable: {exc.__class__.__name__}"

    final_host = (urlparse(resp.url).netloc or "").lower()
    if "facebook.com" in final_host:
        return "facebook_only", "Redirects to Facebook page"

    if resp.status_code >= 400:
        return "broken", f"HTTP {resp.status_code}"

    body = (resp.text or "")[:8000].lower()
    if len(body.strip()) < 80:
        return "broken", "Blank or near-empty page"

    if any(h in body for h in PARKED_HINTS):
        return "parked", "Parked or placeholder domain signals in HTML"

    if "wordpress" in body and ("hello world" in body or "just another wordpress" in body):
        return "broken", "Default WordPress placeholder"

    return "active", f"HTTP {resp.status_code} OK"


def is_generic_email(email: str | None) -> bool:
    if not email or email.lower() == "unknown":
        return False
    e = email.lower()
    if any(x in e for x in ("@gmail.com", "@yahoo.", "@rediffmail", "@hotmail.")):
        return True
    return not ("@" in e and "." in e.split("@")[-1] and " " not in e)


def compute_lead_score(lead: dict, website_status: str) -> int:
    score = 1
    year = lead.get("year_established")
    try:
        if year and int(str(year)[:4]) >= 2021:
            score += 2
        elif year and int(str(year)[:4]) >= 2019:
            score += 1
    except ValueError:
        pass

    if website_status in {"none", "broken", "parked", "facebook_only"}:
        score += 3
    elif website_status == "broken":
        score += 2

    if lead.get("whatsapp") and str(lead.get("whatsapp")).lower() != "unknown":
        score += 1
    if is_generic_email(lead.get("email")):
        score += 2
    if lead.get("instagram") and website_status in {"none", "facebook_only"}:
        score += 1

    board = (lead.get("board") or "").upper()
    stype = (lead.get("school_type") or "").lower()
    if "CBSE" in board or "ICSE" in board:
        score += 1
    if any(k in stype for k in ("play", "montessori", "preschool", "pre-school", "international")):
        score += 1

    priority_states = {
        "west bengal", "uttar pradesh", "bihar", "jharkhand", "odisha", "assam",
        "maharashtra", "karnataka", "telangana", "tamil nadu", "rajasthan", "gujarat",
    }
    if (lead.get("state") or "").lower() in priority_states:
        score += 1

    if lead.get("principal_name") or lead.get("director_name"):
        score += 1

    return min(10, max(1, score))
