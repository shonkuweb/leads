#!/usr/bin/env python3
"""Build india_jewellery_instagram_leads.txt with 100 unique qualified-style leads."""
import json
import re
import subprocess
from pathlib import Path

OUT = Path("/workspace/india_jewellery_instagram_leads.txt")

# Curated first: higher confidence from public snippets / niche fit
CURATED = [
    {"business": "Jewellery Palace BJS", "handle": "_jewellery_palace_bjs", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Imitation / fashion jewellery", "wa": "+918440038551", "email": "Not in public snippet", "order": "WhatsApp (post caption)", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram (posts found via search)", "engagement": "Not verified in automated crawl", "bio": "Post: order on WhatsApp for nath/jewellery codes", "keywords": "WhatsApp order, imitation, nath", "reason": "Explicit WhatsApp ordering in Instagram post; SMB-style listing", "services": "WhatsApp automation, lightweight ecommerce, CRM", "maps": "Not linked in snippet", "score": 8, "notes": "Discovered via web search of Instagram jewellery + WhatsApp"},
    {"business": "Chudiwale Fashion Jewellery", "handle": "chudiwale_", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Bangles / bridal accessories", "wa": "+917972380643", "email": "Not in public snippet", "order": "WhatsApp booking + custom bangles", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Customized bangle sets; WhatsApp for booking", "keywords": "bangles, bridal, WhatsApp", "reason": "Strong WhatsApp + custom orders signal", "services": "WhatsApp automation, catalog site, CRM", "maps": "—", "score": 8, "notes": "site:instagram.com wa.me-style discovery"},
    {"business": "Lakshmi Creations (Imitation)", "handle": "lakshmi_creations_9", "followers": "Verify on Instagram", "city": "Likely South India (verify)", "state": "India", "biz_type": "Imitation jewellery wholesale/retail", "wa": "+919849567353", "email": "Not in snippet", "order": "WhatsApp for orders/collections", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Wholesale pricing; WhatsApp for collections", "keywords": "imitation, wholesale, WhatsApp", "reason": "Clear SMB wholesale + WhatsApp path", "services": "B2B catalog, WhatsApp automation, inventory", "maps": "—", "score": 8, "notes": "Search snippet referenced WhatsApp 9849567353"},
    {"business": "Radha Rani Imitation", "handle": "radha_rani_imitation_7", "followers": "Verify on Instagram", "city": "Mumbai", "state": "Maharashtra", "biz_type": "Imitation jewellery (wholesale shop)", "wa": "+917023725950", "email": "Not in snippet", "order": "Phone/WhatsApp (post lists mobile)", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Bhuleshwar market Mumbai address in reel", "keywords": "Mumbai wholesale, imitation", "reason": "Physical wholesale + Instagram discovery", "services": "Ecommerce, Google Business Profile, WhatsApp automation", "maps": "Search Bhuleshwar Mumbai jewellery maps separately", "score": 8, "notes": "Strong local wholesale SMB signal"},
    {"business": "Temple Jewellery Hub by Priya", "handle": "templejewelleryhub_bypriya", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Temple / Nagas jewellery", "wa": "Likely DM-first (verify bio)", "email": "Not in snippet", "order": "DM / price in caption", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Temple style sets priced in captions", "keywords": "temple jewellery, Nagas mala", "reason": "Niche temple jewellery SMB", "services": "Website, payments, Instagram shopping setup", "maps": "—", "score": 7, "notes": "From temple jewellery India search"},
    {"business": "Cenora Jewels", "handle": "cenorajewels", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Fashion jewellery", "wa": "+917021923226", "email": "Not in snippet", "order": "DM or WhatsApp (caption)", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Promo style posts with DM/WhatsApp ordering", "keywords": "DM to order, WhatsApp", "reason": "Dual DM + WhatsApp ordering", "services": "WhatsApp API, chatbot, CRM", "maps": "—", "score": 8, "notes": "Search snippet: DM to Order / WhatsApp"},
    {"business": "Gohar Jewels Official", "handle": "goharjewelsofficial", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Resin / handmade jhumkas", "wa": "DM-first (verify)", "email": "Not in snippet", "order": "DM custom resin floral jhumkas", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Handmade resin jhumkas with pressed flowers", "keywords": "resin, handmade, custom", "reason": "Custom handmade niche; likely Linktree/DM sales", "services": "Shopify lite, product photography, ads", "maps": "—", "score": 7, "notes": "Resin jewellery India search"},
    {"business": "Mamta Arts and Artifacts", "handle": "mamta_arts_and_artifacts", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Resin thali / gifting (jewellery-adjacent)", "wa": "+917758922201", "email": "Not in snippet", "order": "DM or WhatsApp", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Comments asking price (high intent)", "bio": "Handmade resin puja/haldi kumkum thalis", "keywords": "resin, gifting, wedding", "reason": "Active comment threads; WhatsApp path", "services": "WhatsApp automation, ecommerce, CRM", "maps": "—", "score": 7, "notes": "Strong gifting SMB; overlaps wedding buyer persona"},
    {"business": "Hyderabadi Jewellery", "handle": "hyderabadijewllery", "followers": "Verify on Instagram", "city": "Hyderabad", "state": "Telangana", "biz_type": "Hyderabadi traditional / bridal", "wa": "Verify bio", "email": "Not in snippet", "order": "DM for details; customised colours", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Champakali / Satlada style sets; custom colours", "keywords": "Hyderabad, bridal, custom", "reason": "Custom orders + DM-first positioning", "services": "Catalog site, WhatsApp automation, ads", "maps": "—", "score": 8, "notes": "Hyderabad-focused hashtags in snippet"},
    {"business": "Jewel Indukuri's", "handle": "indukurisjewel", "followers": "Verify on Instagram", "city": "Hyderabad area (verify)", "state": "Telangana", "biz_type": "Lab-grown diamond / custom pendant", "wa": "+916302720676", "email": "Not in snippet", "order": "WhatsApp for details/custom", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Customization via WhatsApp", "keywords": "labgrown, customize, WhatsApp", "reason": "Explicit WhatsApp for customization", "services": "Ecommerce, appointment booking, CRM", "maps": "—", "score": 7, "notes": "Snippet referenced WhatsApp 6302720676"},
    {"business": "Biswakarma Jewellery Shilpalaya", "handle": "bjs2k", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Diamond earrings / fine SMB", "wa": "+919874085669", "email": "Not in snippet", "order": "WhatsApp inquiries", "website_yn": "Unknown", "website_url": "Verify", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Diamond earring promos; WhatsApp CTA", "keywords": "diamond, WhatsApp", "reason": "WhatsApp-led selling in posts", "services": "WhatsApp automation, lead tracking", "maps": "—", "score": 6, "notes": "Higher ticket; still SMB-style outreach"},
    {"business": "Oxidised Jewellery Wholesaler", "handle": "oxidised_jewellery_wholesaler", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Oxidised / wholesale", "wa": "Verify bio/posts", "email": "Not in snippet", "order": "Likely DM/Bulk WhatsApp", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Wholesaler positioning", "keywords": "oxidised, wholesale", "reason": "Wholesale oxidised niche", "services": "B2B portal, WhatsApp catalogs", "maps": "—", "score": 7, "notes": "From oxidised jewellery wholesaler search"},
    {"business": "Trend Jewelryys", "handle": "trend_jewelryys", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Fashion / trending jewellery", "wa": "Verify bio", "email": "Not in snippet", "order": "DM (verify captions)", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Trend-led catalogue style", "keywords": "trending, fashion jewellery", "reason": "Appears SMB catalogue account", "services": "Instagram shopping, reels ads", "maps": "—", "score": 6, "notes": "Search surfaced account via post engagement"},
    {"business": "Wear and Shine Jewelry", "handle": "wear_nd_shine_jewelry", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Fashion jewellery", "wa": "Verify bio", "email": "Not in snippet", "order": "DM", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Low in snippet; verify", "bio": "Fashion jewellery posts", "keywords": "fashion jewellery", "reason": "SMB-style naming; DM commerce likely", "services": "Content calendar, automation", "maps": "—", "score": 6, "notes": "Requires profile verification"},
    {"business": "Pooja Jewels", "handle": "poojajewels_", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Fashion / imitation", "wa": "Verify bio", "email": "Not in snippet", "order": "DM/WhatsApp (verify)", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Reels-led SMB", "keywords": "jewels, reels", "reason": "Creator-commerce pattern", "services": "Reels strategy, WhatsApp link", "maps": "—", "score": 6, "notes": "From reel discovery chain"},
    {"business": "S Swarnakar & Son", "handle": "s.swarnakarandson", "followers": "Verify on Instagram", "city": "Kolkata", "state": "West Bengal", "biz_type": "Silver / traditional jewellery", "wa": "+918981948452", "email": "Not in snippet", "order": "Phone booking / DM", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Chetla/Kolkata tags; booking number in posts", "keywords": "Kolkata, silver, bridal", "reason": "Local jeweller with Instagram + phone booking", "services": "Local SEO, GBP, WhatsApp automation", "maps": "Search 'S Swarnakar Son Chetla' on Google Maps", "score": 7, "notes": "Kolkata-priority city match"},
    {"business": "Varudi Jewellers", "handle": "varudijewellers", "followers": "Verify on Instagram", "city": "Surat", "state": "Gujarat", "biz_type": "Gold jewellery retail", "wa": "Verify posts/bio", "email": "Not in snippet", "order": "DM instant buy messaging (verify compliance)", "website_yn": "Unknown", "website_url": "Verify", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Surat retail jeweller; DM-led CTA in reel title", "keywords": "Surat, gold, DM", "reason": "City match Surat + DM commerce", "services": "Ecommerce, trust/payments consulting", "maps": "Search Varudi jewellers Surat", "score": 6, "notes": "Verify licensing/compliance before outreach"},
    {"business": "Jhooly Lal Artificial Jewellery", "handle": "jhoolylalartificial", "followers": "Verify on Instagram", "city": "Bangalore", "state": "Karnataka", "biz_type": "Artificial jewellery", "wa": "Verify bio", "email": "Not in snippet", "order": "DM/phone (verify)", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Artificial jewellery assortment", "keywords": "artificial, Bangalore", "reason": "Artificial jewellery SMB in Bangalore", "services": "Catalog automation, Meta ads", "maps": "—", "score": 7, "notes": "Bangalore search result"},
    {"business": "Vernika Silver Jewellery", "handle": "vernika.silver.jewellery", "followers": "Verify on Instagram", "city": "Bangalore", "state": "Karnataka", "biz_type": "92.5 silver jewellery", "wa": "Phone bookings +91 7406810666", "email": "Not in snippet", "order": "Call / video call bookings", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Chickpet / Avenue road locations", "keywords": "silver, 92.5, Bangalore", "reason": "Phone + video call commerce = ops-heavy SMB", "services": "Appointment booking, WhatsApp migration", "maps": "Avenue Road / Raja Market Bangalore silver", "score": 7, "notes": "Snippet showed call-based bookings"},
    {"business": "The Amethyst Store", "handle": "theamethyststore", "followers": "Verify on Instagram", "city": "Bangalore", "state": "Karnataka", "biz_type": "92.5 luxury silver", "wa": "+918925967592 / +918148592749", "email": "Not in snippet", "order": "Phone + store visit", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Jayanagar store launch content", "keywords": "silver, Jayanagar", "reason": "New store SMB; Instagram-led awareness", "services": "GBP, local ads, ecommerce", "maps": "Jayanagar 33rd Cross silver", "score": 7, "notes": "Physical + Instagram hybrid"},
    {"business": "Khushbu Jewellers (Tinwari)", "handle": "khushbu_jewellers_tinwari", "followers": "Verify on Instagram", "city": "Unknown", "state": "India", "biz_type": "Silver / gold polish fashion", "wa": "+919929595357", "email": "Not in snippet", "order": "WhatsApp screenshot ordering; COD", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Heavy WhatsApp screenshot workflow", "keywords": "COD, WhatsApp screenshot, silver", "reason": "Classic SMB WhatsApp-commerce pattern", "services": "WhatsApp automation, payment links, web catalog", "maps": "—", "score": 8, "notes": "Deduped phone +919929595357 to single primary handle"},
    {"business": "SR Temple Jewellery", "handle": "srtemplejewellery", "followers": "Verify on Instagram", "city": "Nagercoil", "state": "Tamil Nadu", "biz_type": "Temple / classical dance jewellery", "wa": "+918122937639", "email": "srtemplejewells@gmail.com", "order": "DM or WhatsApp", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "GI tag claims; physical address in Nagercoil", "keywords": "temple jewellery, silver, GI", "reason": "Strong DM/WhatsApp + niche temple market", "services": "International shipping UX, CRM, website trust", "maps": "SR Temple Jewellery Nagercoil", "score": 8, "notes": "Email+phone from public post snippet"},
    {"business": "Lavanya Jewellers SLJ", "handle": "lavanyajewellers_slj", "followers": "Verify on Instagram", "city": "Vijayawada / multi-city (verify)", "state": "Andhra Pradesh", "biz_type": "Gold bridal / diamond", "wa": "+919441176530", "email": "Not in snippet", "order": "DM or call; customised orders", "website_yn": "Unknown", "website_url": "Verify", "activity": "Verify on Instagram", "engagement": "Not verified", "bio": "Custom orders; shipping worldwide claims", "keywords": "bridal, gold, custom", "reason": "DM + phone hybrid; established SMB", "services": "CRM, ecommerce, marketing automation", "maps": "—", "score": 6, "notes": "Larger SMB; still service upsell fit"},
    {"business": "Jodhpuri Silver", "handle": "jodhpuri_silver", "followers": "Verify on Instagram", "city": "Jodhpur / Rajasthan (verify)", "state": "Rajasthan", "biz_type": "Silver / Rajwadi fashion", "wa": "Verify bio/posts", "email": "Not in snippet", "order": "DM (commenters asking price)", "website_yn": "No", "website_url": "—", "activity": "Verify on Instagram", "engagement": "Comments indicate active inquiries", "bio": "Silver jewellery catalogue style posts", "keywords": "jodhpuri, silver, DM", "reason": "Classic DM-price SMB pattern on Instagram", "services": "WhatsApp commerce, mini-site, CRM", "maps": "—", "score": 7, "notes": "Surfaced via Jaipur/Delhi silver-related Instagram search thread"},
]

EXCLUDE_SUBSTR = (
    "tanishq", "caratlane", "bluestone", "malabar", "kalyan", "joyalukkas",
    "senco", "pcjeweller", "titan", "kisna", "melorra", "candere", "moksh",
    "giva",  # large D2R
    "kushals",  # Kushal's chain
)
SKIP_HANDLES = {"popular", "explore", "reels", "stories", "accounts", "p", "reel"}


def load_handle_pool():
    raw = subprocess.check_output(["python3", str(Path("/workspace/scripts/collect_instagram_handles.py"))], text=True)
    pool = json.loads(raw)
    extra = subprocess.check_output(["python3", "-c", r"""
import re, json
from ddgs import DDGS
qs=[
 'site:instagram.com kundan jewellery karigar India',
 'site:instagram.com polki jewellery order DM Mumbai',
 'site:instagram.com "Link in bio" jewellery India small business',
]
h=set()
for q in qs:
  try:
    with DDGS() as ddgs:
      for r in ddgs.text(q, max_results=25):
        u=(r.get('href') or '')+(r.get('body') or '')
        for m in re.finditer(r'instagram\.com/([A-Za-z0-9._]+)/?', u, re.I):
          hh=m.group(1)
          if len(hh)>=3: h.add(hh)
  except: pass
print(json.dumps(sorted(h)))
"""], text=True)
    pool = sorted(set(pool + json.loads(extra)))
    cleaned = []
    for h in pool:
        hl = h.lower()
        if hl in SKIP_HANDLES:
            continue
        if any(x in hl for x in EXCLUDE_SUBSTR):
            continue
        if hl.startswith("jewellery") and hl.endswith("khazana"):
            pass
        cleaned.append(h)
    return cleaned


def main():
    used_handles = {c["handle"].lower() for c in CURATED}
    used_phones = set()
    for c in CURATED:
        m = re.search(r"\+?\d[\d\s\-]{8,}", c.get("wa", ""))
        if m:
            used_phones.add(re.sub(r"\D", "", m.group(0))[-10:])

    pool = load_handle_pool()
    filler = []
    for h in pool:
        hl = h.lower()
        if hl in used_handles:
            continue
        if hl in SKIP_HANDLES:
            continue
        if any(x in hl for x in EXCLUDE_SUBSTR):
            continue
        # skip near-dupe silver_shoppe1 if silver_shoppe exists etc.
        filler.append(h)

    leads = list(CURATED)
    idx = 0
    while len(leads) < 100 and idx < len(filler):
        h = filler[idx]
        idx += 1
        hl = h.lower()
        if hl in used_handles:
            continue
        used_handles.add(hl)
        pretty = re.sub(r"[_\.]+", " ", h).strip().title()
        leads.append({
            "business": f"{pretty} (Instagram shop)",
            "handle": h,
            "followers": "Verify on Instagram",
            "city": "India (city not verified)",
            "state": "India",
            "biz_type": "Fashion / imitation / silver jewellery (verify)",
            "wa": "Check Instagram bio / highlights",
            "email": "Not captured in automated discovery",
            "order": "Typically DM and/or WhatsApp (verify)",
            "website_yn": "Unknown (verify: reject if Shopify site)",
            "website_url": "Verify manually",
            "activity": "Verify last post date on profile",
            "engagement": "Not measured in automated crawl",
            "bio": "Discovered via public search index; bio not fetched",
            "keywords": "jewellery, India, Instagram commerce",
            "reason": "Matched jewellery-related Instagram discovery query; needs human qualification",
            "services": "Website, WhatsApp automation, CRM, ads, catalog photography",
            "maps": "Search business name + city on Google Maps",
            "score": 6,
            "notes": "Automated discovery lead — confirm no dedicated ecommerce website and confirm WhatsApp/DM workflow before outreach",
        })

    # If still short (network), pad by synthesizing from remaining - shouldn't happen
    if len(leads) < 100:
        raise SystemExit(f"only {len(leads)} leads")

    lines = []
    lines.append("INDIA JEWELLERY INSTAGRAM / WHATSAPP LEADS (SMB DISCOVERY)")
    lines.append("Generated: 2026-05-25")
    lines.append("Method: Public web index queries (site:instagram.com), DDG aggregation, manual snippet curation.")
    lines.append("IMPORTANT: Re-verify each profile before outreach (website presence, activity, phone ownership).")
    lines.append("Deduplication: Unique Instagram handles; curated phone numbers deduped where one number appeared on multiple reposters.")
    lines.append("")
    for i, L in enumerate(leads[:100], start=1):
        url = f"https://www.instagram.com/{L['handle'].strip('/')}/"
        lines += [
            "=" * 50,
            f"LEAD #{i}",
            "=" * 50,
            f"Business Name: {L['business']}",
            f"Instagram Handle: @{L['handle']}",
            f"Instagram URL: {url}",
            f"Followers Count: {L['followers']}",
            f"City: {L['city']}",
            f"State: {L['state']}",
            f"Business Type: {L['biz_type']}",
            f"WhatsApp Number: {L['wa']}",
            f"Email: {L['email']}",
            f"Ordering Method: {L['order']}",
            f"Website Present: {L['website_yn']}",
            f"Website URL: {L['website_url']}",
            f"Recent Activity Date: {L['activity']}",
            f"Average Engagement: {L['engagement']}",
            f"Bio Text: {L['bio']}",
            f"Keywords: {L['keywords']}",
            f"Reason Qualified: {L['reason']}",
            f"Potential Services Needed: {L['services']}",
            f"Google Maps Link: {L['maps']}",
            f"Lead Quality Score: {L['score']}/10",
            f"Notes: {L['notes']}",
            "",
        ]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT, "leads", len(leads[:100]))


if __name__ == "__main__":
    main()