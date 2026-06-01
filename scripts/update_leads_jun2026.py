#!/usr/bin/env python3
"""Replace low-scoring leads and refresh cron metadata."""

from pathlib import Path

FILE = Path("/workspace/india_jewellery_instagram_leads.txt")

REPLACEMENTS = {
    62: """==================================================
LEAD #62
==================================================
Business Name: Chezhiyan Velli Maaligai
Instagram Handle: @chezian_velli_maaligai
Instagram URL: https://www.instagram.com/chezian_velli_maaligai/
Followers Count: Unknown (not in indexed sources)
City: Chennai
State: Tamil Nadu
Business Type: 925 silver / custom laser rings
WhatsApp Number: +917010078402
Email: N/A
Ordering Method: DM; WhatsApp for custom silver orders
Website Present: No
Website URL: N/A
Recent Activity Date: 2024-01 (indexed reel C2tf2iUPVUs)
Average Engagement: Medium (custom name rings; silver wedding bands)
Bio Text: DM or WhatsApp order for customised 92.5 silver pieces
Keywords: silver, custom, DM, WhatsApp, Chennai
Reason Qualified: Explicit DM + WhatsApp CTAs; no dedicated ecommerce site in index
Potential Services Needed: WhatsApp catalog; DM automation; custom order CRM
Google Maps Link: N/A
Lead Quality Score: 8/10
Notes: Replaced curator lead 2026-06-01 cron; verify bio for store address.

""",
    64: """==================================================
LEAD #64
==================================================
Business Name: Fashion Darbar Hub
Instagram Handle: @fashion_darbar_hub_
Instagram URL: https://www.instagram.com/fashion_darbar_hub_/
Followers Count: Unknown (not in indexed sources)
City: Hyderabad
State: Telangana
Business Type: Fashion / couple jewellery
WhatsApp Number: +918829911024
Email: N/A
Ordering Method: WhatsApp screenshot order; COD India
Website Present: No
Website URL: N/A
Recent Activity Date: 2025-04 (indexed post DI22EO0JK3x)
Average Engagement: Medium (couple bracelet combos ₹4000)
Bio Text: Send screenshot on WhatsApp for order; COD available
Keywords: WhatsApp, screenshot order, COD, couple jewellery
Reason Qualified: WhatsApp-first selling; no professional standalone store in index
Potential Services Needed: WhatsApp automation; payment links; Instagram shop setup
Google Maps Link: N/A
Lead Quality Score: 8/10
Notes: Replaced duplicate Kolkata handle 2026-06-01 cron.

""",
    75: """==================================================
LEAD #75
==================================================
Business Name: Gobind Jewellers
Instagram Handle: @gobindjewellers
Instagram URL: https://www.instagram.com/gobindjewellers/
Followers Count: Unknown (not in indexed sources)
City: Durgapur
State: West Bengal
Business Type: Hallmarked gold / silver bridal
WhatsApp Number: +919593222111
Email: N/A
Ordering Method: Call or WhatsApp; home delivery WB/Jharkhand
Website Present: No
Website URL: N/A
Recent Activity Date: 2025-05 (indexed post DJBivb4oBi3)
Average Engagement: Medium (bridal chur/socket collections)
Bio Text: CALL OR WHATSAPP; Chandidas Market Durgapur
Keywords: WhatsApp, bridal, hallmarked, Durgapur, home delivery
Reason Qualified: WhatsApp ordering on posts; IG-led promotions (SMB showroom)
Potential Services Needed: WhatsApp CRM; ecommerce for catalog; delivery automation
Google Maps Link: https://www.google.com/maps/search/Chandidas+Market+Durgapur
Lead Quality Score: 7/10
Notes: Replaced weak regional placeholder 2026-06-01 cron; has physical store.

""",
    77: """==================================================
LEAD #77
==================================================
Business Name: Al-Wahab Resin Floral Jewellery (Seno Boutique)
Instagram Handle: @seno.boutique.jewellery
Instagram URL: https://www.instagram.com/seno.boutique.jewellery/
Followers Count: Unknown (not in indexed sources)
City: Unknown
State: India
Business Type: Resin floral / handmade jewellery
WhatsApp Number: N/A
Email: N/A
Ordering Method: DM to order; customisation available
Website Present: No
Website URL: N/A
Recent Activity Date: 2024-06 (indexed reel C8aBqD4oGsx)
Average Engagement: Medium (resin jhumka reels; handmade tags)
Bio Text: DM to order; customization available
Keywords: DM to order, resin, handmade, custom
Reason Qualified: Instagram-only DM sales flow; resin niche SMB
Potential Services Needed: DM automation; WhatsApp bridge; custom order forms
Google Maps Link: N/A
Lead Quality Score: 9/10
Notes: Replaced unknown Rajasthan placeholder 2026-06-01 cron.

""",
    79: """==================================================
LEAD #79
==================================================
Business Name: Lalaland Jewellery Studio
Instagram Handle: @lalalandjewellerystudio
Instagram URL: https://www.instagram.com/lalalandjewellerystudio/
Followers Count: Unknown (not in indexed sources)
City: Bangalore
State: Karnataka
Business Type: Fashion / boutique jewellery
WhatsApp Number: N/A
Email: N/A
Ordering Method: DM to order (indexed site:instagram.com discovery)
Website Present: No
Website URL: N/A
Recent Activity Date: Unknown
Average Engagement: Unknown
Bio Text: Boutique studio; verify WhatsApp in bio
Keywords: jewellery studio, Bangalore, DM order
Reason Qualified: Discovered via DM-order search batch; no Shopify in index
Potential Services Needed: Website; WhatsApp automation; Instagram growth
Google Maps Link: N/A
Lead Quality Score: 7/10
Notes: Replaced spelling-variant placeholder 2026-06-01 cron; confirm activity on profile.

""",
}


def replace_lead(text: str, num: int, new_block: str) -> str:
    start_marker = f"==================================================\nLEAD #{num}\n"
    start = text.find(start_marker)
    if start == -1:
        raise SystemExit(f"Lead #{num} not found")
    next_lead = text.find("\n==================================================\nLEAD #", start + 1)
    if next_lead == -1:
        raise SystemExit(f"Next lead after #{num} not found")
    return text[:start] + new_block + text[next_lead + 1 :]


def main() -> None:
    text = FILE.read_text(encoding="utf-8")
    text = text.replace(
        "Last automation run: 2026-05-29T17:30:00Z (cron)",
        "Last automation run: 2026-06-01T17:30:00Z (cron)",
    )
    text = text.replace(
        "Last refresh: Replaced 2 leads + enriched 1 (May-2026 indexed DM/WhatsApp discoveries).",
        "Last refresh: Replaced 5 low-score leads (4/10) with Jun-2026 DM/WhatsApp discoveries.",
    )
    for num in sorted(REPLACEMENTS):
        text = replace_lead(text, num, REPLACEMENTS[num])
    FILE.write_text(text, encoding="utf-8")
    handles = [line.split("@", 1)[1].strip() for line in text.splitlines() if line.startswith("Instagram Handle: @")]
    assert len(handles) == len(set(handles)), "Duplicate handles detected"
    assert len(handles) == 100, f"Expected 100 leads, got {len(handles)}"
    print("OK: 100 unique handles")


if __name__ == "__main__":
    main()
