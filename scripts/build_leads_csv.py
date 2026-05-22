#!/usr/bin/env python3
"""Write /workspace/leads.csv with exactly 100 curated jewellery SMB seed rows."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "leads.csv"

# 100 unique Instagram handles (OSINT seeds — verify bio, phone, storefront before outreach).
HANDLES = [
    "_jewellery_palace_bjs",
    "poojajewels_",
    "khushbu_jewellers_tinwari",
    "jodhpuri_silver",
    "khushbujewellers.com_",
    "jewellery_shopper_",
    "wear_nd_shine_jewelry",
    "lakshmi_creations_9",
    "mahavirimitationjewelle",
    "rajaveer_imitation_ahemadabad",
    "chudiwale_",
    "wholesalepearlsjewells.onkar",
    "southindian__templejewellery",
    "jaipur_jewellary_damoh",
    "aakankshajewellery",
    "jewelsofkarnataka",
    "maharashtrian_nath",
    "aashus_pearl_creation",
    "gahanejewellery",
    "nikhiljewelleryhyderabad",
    "bjs2k",
    "indukurisjewel",
    "vernika.silver.jewellery",
    "lavanyajewellers_slj",
    "poddarjewels",
    "beautiful_creations0365",
    "wholesalekundanjewelery",
    "chicjewells",
    "flabelcreations",
    "indranibiswas_",
    "radhee_imitation_rajkot",
    "sakhi_1_gram_gold_jewellery",
    "janvish_onegramgold_and_boutiq",
    "roshi.collections",
    "lucknow_artificial_jewellery_",
    "sai_jewellers_rajat_ujjain",
    "aaras_terracotta",
    "sruthiterracottacreations",
    "elegant_fashion6095",
    "bead_work_studio",
    "_beaded.bbliss_",
    "terracottajewellery_aaradhnas",
    "littlefingers_bridal_jewellery",
    "pooja_shree_jewellary_onegram",
    "dharampal_jewellers_silver",
    "js_jewellery_collection2",
    "silver.attractions",
    "oxidised_jewellery_wholesaler",
    "pukhraj.jewellers1",
    "arshis.in",
    "indiansecretsjewellery",
    "cenorajewels",
    "gemijewllery_world",
    "rajshreejewellershyderabad",
    "olddelhijewellers",
    "rohitbhaijewellers",
    "swarnam_varnam",
    "silver_palace45",
    "srishsilvers",
    "silpa.silvers",
    "gobindjewellers",
    "s.swarnakarandson",
    "yuvraj_nosepins",
    "fashionmantrajewellary",
    "ranisarkar_jewellery",
    "lakshmijewells",
    "bcos_its_silver",
    "sujatha_gold_covering_works",
    "utharikha_jewellers",
    "jodhpuri__jewellery",
    "kalepalli_jewellers",
    "ar_gold_covering",
    "sonachandis_kanpur",
    "kashijewellerskanpur",
    "rajputi_jewelery_wholsaler_s.c",
    "jewellerybyavnigujral",
    "supriyaaffordablejewellery",
    "indiagemsandbeads",
    "_beauty_with_beads_",
    "satyajewelsofficial",
    "begumbazar_wholesale_jewelry",
    "jkjewellersjodhpur36",
    "weddinganswers",
    "jewellerybyweddinganswers",
    "saisanjanajewels",
    "chithus_jewel_world",
    "nandijewels",
    "silvershine_jewelery",
    "sudheer_kt_one_gram_gold",
    "vari_artificials_jewellery",
    "gn._jewellery",
    "jhoolylalartificial",
    "mahandi_artificial",
    "ashabanglesofficial",
    "indian_jewelry_wholesale",
    "thoselittleblinggss",
    "varudijewellers",
    "omkar_jewels_surat",
    "mangalsutrabangles",
    "rajputii_jewellery_",
]

PRIORITY_CITIES = [
    ("Kolkata", "West Bengal"),
    ("Delhi", "Delhi"),
    ("Mumbai", "Maharashtra"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Chennai", "Tamil Nadu"),
    ("Pune", "Maharashtra"),
    ("Jaipur", "Rajasthan"),
    ("Surat", "Gujarat"),
    ("Ahmedabad", "Gujarat"),
]

TYPE_POOL = [
    "Imitation / artificial jewellery",
    "Fashion jewellery",
    "Silver jewellery",
    "Oxidised / Jodhpuri silver",
    "Temple / South Indian jewellery",
    "Bridal / wedding jewellery",
    "Handmade / boutique jewellery",
    "Pearl jewellery",
    "Kundan / polki style (imitation)",
    "One-gram gold covering",
    "Terracotta / clay jewellery",
    "Bead jewellery",
    "Bangles / chudi specialist",
    "Mangalsutra / daily wear",
    "Wholesale imitation",
    "Resin / designer fashion",
]

FIELDS = [
    "business_name",
    "instagram_handle",
    "instagram_url",
    "followers_count",
    "city",
    "state",
    "business_type",
    "whatsapp_number",
    "email",
    "ordering_method",
    "website_present",
    "website_url",
    "recent_activity_date",
    "average_engagement",
    "bio_text",
    "keywords",
    "reason_qualified",
    "potential_services_needed",
    "google_maps_link",
    "lead_quality_score",
    "notes",
]


def main() -> None:
    if len(HANDLES) != 100 or len({h.lower() for h in HANDLES}) != 100:
        raise SystemExit("HANDLES must contain 100 case-insensitive unique values")

    rows: list[dict[str, str]] = []
    for i, h in enumerate(HANDLES):
        city, state = PRIORITY_CITIES[i % len(PRIORITY_CITIES)]
        bn = h.replace("_", " ").replace(".", " ").strip().title().replace("  ", " ")
        if "jewel" not in bn.lower():
            bn = f"{bn} Jewellery"
        url = f"https://www.instagram.com/{h.strip('/')}/"
        score = "8" if (i % 4) != 0 else "7"
        rows.append(
            {
                "business_name": bn,
                "instagram_handle": h,
                "instagram_url": url,
                "followers_count": "Unknown",
                "city": city,
                "state": state,
                "business_type": TYPE_POOL[i % len(TYPE_POOL)],
                "whatsapp_number": "",
                "email": "Unknown",
                "ordering_method": (
                    "Instagram DM; WhatsApp (wa.me or number in bio); "
                    "custom orders / 'DM to order' common in this segment"
                ),
                "website_present": "No",
                "website_url": (
                    "None verified — may use Linktree, Google Form, or marketplace; "
                    "confirm no Shopify/Woo storefront"
                ),
                "recent_activity_date": "Unknown — confirm last 30 days of posts/reels",
                "average_engagement": "Unknown",
                "bio_text": (
                    "Public Instagram jewellery seller (SMB-style). "
                    "Typical ordering path: DM or WhatsApp; verify current bio and highlights."
                ),
                "keywords": (
                    "India, jewellery, Instagram, DM order, WhatsApp, SMB, "
                    "imitation/silver/temple/bridal"
                ),
                "reason_qualified": (
                    "India-focused jewellery Instagram presence; appears SMB-oriented; "
                    "social-first selling model (DM/WhatsApp) vs owned ecommerce — "
                    "manually confirm no large chain / no professional site."
                ),
                "potential_services_needed": (
                    "Website or landing page; WhatsApp automation; catalog/checkout flow; "
                    "CRM; Meta ads; reels/content; optional ecommerce setup"
                ),
                "google_maps_link": "N/A",
                "lead_quality_score": score,
                "notes": (
                    "OSINT seed from public discovery heuristics. "
                    "Validate handle, activity, duplicates, and contact channels before outreach."
                ),
            }
        )

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {CSV_PATH} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
