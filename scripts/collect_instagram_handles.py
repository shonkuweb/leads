#!/usr/bin/env python3
"""Collect Instagram jewellery-related handles via DDG (read-only discovery)."""
import re
import json
from urllib.parse import urlparse

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

QUERIES = [
    'site:instagram.com "DM to order" jewellery India',
    'site:instagram.com "Order on WhatsApp" jewellery India',
    'site:instagram.com "WhatsApp" bridal jewellery India',
    'site:instagram.com kolkata jewellery shop',
    'site:instagram.com Mumbai imitation jewellery',
    'site:instagram.com Delhi artificial jewellery wholesale',
    'site:instagram.com Hyderabad silver jewellery order',
    'site:instagram.com Bangalore fashion jewellery DM',
    'site:instagram.com Chennai kundan jewellery WhatsApp',
    'site:instagram.com Jaipur polki jewellery DM',
    'site:instagram.com Surat jewellery wholesale WhatsApp',
    'site:instagram.com Ahmedabad oxidised jewellery',
    'site:instagram.com Pune temple jewellery order',
    'site:instagram.com "wa.me" jewellery India',
    'site:instagram.com "+91" kundan jewellery order',
    'site:instagram.com custom jewellery India handmade',
    'site:instagram.com artificial jewellery India COD',
    'site:instagram.com silver jewellery rajasthani Instagram',
    'site:instagram.com fashion jewellery boutique India',
    'site:instagram.com bridal jewellery set order WhatsApp',
    'site:instagram.com imitation jewellery wholesale India',
    'site:instagram.com german silver jewellery India',
    'site:instagram.com "screenshot" order jewellery WhatsApp India',
    'site:instagram.com resin earrings India DM',
    'site:instagram.com jhumka wholesale Instagram India',
]

HANDLE_RE = re.compile(r"instagram\.com/([A-Za-z0-9._]+)/?", re.I)
SKIP = {
    "p", "reel", "reels", "stories", "explore", "accounts", "direct",
    "legal", "about", "blog", "developers", "help", "tv",
}

EXCLUDE_SUBSTR = (
    "tanishq", "caratlane", "bluestone", "malabar", "kalyan", "joyalukkas",
    "senco", "pcjeweller", "titan", "swarovski", "cartier", "tiffany",
    "kisna", "melorra", "candere",
)


def main():
    handles = set()
    with DDGS() as ddgs:
        for q in QUERIES:
            try:
                for r in ddgs.text(q, max_results=25):
                    for u in (r.get("href") or "", r.get("body") or ""):
                        for m in HANDLE_RE.finditer(u):
                            h = m.group(1).strip("._")
                            if h.lower() in SKIP:
                                continue
                            if any(x in h.lower() for x in EXCLUDE_SUBSTR):
                                continue
                            if len(h) < 3 or len(h) > 30:
                                continue
                            handles.add(h)
            except Exception:
                continue
    print(json.dumps(sorted(handles), indent=0))


if __name__ == "__main__":
    main()
