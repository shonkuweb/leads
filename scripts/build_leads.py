#!/usr/bin/env python3
"""
Fetch Indian jewellery SMB Instagram leads via public web_profile_info API.
Respects rate limits with backoff; expands queue via @mentions in bios.

Note: In some automation environments this endpoint returns HTTP 404 or empty
payloads; use scripts/generate_leads_txt.py for the curated offline export.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "scripts" / "instagram_seed_handles.txt"
OUT_PATH = ROOT / "india_jewellery_instagram_leads.txt"

IG_APP_ID = "936619743392459"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

JEWEL_RE = re.compile(
    r"jewel|jhumka|silver|gold|oxid|imitation|kundan|polki|palakka|"
    r"bangle|choker|necklace|earring|bridal|temple|handmade|artificial|"
    r"one gram|forming|925|92\.5|sterling|chaandi|chandi|mangalsutra|"
    r"antique|ethnic|traditional|ladies|fashion jew|accessory|haram|"
    r"payal|kada|nose pin|nath|maang|tikka|chudi|bangle|rajwadi|"
    r"german silver|meenakari|moissanite|resin|clay|custom",
    re.I,
)
INDIA_RE = re.compile(
    r"\+91|\bindia\b|cod|₹|rs\.|rupees|tamil|kerala|bengal|kolkata|"
    r"delhi|mumbai|bangalore|bengaluru|hyderabad|chennai|pune|jaipur|"
    r"surat|ahmedabad|lucknow|indore|nagpur|patna|rajkot|vadodara|"
    r"ghaziabad|ludhiana|agra|noida|gurgaon|faridabad|kochi|thrissur|"
    r"palakk|calicut|malappuram|kannur|wayanad|mysore|mangalore|"
    r"coimbatore|madurai|salem|trichy|vellore|aurangabad|nashik|"
    r"kolhapur|nagpur|maharashtra|gujarat|rajasthan|punjab|haryana|"
    r"up |uttar|bihar|west bengal|telangana|andhra|karnataka|tamil|"
    r"himachal|uttarakhand|odisha|orissa|assam|goa|manipur|"
    r"[\u0900-\u097F]",  # Devanagari etc.
    re.I,
)
ORDER_RE = re.compile(
    r"\bdm\b|direct message|inbox|whatsapp|wtsapp|watsapp|wa\.me|"
    r"order|booking|screenshot|paytm|gpay|phonepe|upi|"
    r"call us|contact\s*\+|message us",
    re.I,
)
PHONE_RE = re.compile(r"(?:\+91|0)?[\s-]?(?:\d[\s-]?){9}\d")
MENTION_RE = re.compile(r"@([a-zA-Z0-9._]{3,30})")

BLOCKED_URL_SUBSTR = (
    "shopify",
    "myshopify",
    "woocommerce",
    "bigcommerce",
    "amazon.in",
    "flipkart",
    "meesho.com/s/",
    "nykaa",
    "caratlane",
    "bluestone",
    "tanishq",
    "malabar",
    "kalyanjewellers",
    "joyalukkas",
    "pckt",
)

# Dedicated storefront domains (reject as "professional website")
def has_pro_store(url: str | None) -> bool:
    if not url:
        return False
    u = url.lower()
    if any(x in u for x in BLOCKED_URL_SUBSTR):
        return True
    # bare ecommerce-looking domains (not link aggregators)
    if "linktr.ee" in u or "bio.link" in u or "lnk.bio" in u or "taplink" in u:
        return False
    if "wa.me" in u or "api.whatsapp" in u:
        return False
    if u.startswith("http") and "instagram.com" in u:
        return False
    # *.com / *.in product sites
    if re.search(r"https?://[^/]+\.(com|in|co\.in)(/|$)", u):
        if not any(
            x in u
            for x in (
                "facebook.com",
                "youtube.com",
                "youtu.be",
                "google.com",
                "maps.app",
                "goo.gl",
            )
        ):
            return True
    return False


def fetch_profile(username: str) -> dict[str, Any] | None:
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "X-IG-App-ID": IG_APP_ID,
        },
        method="GET",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            if not raw.strip():
                time.sleep(12)
                continue
            data = json.loads(raw)
            if data.get("status") == "fail":
                time.sleep(12)
                continue
            return data
        except urllib.error.HTTPError as e:
            if e.code in (401, 429, 560):
                time.sleep(18 + attempt * 12)
                continue
            return None
        except Exception:
            time.sleep(10 + attempt * 6)
            continue
    return None


def norm_phone(s: str) -> str | None:
    digits = re.sub(r"\D", "", s)
    if len(digits) >= 10:
        return digits[-10:]
    return None


def extract_phones(bio: str) -> list[str]:
    out: list[str] = []
    for m in PHONE_RE.finditer(bio):
        p = norm_phone(m.group(0))
        if p and p not in out:
            out.append(p)
    return out


def latest_post_info(user: dict[str, Any]) -> tuple[str | None, list[tuple[int, int]]]:
    """Return (iso date of latest post, list of (likes, comments) for up to 3 posts)."""
    edge = user.get("edge_owner_to_timeline_media") or {}
    edges: Iterable[dict] = edge.get("edges") or []
    stats: list[tuple[int, int]] = []
    latest_ts: int | None = None
    for i, e in enumerate(edges):
        node = e.get("node") or {}
        ts = node.get("taken_at_timestamp")
        if ts and (latest_ts is None or ts > latest_ts):
            latest_ts = ts
        likes = (node.get("edge_liked_by") or {}).get("count")
        comments = (node.get("edge_media_to_comment") or {}).get("count")
        if likes is not None and comments is not None and i < 3:
            stats.append((int(likes), int(comments)))
    if not latest_ts:
        return None, stats
    dt = datetime.fromtimestamp(latest_ts, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d"), stats


def infer_city_state(bio: str) -> tuple[str, str]:
    bio_l = bio.lower()
    cities = [
        ("Kolkata", "West Bengal", ("kolkata", "chetla", "bengal")),
        ("Mumbai", "Maharashtra", ("mumbai", "colaba", "thane")),
        ("Delhi", "Delhi", ("delhi", "lajpat", "chandni", "noida", "gurgaon")),
        ("Bangalore", "Karnataka", ("bangalore", "bengaluru", "malleshwaram", "jayanagar")),
        ("Hyderabad", "Telangana", ("hyderabad", "secunderabad", "kukatpally")),
        ("Chennai", "Tamil Nadu", ("chennai", "tamil")),
        ("Pune", "Maharashtra", ("pune",)),
        ("Jaipur", "Rajasthan", ("jaipur", "jodhpur", "rajasthan")),
        ("Surat", "Gujarat", ("surat", "rajkot")),
        ("Ahmedabad", "Gujarat", ("ahmedabad", "gujarat")),
        ("Lucknow", "Uttar Pradesh", ("lucknow", "uttar pradesh")),
        ("Kochi", "Kerala", ("kochi", "kerala", "palakk")),
        ("Hyderabad", "Telangana", ("telangana",)),
    ]
    for city, st, keys in cities:
        if any(k in bio_l for k in keys):
            return city, st
    if INDIA_RE.search(bio):
        return "India (unspecified)", "India"
    return "Unknown", "Unknown"


def business_type(bio: str, cat: str | None) -> str:
    blob = f"{bio} {cat or ''}".lower()
    tags: list[str] = []
    if re.search(r"oxid|german silver", blob):
        tags.append("Oxidised/German silver")
    if re.search(r"silver|925|92\.5|sterling", blob):
        tags.append("Silver")
    if re.search(r"one gram|forming|gold plated|imitation|ad jew|american diamond", blob):
        tags.append("Imitation / gold-forming")
    if re.search(r"bridal|wedding|kundan|polki|temple", blob):
        tags.append("Bridal / temple")
    if re.search(r"handmade|clay|resin|custom", blob):
        tags.append("Handmade / custom")
    if not tags:
        tags.append("Fashion jewellery")
    return "; ".join(tags[:3])


def score_lead(
    has_whatsapp_hint: bool,
    has_dm: bool,
    no_pro_site: bool,
    followers: int,
    engagement_pct: float | None,
    recent_days: int | None,
) -> int:
    s = 5
    if has_whatsapp_hint:
        s += 1
    if has_dm:
        s += 1
    if no_pro_site:
        s += 1
    if engagement_pct is not None and engagement_pct >= 0.8:
        s += 1
    elif engagement_pct is not None and engagement_pct >= 0.3:
        s += 0
    if recent_days is not None and recent_days <= 45:
        s += 1
    if 500 <= followers <= 500000:
        s += 0
    return max(1, min(10, s))


@dataclass
class Lead:
    business_name: str
    handle: str
    followers: int
    city: str
    state: str
    business_type: str
    whatsapp: str
    email: str
    ordering: str
    website_present: str
    website_url: str
    recent_activity: str
    avg_engagement: str
    bio: str
    keywords: str
    reason: str
    services: str
    maps: str
    quality: int
    notes: str


def lead_to_txt(idx: int, L: Lead) -> str:
    lines = [
        "",
        "=" * 50,
        f"LEAD #{idx}",
        "=" * 50,
        f"Business Name: {L.business_name}",
        f"Instagram Handle: @{L.handle}",
        f"Instagram URL: https://www.instagram.com/{L.handle}/",
        f"Followers Count: {L.followers}",
        f"City: {L.city}",
        f"State: {L.state}",
        f"Business Type: {L.business_type}",
        f"WhatsApp Number: {L.whatsapp}",
        f"Email: {L.email}",
        f"Ordering Method: {L.ordering}",
        f"Website Present: {L.website_present}",
        f"Website URL: {L.website_url}",
        f"Recent Activity Date: {L.recent_activity}",
        f"Average Engagement: {L.avg_engagement}",
        f"Bio Text: {L.bio}",
        f"Keywords: {L.keywords}",
        f"Reason Qualified: {L.reason}",
        f"Potential Services Needed: {L.services}",
        f"Google Maps Link: {L.maps}",
        f"Lead Quality Score: {L.quality}",
        f"Notes: {L.notes}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    seeds = [
        ln.strip()
        for ln in SEED_PATH.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    # unique preserve order
    seen_h: set[str] = set()
    queue: list[str] = []
    for h in seeds:
        hl = h.lower().strip("@")
        if hl not in seen_h:
            seen_h.add(hl)
            queue.append(hl)

    leads: list[Lead] = []
    phones_used: set[str] = set()
    handles_out: set[str] = set()
    visited: set[str] = set()
    max_fetches = 650

    queued: set[str] = set(seen_h)

    OUT_PATH.unlink(missing_ok=True)
    OUT_PATH.write_text(
        "India Jewellery Instagram / WhatsApp SMB lead export\n"
        f"Generated (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}\n"
        "Leads appended as discovered.\n",
        encoding="utf-8",
    )

    def append_lead(idx: int, L: Lead) -> None:
        with OUT_PATH.open("a", encoding="utf-8") as fa:
            fa.write(lead_to_txt(idx, L))

    def consider_mentions(bio: str) -> None:
        for m in MENTION_RE.finditer(bio):
            h = m.group(1).lower()
            if h in visited or h in queued:
                continue
            if len(queue) > 800:
                return
            queued.add(h)
            queue.append(h)

    fetches = 0
    while queue and len(leads) < 100 and fetches < max_fetches:
        handle = queue.pop(0)
        if handle in visited:
            continue
        visited.add(handle)
        fetches += 1
        data = fetch_profile(handle)
        time.sleep(2.1)
        if not data:
            continue
        user = (data.get("data") or {}).get("user")
        if not user:
            continue
        bio = user.get("biography") or ""
        ext = user.get("external_url") or ""
        full_name = user.get("full_name") or ""
        cat = user.get("category_name") or user.get("business_category_name") or ""
        followers = int((user.get("edge_followed_by") or {}).get("count") or 0)

        consider_mentions(bio)

        if not JEWEL_RE.search(f"{bio} {full_name} {cat}"):
            continue
        if not INDIA_RE.search(bio + " " + full_name):
            # still allow if India-heavy category hashtags missing but +91 present in bio_links titles - skip strict
            if "+91" not in bio and "india" not in bio.lower():
                continue
        if not ORDER_RE.search(bio):
            continue

        pro_site = has_pro_store(ext)
        if pro_site:
            continue

        phones = extract_phones(bio)
        wa_hint = bool(re.search(r"whatsapp|wtsapp|wa\.me", bio, re.I)) or bool(phones)
        dm_hint = bool(re.search(r"\bdm\b|direct message|inbox", bio, re.I))

        # Deduplicate by primary phone
        primary = phones[0] if phones else ""
        if primary and primary in phones_used:
            continue

        recent_iso, stat_triples = latest_post_info(user)
        eng_pct: float | None = None
        if stat_triples and followers > 0:
            avg_likes = sum(x[0] for x in stat_triples) / len(stat_triples)
            eng_pct = round(100.0 * avg_likes / max(followers, 1), 3)

        recent_days: int | None = None
        if recent_iso:
            try:
                d0 = datetime.strptime(recent_iso, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                recent_days = (datetime.now(timezone.utc) - d0).days
            except Exception:
                recent_days = None

        inactive = recent_days is not None and recent_days > 150
        if inactive:
            continue

        if primary:
            phones_used.add(primary)

        city, state = infer_city_state(bio + " " + full_name)
        btype = business_type(bio, cat)
        ordering_parts = []
        if dm_hint:
            ordering_parts.append("Instagram DM")
        if wa_hint:
            ordering_parts.append("WhatsApp")
        if not ordering_parts:
            ordering_parts.append("Instagram contact")
        ordering = " + ".join(ordering_parts)

        email_m = re.search(
            r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", bio + " " + full_name, re.I
        )
        email = email_m.group(0) if email_m else "Not listed in bio"

        wa_display = ", ".join(f"+91 {p}" for p in phones) if phones else "See Instagram DM / bio link"

        reason = (
            "India-focused jewellery seller on Instagram; posts indicate catalogue commerce; "
            "bio requests DM/WhatsApp for orders; no professional ecommerce URL detected in profile link field."
        )
        services = (
            "Lightweight ecommerce or catalog site; WhatsApp automation; order CRM; "
            "Instagram booking flows; optional AI chatbot for FAQs; ads/creative support."
        )
        kw = ", ".join(
            sorted(
                set(
                    w
                    for w in re.findall(
                        r"#([\w]+)", bio, flags=re.UNICODE
                    )[:12]
                )
            )
        )
        if not kw:
            kw = "jewellery, Instagram shop, India"

        q = score_lead(wa_hint, dm_hint, not pro_site, followers, eng_pct, recent_days)

        eng_txt = (
            f"~{eng_pct}% est. likes/followers (last {len(stat_triples)} grid posts)"
            if eng_pct is not None
            else "Insufficient public post stats"
        )

        L = Lead(
            business_name=full_name or handle.replace("_", " ").title(),
            handle=handle,
            followers=followers,
            city=city,
            state=state,
            business_type=btype,
            whatsapp=wa_display,
            email=email,
            ordering=ordering,
            website_present="No" if not ext else "Link only (see URL)",
            website_url=ext or "None listed",
            recent_activity=recent_iso or "Unknown (no public grid)",
            avg_engagement=eng_txt,
            bio=bio.replace("\n", " / ")[:900],
            keywords=kw,
            reason=reason,
            services=services,
            maps="Not provided in bio",
            quality=q,
            notes="Sourced via public Instagram profile metadata; verify details before outreach.",
        )
        if handle in handles_out:
            continue
        handles_out.add(handle)
        leads.append(L)
        append_lead(len(leads), L)

    with OUT_PATH.open("a", encoding="utf-8") as fa:
        fa.write(f"\nTotal unique leads: {len(leads)}\n")
    print(f"Wrote {len(leads)} leads to {OUT_PATH}")


if __name__ == "__main__":
    main()
