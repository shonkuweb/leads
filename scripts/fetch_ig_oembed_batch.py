#!/usr/bin/env python3
"""Fetch Instagram oEmbed metadata for profile URLs (public API)."""
import json
import sys
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; LeadResearchBot/1.0; +https://example.invalid)"


def fetch(handle: str) -> dict | None:
    url = f"https://www.instagram.com/{handle.strip('/')}/"
    api = "https://www.instagram.com/api/v1/oembed/?url=" + urllib.parse.quote(url, safe="")
    req = urllib.request.Request(api, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e), "handle": handle}


def main() -> None:
    handles = [ln.strip() for ln in sys.stdin if ln.strip() and not ln.startswith("#")]
    for i, h in enumerate(handles):
        data = fetch(h)
        rec = {"handle": h, "oembed": data}
        print(json.dumps(rec, ensure_ascii=False))
        sys.stdout.flush()
        time.sleep(0.22)


if __name__ == "__main__":
    main()
