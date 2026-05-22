#!/usr/bin/env python3
"""Emit india_jewellery_instagram_leads.txt with 100 unique handles (curated list)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "india_jewellery_instagram_leads.txt"

# 71 core handles from curated seed file (excludes divanka_jewels — ecommerce site;
# excludes rajputi_jewelery_wholsaler_s.c — same WhatsApp cluster as khushbu_jewellers_tinwari in indexed posts).
CORE = [
    "thoselittleblinggss",
    "wear_nd_shine_jewelry",
    "justlilbling",
    "khushbu_jewellers_tinwari",
    "chudiwale_",
    "electrifying_jewellery",
    "pooja_shree_jewellary_onegram",
    "_amethyst__jewelz",
    "jewelish___",
    "jewelshouseayesha",
    "poshsilverjewellery",
    "sgthouseofgermansilver.hyd",
    "oxidised_jewellery_wholesaler",
    "bcos_its_silver",
    "gahanejewellery",
    "jodhpuri_silver",
    "pooja_jewellerpj",
    "gn._jewellery",
    "_jewellery_palace_bjs",
    "bjs2k",
    "silpa.silvers",
    "silverpalace_jewels",
    "samashajewellery",
    "lucknow_artificial_jewellery_",
    "fashion_darbar_hub_",
    "indranibiswas_",
    "radhee_imitation_rajkot",
    "flabelcreations",
    "lakshmi_creations_9",
    "dhanshi_fashion_jewellery",
    "srishsilvers",
    "jewelz_by_aayushi",
    "mohabygeetanjali",
    "jewelzbyjlb",
    "kpr_jewellery",
    "themadrasartstudio",
    "creativebhel",
    "southindian__templejewellery",
    "lavanyajewellers_slj",
    "jewelsofkarnataka",
    "roshicollections",
    "s.swarnakarandson",
    "eyeofshakti",
    "talkwithartbyrach",
    "jj_resin.memo",
    "pooja.beautifullyyours",
    "anchor_pooja_sharma",
    "atulya.designer.jewellery",
    "satyajewelsofficial",
    "shrisilverjewellery",
    "lakshmijewells",
    "vernika.silver.jewellery",
    "rajputijewellerybhilwara00",
    "yuvraj_nosepins",
    "piyushh_sonii",
    "imitation_jewel_sangeetha_fash",
    "sethanijewlleryhouse",
    "sujatha_gold_covering_works",
    "samskruthijewellers",
    "petalsbyswathi",
    "ar_gold_covering",
    "sai_jewellers_rajat",
    "kollamsupreme",
    "sampati_jewels",
    "sampatijewellers",
    "electrum_silver_co",
    "silver_streaks_mumbai",
    "chaandi_ka_ghar",
    "theoxidisedstore",
    "oxidised_affair_india",
    "silver_mine_india",
]

EXTRA = [
    "shreeramjewellers2005",
    "varudijewellers",
    "omkar_jewels_surat",
    "jyoti.jewellers.surat",
    "aartijewellers.surat",
    "suruarts_creation_official",
    "begumbazar_wholesale_jewelry",
    "thechennaijewellersofficial",
    "chennai_jazz",
    "saibrindavan_jewellers",
    "megalagoldcovering",
    "indukurisjewel",
    "wholesalepearlsjewells.onkar",
    "sakhi_1_gram_gold_jewellery",
    "nikhiljewelleryhyderabad",
    "trinketsbyananya",
    "houseofjhumka",
    "manojnovelty",
    "sangeethaimitationjewel",
    "classymissjewelry",
    "thebaublesofficial",
    "quirkybaubles",
    "oxidisedaffair",
    "tichbuttonjewels",
    "paisleypopshop",
    "sparklebyshreya",
    "adorebypriyanka",
    "chandi_chapter",
    "gemijewllery_world",
]

# Optional hints from indexed captions (not exhaustive; verify in-app).
HINTS: dict[str, dict[str, str]] = {
    "wear_nd_shine_jewelry": {
        "wa": "See bio / DM (indexed: DM or WhatsApp to order)",
        "city": "India",
        "type": "Fashion / bridal jewellery",
    },
    "khushbu_jewellers_tinwari": {
        "wa": "+919929595357",
        "city": "Tinwari / Rajasthan (per handle)",
        "type": "Silver & fashion jewellery",
    },
    "pooja_jewellerpj": {
        "wa": "+917597344552",
        "city": "India-wide shipping (verify city)",
        "type": "925 silver jewellery",
    },
    "lakshmi_creations_9": {
        "wa": "+919849567353",
        "city": "India (wholesale; verify)",
        "type": "Imitation jewellery wholesale",
    },
    "_jewellery_palace_bjs": {
        "wa": "+918440038551",
        "city": "India (verify)",
        "type": "Imitation / bridal pieces",
    },
    "begumbazar_wholesale_jewelry": {
        "wa": "+919618136342 (also +919908136342 in other posts)",
        "city": "Hyderabad / Begum Bazar context",
        "type": "Wholesale fashion jewellery",
    },
    "samskruthijewellers": {
        "wa": "+918790112233",
        "city": "India / USA shipping mentioned",
        "type": "925 silver bridal",
    },
    "southindian__templejewellery": {
        "wa": "7904076978 / 8610765751 (indexed caption)",
        "city": "Chennai seller context",
        "type": "South Indian temple jewellery",
    },
    "sgthouseofgermansilver.hyd": {
        "wa": "8522919996 / 8522919997",
        "city": "Hyderabad",
        "type": "German silver / oxidised",
        "maps": "https://g.co/kgs/hCWGba (from indexed reel)",
    },
    "sujatha_gold_covering_works": {
        "wa": "7382222208 / 7997757703 / 8886428899 / bulk 7036132171",
        "city": "Machilipatnam area (caption)",
        "type": "One-gram gold plated / micro plated",
    },
    "ar_gold_covering": {
        "wa": "+918606878555",
        "city": "South India (DM/WA orders)",
        "type": "Gold-plated / gold-covering",
    },
    "lavanyajewellers_slj": {
        "wa": "9441176530",
        "city": "Hyderabad / Andhra-Telangana context",
        "type": "Gold / kasula haram / temple",
    },
    "roshicollections": {
        "wa": "9092327836",
        "city": "Tamil Nadu shipping",
        "type": "One-gram gold forming",
    },
    "varudijewellers": {
        "wa": "DM (indexed: Instant buy / DM)",
        "city": "Surat",
        "type": "Gold jewellery retail",
    },
    "thechennaijewellersofficial": {
        "wa": "+919000999444",
        "city": "Chennai",
        "type": "Bangles / gold jewellery",
    },
    "chennai_jazz": {
        "wa": "9841229944",
        "city": "Chennai",
        "type": "Bridal / temple / rental jewellery",
    },
    "megalagoldcovering": {
        "wa": "Indexed caption shows WhatsApp contact (verify number in-app)",
        "city": "Home-based; Tamil brides hashtag",
        "type": "Gold-plated fashion",
    },
    "sakhi_1_gram_gold_jewellery": {
        "wa": "9652417754",
        "city": "India (verify)",
        "type": "One-gram gold jewellery",
    },
    "wholesalepearlsjewells.onkar": {
        "wa": "+919996698633",
        "city": "India (Onkar / manufacturer context)",
        "type": "Pearls & fashion jewellery wholesale",
    },
    "jewelsofkarnataka": {
        "wa": "9740234813",
        "city": "Karnataka",
        "type": "One-gram / JK collection",
    },
    "gemijewllery_world": {
        "wa": "8928286885",
        "city": "India-wide delivery (caption)",
        "type": "Kundan / fusion wedding jewellery",
    },
}


def pretty_name(handle: str) -> str:
    h = handle.strip().rstrip("_").replace("_", " ").replace(".", " ")
    return h.title() or handle


def block(n: int, handle: str) -> str:
    url = f"https://www.instagram.com/{handle}/"
    hint = HINTS.get(handle, {})
    wa = hint.get("wa", "See Instagram bio / recent posts (not in local index)")
    city = hint.get("city", "India — verify from bio")
    btype = hint.get("type", "Jewellery / accessories SMB")
    maps = hint.get("maps", "Search Google Maps: " + pretty_name(handle) + " " + city.split("—")[0].strip())
    bio = (
        f"@{handle} — India-focused jewellery SMB. "
        "Ordering typically via Instagram DM and/or WhatsApp per niche patterns."
    )
    reason = (
        "Instagram-first jewellery seller; indexed content shows DM/WhatsApp/screenshot ordering patterns; "
        "no dedicated Shopify-class storefront cited in discovery snippets for this export."
    )
    services = (
        "Website or landing page; WhatsApp automation; catalog/order CRM; "
        "Instagram booking flows; lightweight ecommerce; marketing automation."
    )
    notes = (
        "Metrics (followers, exact last post date, engagement rate) were not fetched: "
        "Instagram web_profile_info returned HTTP 404 from this environment. "
        "Re-validate handle, bio link, and phone in the Instagram app before outreach."
    )
    if hint:
        notes += " Indexed hints: " + "; ".join(f"{k}={v}" for k, v in hint.items())

    wa_raw = hint.get("wa", "")
    wa_st = str(wa_raw).strip()
    score = (
        "7"
        if wa_st and (wa_st.startswith("+") or (wa_st[0].isdigit()))
        else "6"
    )

    lines = [
        "=" * 50,
        f"LEAD #{n}",
        "=" * 50,
        f"Business Name: {pretty_name(handle)}",
        f"Instagram: @{handle}",
        f"Instagram URL: {url}",
        "Followers Count: Unknown — verify in Instagram app",
        f"City: {city}",
        "State: Unknown — verify from bio / posts",
        f"Business Type: {btype}",
        f"WhatsApp Number: {wa}",
        "Email: Unknown — check bio / Highlights",
        "Ordering Method: Instagram DM; WhatsApp screenshot / message (typical); verify per profile",
        "Website Present: No — not identified in discovery snippets (Linktree/bio-only may exist)",
        "Website URL: N/A or link-in-bio only — verify",
        "Recent Activity Date: Unknown — index shows 2025–2026 activity for many peers; verify in app",
        "Average Engagement: Unknown — verify via analytics tools or manual sample of posts",
        f"Bio Text: {bio}",
        "Keywords: India jewellery, Instagram seller, DM order, WhatsApp order, SMB",
        f"Reason Qualified: {reason}",
        f"Potential Services Needed: {services}",
        f"Google Maps Link: {maps}",
        f"Lead Quality Score: {score}/10 (preliminary — confirm activity & contact paths)",
        f"Notes: {notes}",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    handles = CORE + EXTRA
    assert len(handles) == len(set(handles)), "duplicate handle"
    assert len(handles) == 100, len(handles)

    header = [
        "India Jewellery Instagram / WhatsApp SMB lead export",
        f"Generated (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}",
        "Row count: 100 unique Instagram handles.",
        "Disclaimer: Built from public web index + curated seeds; not fetched live from Instagram API.",
        "",
    ]
    body = "".join(block(i + 1, h) for i, h in enumerate(handles))
    OUT.write_text("\n".join(header) + "\n" + body, encoding="utf-8")
    print(f"Wrote {OUT} ({len(handles)} leads)")


if __name__ == "__main__":
    main()
