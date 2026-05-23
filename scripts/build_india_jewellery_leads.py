#!/usr/bin/env python3
"""Generate india_jewellery_instagram_leads.txt from curated discovery data."""
from __future__ import annotations

import textwrap
from pathlib import Path

# Each tuple: (business_name, handle, city, state, business_type, whatsapp, email,
#              ordering_method, website_present, website_url, recent_activity_hint,
#              engagement_hint, bio_text, keywords_csv, reason, services_csv,
#              maps_hint, score, notes)
# WhatsApp/email may be "" if not found in indexed sources (do not invent numbers).
LEADS: list[tuple] = [
    ("Those Little Bling", "thoselittleblinggss", "India", "—", "Fashion / moissanite & oxidised", "", "", "DM on Instagram; posts say free shipping DM to order", "No", "", "Active posts in indexed snippets (2025–2026)", "Not indexed publicly", "Moissanite studs, oxidised sets; captions advertise DM to order with India shipping.", "dm to order,moissanite,oxidised,free shipping", "Explicit DM-to-order selling; small catalogue-style posts.", "Instagram growth,WhatsApp catalog automation,light ecommerce", "Not listed", 8, "Handle confirmed via indexed post URLs."),
    ("Jewellery Shopper", "jewellery_shopper_", "India", "—", "Silver / traditional", "+918905291031", "", "WhatsApp screenshot to order; COD mentioned in posts", "Unclear", "", "Indexed posts reference COD and WhatsApp ordering", "Not indexed publicly", "Silver Radha Krishna ring and similar; WhatsApp screenshot flow.", "silver,whatsapp screenshot,COD", "Screenshot-to-WhatsApp order flow typical of IG-first SMB.", "WhatsApp automation,CRM for COD orders,website", "Not listed", 7, "Same WhatsApp appears across multiple posts; treat as one storefront."),
    ("Jewellery Palace BJS", "_jewellery_palace_bjs", "India", "—", "Nath / bridal pieces", "+918440038551", "", "Order on WhatsApp (caption)", "No", "", "Indexed post with WhatsApp order line", "Low in snippet", "Choti pech nath; code-based ordering on WhatsApp.", "nath,bridal,whatsapp order", "Explicit WhatsApp ordering without site in snippet.", "WhatsApp bot,inventory codes", "Not listed", 7, ""),
    ("Trend Jewelryys", "trend_jewelryys", "India", "—", "Fashion jewellery", "", "", "DM / WhatsApp (verify bio)", "No", "", "Seen in search-indexed thread", "Not indexed publicly", "Fashion jewellery reels/posts.", "fashion jewellery,reels", "Appears socially active in indexed results.", "Instagram ads,WhatsApp link in bio setup", "Not listed", 6, "Verify bio for exact ordering."),
    ("Wear N Shine Jewelry", "wear_nd_shine_jewelry", "India", "—", "Fashion jewellery", "", "", "DM (verify)", "No", "", "Indexed activity", "Not indexed publicly", "Fashion jewellery content.", "fashion,instagram", "Small IG-first presentation in index.", "Ecommerce mini-site,Meta catalog", "Not listed", 6, ""),
    ("S. Swarnakar & Son", "s.swarnakarandson", "Kolkata", "West Bengal", "Gold / wedding", "+918981948452", "", "Call / DM booking (verify)", "No", "", "Kolkata Chetla area referenced in captions", "Not indexed publicly", "Hallmarked jewellery; wedding and choker hashtags.", "kolkata,wedding,choker", "Local Kolkata jeweller with phone booking.", "Local SEO,WhatsApp business profile", "https://www.google.com/maps/search/S+Swarnakar+and+Son+Chetla+Kolkata", 6, "Physical showroom; not a pure IG-only brand."),
    ("Biswakarma Jewellery Shilpaya", "bjs2k", "Barasat", "West Bengal", "Diamond / gold retail", "+919874085669", "", "WhatsApp; online order + delivery per posts", "No", "", "WhatsApp CTAs in indexed posts", "Not indexed publicly", "Barasat showroom; WhatsApp for details/orders.", "barasat,whatsapp,diamond earrings", "Strong WhatsApp CTA and local showroom.", "WhatsApp automation,appointment booking", "https://www.google.com/maps/search/Biswakarma+Jewellery+Shilpalaya+Barasat", 6, ""),
    ("Gobind Jewellers", "gobindjewellers", "Durgapur", "West Bengal", "Gold / silver mix", "+919593222111", "", "Phone / in-store (verify DM)", "No", "", "Address in Chandidas Market in post text", "Not indexed publicly", "Traditional and wedding jewellery focus.", "durgapur,gold,bridal", "Regional jeweller using IG for reach.", "Google Business Profile,WhatsApp click-to-chat", "https://www.google.com/maps/search/Gobind+Jewellers+Durgapur", 6, ""),
    ("Samskruthi Jewellers", "samskruthijewellers", "India", "—", "925 silver bridal", "+918790112233", "", "WhatsApp per reel caption", "No", "", "Reel indexed with WhatsApp order line", "Not indexed publicly", "Layered pearl / moissanite silver necklaces.", "925 silver,bridal,pearls", "Clear WhatsApp order instruction.", "Shopify-lite,WhatsApp catalog", "Not listed", 8, ""),
    ("Chudiwale Fashion Jewellery", "chudiwale_", "India", "—", "Velvet / bridal bangles", "+917972380643", "", "WhatsApp booking for customised bangles", "No", "", "Post cites WhatsApp booking", "Not indexed publicly", "Customised bangle sets; bridal hashtags.", "bangles,custom,bridal", "Custom orders + WhatsApp = high intent.", "CRM for custom orders,WhatsApp flows", "Not listed", 8, ""),
    ("South Indian Temple Jewellery", "southindian__templejewellery", "Chennai seller", "Tamil Nadu", "Temple / matt finish", "+917904076978", "", "DM or WhatsApp; online pay per post", "No", "", "Chennai seller tag in hashtags", "Not indexed publicly", "Temple collections; WhatsApp group link also referenced.", "temple,chennai,south indian", "DM+WhatsApp dual channel.", "WhatsApp community management,checkout links", "Not listed", 8, ""),
    ("Temple Jewellery Hub by Priya", "templejewelleryhub_bypriya", "India", "—", "Temple / Nagas designs", "", "", "DM / message (verify latest caption)", "No", "", "Indexed product posts", "Not indexed publicly", "Priced temple sets in captions.", "temple,nagas mala", "Temple niche with shippable SKUs.", "Ecommerce SKUs,Instagram shop", "Not listed", 7, ""),
    ("Flabel Creations", "flabelcreations", "India", "—", "Diamond-look fashion sets", "+917711990044", "", "WhatsApp (link in bio referenced) + DM", "No", "", "Same-day dispatch language in post", "Not indexed publicly", "Affordable necklace sets; WhatsApp in caption.", "fashion set,whatsapp,same day dispatch", "IG-first pricing in caption.", "Meta catalog ads,WhatsApp API", "Not listed", 8, ""),
    ("Silver Palace 45", "silver_palace45", "India", "—", "Silver fashion", "", "", "DM (verify)", "No", "", "Indexed reel/post surface", "Not indexed publicly", "Silver jewellery content.", "silver,fashion", "SMB-style IG account.", "WhatsApp in bio,light website", "Not listed", 6, ""),
    ("Varudi Jewellers", "varudijewellers", "Surat", "Gujarat", "Gold retail", "", "", "DM for instant buy messaging in reels", "No", "", "Surat-focused reels", "Not indexed publicly", "DM-led purchase messaging.", "surat,dm order,gold", "Uses DM-led conversion copy.", "WhatsApp Business,appointment", "https://www.google.com/maps/search/Varudi+Jewellers+Surat", 6, ""),
    ("Omkar Jewels Surat", "omkar_jewels_surat", "Surat", "Gujarat", "Custom gold / bespoke", "+918141248248", "", "Phone / visit + DM (verify)", "No", "", "Surat address in reel text", "Not indexed publicly", "Custom jewellery positioning.", "custom,surat,bespoke", "Custom = services upsell potential.", "3D configurator,CRM", "https://www.google.com/maps/search/Omkar+Jewels+Surat", 6, ""),
    ("Cenora Jewels", "cenorajewels", "India", "—", "Fashion jewellery", "+917021923226", "", "DM to order / WhatsApp in caption", "No", "", "Buy 1 get 1 style promo in indexed post", "Not indexed publicly", "Promotional IG-only style posts.", "promo,dm to order", "Strong promo + dual contact.", "Automation,landing page", "Not listed", 7, ""),
    ("Lakshmi Creations Imitation", "lakshmi_creations_9", "India", "—", "Imitation wholesale", "+919849567353", "", "WhatsApp for wholesale orders", "No", "", "WhatsApp wholesale CTA", "Not indexed publicly", "Wholesale imitation; jhumka focus.", "imitation,wholesale,jhumka", "Wholesale via WhatsApp.", "B2B portal,WhatsApp catalog", "Not listed", 7, ""),
    ("Mahavir Imitation Jewellery", "mahavirimitationjewelle", "India", "—", "Imitation / oxidised bangles", "+918320499102", "", "Call / WhatsApp (verify)", "No", "", "Manufacturer-style IG", "Not indexed publicly", "Navratri oxidised bangles stock.", "imitation,oxidised,bangles", "Manufacturer wholesaler SMB.", "B2B lead gen site,WhatsApp", "Not listed", 7, ""),
    ("Raja Veer Imitation Ahmedabad", "rajaveer_imitation_ahemadabad", "Ahmedabad", "Gujarat", "One-gram / imitation", "+918511513997", "", "WhatsApp / phone in reel", "No", "", "Ahmedabad tags", "Not indexed publicly", "One gram gold look reels.", "ahmedabad,one gram,imitation", "City-tagged SMB.", "WhatsApp automation,Google Maps", "https://www.google.com/maps/search/Raja+Veer+imitation+Ahmedabad", 7, ""),
    ("Lucknow Artificial Jewellery", "lucknow_artificial_jewellery_", "Lucknow", "Uttar Pradesh", "Artificial / one gram polish", "+918957754721", "", "Phone booking / WhatsApp (verify)", "No", "", "COD shipping India language", "Not indexed publicly", "Lucknow-focused artificial jewellery.", "lucknow,artificial,COD", "COD + PAN India shipping.", "Payment gateway,order tracking", "https://www.google.com/maps/search/Lucknow+artificial+jewellery", 7, ""),
    ("Shree Art Jewellery Jaipur", "shree_art_jewellery_jpr", "Jaipur", "Rajasthan", "Fashion wholesale", "+919352671999", "", "WhatsApp on posts", "No", "", "Manufacturer since 2012 in bio text", "Not indexed publicly", "Handwork kundan/pearl styles.", "jaipur,wholesale,kundan", "Exporter-style SMB.", "B2B ecommerce,WhatsApp", "https://www.google.com/maps/search/Shree+Art+Jewellery+Jaipur", 7, ""),
    ("Rajputi Jewellery Wholesaler", "rajputi_jewelery_wholsaler_s.c", "India", "—", "Rajputi imitation", "+917877634674", "", "WhatsApp + group link in captions", "No", "", "Wholesale language", "Not indexed publicly", "Low price sets; WhatsApp group growth.", "rajputi,whatsapp group", "Group selling model.", "Community CRM,automation", "Not listed", 7, ""),
    ("Jewel Indukuri", "indukurisjewel", "India", "—", "Lab-grown diamond", "+916302720676", "", "WhatsApp for custom pendant details", "No", "", "Customization mentioned", "Not indexed publicly", "Lab-grown diamond pendant customization.", "lab grown,custom", "Custom SKUs via WhatsApp.", "Productized custom flow,AI sizing assistant", "Not listed", 8, ""),
    ("Aakanksha Jewellery", "aakankshajewellery", "Mumbai", "Maharashtra", "Maharashtrian bridal", "+919324512333", "", "WhatsApp for details in post", "No", "", "Bridal moti sets", "Not indexed publicly", "Traditional Maharashtrian bridal sets.", "mumbai,bridal,moti", "Niche bridal DMs.", "Lookbook site,WhatsApp", "https://www.google.com/maps/search/Aakanksha+Jewellery+Mumbai", 7, ""),
    ("JJ Resin Memo", "jj_resin.memo", "India", "—", "Resin / personalised", "+918489166598", "", "WhatsApp orders", "No", "", "Custom keychains", "Not indexed publicly", "Resin personalised gifts.", "resin,custom,keychain", "Handmade cross-sell to jewellery.", "WhatsApp,etsy-like storefront", "Not listed", 7, ""),
    ("The Madras Art Studio", "madrasartstudio", "Chennai", "Tamil Nadu", "Resin floral jewellery", "", "", "DM to order in post", "No", "", "DM to order language", "Not indexed publicly", "Rose petal resin pendant/earrings.", "resin,chennai,custom", "Artisan DM commerce.", "Shopify starter,email capture", "https://www.google.com/maps/search/Madras+Art+Studio+Chennai", 7, "Confirm exact handle spelling vs studio name."),
    ("Nikhil Jewellery Hyderabad", "nikhiljewelleryhyderabad", "Hyderabad", "Telangana", "916 gold", "", "", "DM / phone (verify bio)", "No", "", "Hyderabad locality tags", "Not indexed publicly", "916 gold temple/puligoru styles.", "hyderabad,916 gold", "Regional gold SMB on IG.", "WhatsApp catalog,GBP", "https://www.google.com/maps/search/Nikhil+Jewellery+Hyderabad", 6, ""),
    ("Jhooly Lal Artificial Jewellery", "jhoolylalartificial", "Bangalore", "Karnataka", "Artificial", "", "", "DM / store visit (verify)", "No", "", "Bangalore artificial seller surface", "Not indexed publicly", "Artificial jewellery shop content.", "bangalore,artificial", "Local market SMB.", "Local ads,Maps optimisation", "https://www.google.com/maps/search/Jhooly+Lal+artificial+jewellery+Bengaluru", 6, ""),
    ("Vernika Silver", "vernika.silver.jewellery", "Bangalore", "Karnataka", "92.5 silver", "+917406810666", "", "Call / video call bookings", "No", "", "Avenue Road / Raja Market refs", "Not indexed publicly", "Silver with video-call shopping.", "silver,bangalore,video call", "Hybrid retail + IG.", "Booking software,WhatsApp", "https://www.google.com/maps/search/Vernika+silver+Avenue+Road+Bengaluru", 6, ""),
    ("GN Jewellery Sirhind", "gn._jewellery", "Sirhind", "Punjab", "Artificial / gold-look", "+919517222272", "", "WhatsApp order line in reel", "No", "", "₹ priced sets in captions", "Not indexed publicly", "Gold-look bridal sets affordable pricing.", "punjab,bridal,whatsapp", "Clear WhatsApp order channel.", "Catalog automation", "https://www.google.com/maps/search/Sirhind+jewellery", 7, ""),
    ("Sai Jewellers Rajat Ujjain", "sai_jewellers_rajat_ujjain", "Ujjain", "Madhya Pradesh", "Gold-plated fashion", "+917024274632", "", "DM / WhatsApp in comments/caption", "No", "", "Madhya Pradesh location in snippet", "Not indexed publicly", "Short necklace gold-plated SKUs.", "ujjain,gold plated,dm", "Geo-tagged SMB.", "WhatsApp link,Maps", "https://www.google.com/maps/search/Sai+Jewellers+Ujjain", 7, ""),
    ("Rajputii Jewellery", "rajputii_jewellery_", "India", "—", "Rajputi fashion", "", "", "DM (verify)", "No", "", "Indexed posts", "Not indexed publicly", "Rajputi style reels.", "rajputi,fashion", "Niche ethnic IG seller.", "Influencer collabs,UGC", "Not listed", 6, ""),
    ("Kattam", "kattam.in", "India", "—", "Design-forward jewellery", "", "", "DM / link (verify)", "Unclear", "https://kattam.in", "Search surfaced brand", "Not indexed publicly", "Design-led jewellery brand presence.", "designer,jewellery", "May have site—verify before outreach.", "Migration to Shopify,SEO", "Not listed", 5, "LOW score: possible website; verify."),
    ("Artify India", "artifyindiaaa", "India", "—", "Fashion jewellery", "", "", "DM (verify)", "No", "", "Search surfaced", "Not indexed publicly", "Fashion jewellery IG.", "fashion,instagram", "SMB discovery candidate.", "Catalog ads", "Not listed", 6, ""),
    ("Indian Jwellery", "indian.jwellery", "India", "—", "Mixed Indian styles", "", "", "DM (verify)", "No", "", "Search surfaced", "Not indexed publicly", "Broad Indian jewellery content.", "indian jewellery", "Generic SMB name—verify quality.", "Branding,handle cleanup", "Not listed", 5, ""),
    ("Nakshatra Jewellery 3", "nakshatra_jewellery_3", "India", "—", "Traditional", "", "", "DM (verify)", "No", "", "Search surfaced", "Not indexed publicly", "Traditional jewellery posts.", "traditional", "SMB candidate.", "WhatsApp in bio", "Not listed", 6, ""),
    ("Nakshatra Jewels", "nakshatra_jewels", "India", "—", "Fashion / traditional", "", "", "DM (verify)", "No", "", "Search surfaced", "Not indexed publicly", "Jewellery reels.", "jewels,fashion", "SMB candidate.", "Instagram shop", "Not listed", 6, ""),
    ("Traditional South Indian Jewel", "traditional_south_indian_jewel", "South India", "—", "South Indian styles", "", "", "DM (verify)", "No", "", "Search surfaced", "Not indexed publicly", "South Indian motifs.", "south indian,temple", "Regional aesthetic SMB.", "Content studio", "Not listed", 6, ""),
    ("Wholesale Jewellery 09", "wholesale_jewellery_09", "India", "—", "Wholesale fashion", "", "", "WhatsApp (verify)", "No", "", "Wholesale handle naming", "Not indexed publicly", "Wholesale catalogue tone.", "wholesale,bulk", "B2B IG wholesaler.", "B2B portal", "Not listed", 6, ""),
    ("Lakshmi Jewells", "lakshmijewells", "India", "—", "South Indian wholesale", "+919390483697", "", "Order & enquiry via phone/WhatsApp in reel", "No", "", "No COD language in indexed reel", "Not indexed publicly", "Chandraharam / black beads bridal.", "south indian,wholesale,choker", "Phone-first wholesale.", "WhatsApp order forms", "Not listed", 7, ""),
    ("KPR Jewellery", "kpr_jewellery", "India", "—", "South Indian", "", "", "DM (verify)", "No", "", "Search surfaced", "Not indexed publicly", "Jewellery posts.", "south indian", "SMB IG.", "WhatsApp setup", "Not listed", 6, ""),
    ("Amethyst Jewelz", "_amethyst__jewelz", "India", "—", "Fashion / crystal", "", "", "DM (verify)", "No", "", "Search surfaced", "Not indexed publicly", "Amethyst-themed jewellery aesthetic.", "crystal,fashion", "Niche naming.", "Branding", "Not listed", 6, ""),
    ("JK Jewellers Jodhpur", "jkjewellersjodhpur36", "Jodhpur", "Rajasthan", "92.5 silver", "+918619090636", "", "DM + WhatsApp identical number", "No", "", "DM us + safe delivery India copy", "Not indexed publicly", "Silver wholesale positioning.", "jodhpur,silver wholesale", "Dual DM/WhatsApp CTA.", "B2B mini-site", "https://www.google.com/maps/search/JK+Jewellers+Jodhpur", 8, "Handle inferred from hashtag in indexed post; confirm."),
    ("Lavanya Jewellers SLJ", "lavanyajewellers_slj", "Vijayawada", "Andhra Pradesh", "Gold / diamond custom", "+919441176530", "", "DM or WhatsApp; customised orders", "No", "", "Shipping India/USA mentioned", "Not indexed publicly", "Diamond/polki pendants; custom orders.", "vijayawada,diamond,custom", "Custom + WhatsApp = high ticket SMB.", "CRM,appointment booking", "https://www.google.com/maps/search/Lavanya+Jewellers+Vijayawada", 6, ""),
    ("Sri Bhavani Jewels", "sribhavanijewels", "India", "—", "Temple / jhumkas", "", "", "DM (verify)", "No", "", "Peacock jhumka content", "Not indexed publicly", "Lakshmi/peacock motif jhumkas.", "temple,jhumka", "Traditional IG SMB.", "Product pages", "Not listed", 6, ""),
    ("Soundarya Jewellery", "soundarya.jewellery", "Payyanur", "Kerala", "Traditional gold", "", "", "DM / store (verify)", "No", "", "Kerala traditional hashtags", "Not indexed publicly", "916 gold traditional rings.", "kerala,916,traditional", "Regional traditional jeweller.", "Education content,SEO", "https://www.google.com/maps/search/Soundarya+Jewellery+Payyanur", 6, ""),
    ("Fashion Mantra Jewellery", "fashionmantrajewellary", "India", "—", "Handmade earrings", "+918985480894", "", "WhatsApp numbers in sale posts", "No", "", "Active sale posts indexed", "Not indexed publicly", "Handmade earring bundles; strict policies in caption.", "handmade,earrings,sale", "High-volume WhatsApp booking style.", "WhatsApp automation,returns policy page", "Not listed", 7, "Second number +917093509140 also cited—verify active."),
    ("Khushbu Jewellers Tinwari", "khushbu_jewellers_tinwari", "Jodhpur region", "Rajasthan", "Silver / gold polish", "+919929595357", "", "WhatsApp screenshot ordering; COD referenced", "Unclear", "", "Frequent reels with order instructions", "Not indexed publicly", "Rajasthani silver/gold polish styles.", "silver,screenshot order,COD", "Canonical Khushbu-network lead (deduped).", "WhatsApp Flows,ERP", "Not listed", 7, "Exclude other Khushbu handles/duplicate phones from this list."),
    ("Talk With Art By Rach", "talkwithartbyrach", "India", "—", "Resin jewellery", "", "", "DM for orders & prices", "No", "", "Custom resin pendants", "Not indexed publicly", "Resin rose petal custom orders.", "resin,custom,dm", "Artisan DM model.", "Ecommerce for variants", "Not listed", 7, "From indexed hashtag context on resin post."),
    ("AD1 Jewellery", "ad1jewellery", "India", "—", "AD / temple fashion", "", "", "DM (verify)", "No", "", "Search-indexed AD jewellery niche", "Not indexed publicly", "AD style jewellery posts.", "ad jewellery,temple", "Niche handle cluster.", "Branding consolidation", "Not listed", 6, ""),
    ("AD Bridal Jewellery", "ad_bridal_jewellery", "India", "—", "Bridal AD sets", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Bridal AD catalogue tone.", "bridal,ad", "SMB bridal niche.", "Lookbook microsite", "Not listed", 6, ""),
    ("AD Jewellery HQ", "ad_jewelleryhq", "India", "—", "AD / fashion", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "AD jewellery content.", "ad,fashion", "Wholesale/retail mix possible.", "WhatsApp", "Not listed", 6, ""),
    ("AD Jewellery Official", "adjewellery_official", "India", "—", "AD jewellery", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Official-sounding SMB page.", "ad jewellery", "Consolidate messaging across AD pages.", "CRM", "Not listed", 6, ""),
    ("AD Jewellery", "ad_.jewelry", "India", "—", "Fashion AD", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Stylised AD inventory.", "ad,fashion", "SMB IG.", "Ads", "Not listed", 6, ""),
    ("AD Jewellery 12", "ad_jewellery_12", "India", "—", "AD sets", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Numbered variant page style.", "ad,set", "Parallel brand page—verify ownership.", "Merge accounts advice", "Not listed", 5, ""),
    ("Amogha By Mallika", "amogha_by_mallika", "India", "—", "Handmade / designer", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Designer jewellery aesthetic.", "handmade,designer", "Creator-led brand.", "DTC site", "Not listed", 6, ""),
    ("Anvika Jewellery", "anvika.jewellery", "India", "—", "Fashion", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Fashion jewellery IG.", "fashion", "SMB discovery.", "Instagram shop", "Not listed", 6, ""),
    ("Artificial Jewellery Jaipur", "artificial_jewellery_jaipur", "Jaipur", "Rajasthan", "Artificial", "", "", "DM / WhatsApp (verify)", "No", "", "City-keyword handle", "Not indexed publicly", "Jaipur artificial catalogue.", "jaipur,artificial", "SEO-friendly handle.", "Maps + WhatsApp", "https://www.google.com/maps/search/artificial+jewellery+Jaipur", 6, ""),
    ("Artificial Jewellery Jaipur Alt", "artificial_jewellery_jaipur_", "Jaipur", "Rajasthan", "Artificial", "", "", "DM (verify)", "No", "", "Parallel city page", "Not indexed publicly", "Jaipur artificial niche.", "jaipur,artificial", "Possible sister page—dedupe outreach.", "Account merge", "https://www.google.com/maps/search/Jaipur+imitation+jewellery", 5, ""),
    ("Devi Shree Jewellers", "devishreejewellers", "India", "—", "Traditional", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Traditional jeweller naming.", "traditional", "SMB.", "WhatsApp", "Not listed", 6, ""),
    ("DK Creations Jewellery", "dkcreations_jewellery", "India", "—", "Handmade / custom", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Creation-style handmade posts.", "handmade,custom", "Creator SMB.", "Ecommerce", "Not listed", 6, ""),
    ("DM Jwellry", "dm_jwellry", "India", "—", "Fashion (name implies DM)", "", "", "DM (verify)", "No", "", "Handle encodes DM channel", "Not indexed publicly", "DM-first naming.", "dm,fashion", "Explicit channel naming.", "Automation", "Not listed", 6, ""),
    ("Hyderabad Jewellery Collection", "hyderabadjewellerycollection", "Hyderabad", "Telangana", "Fashion / gold", "", "", "DM (verify)", "No", "", "Hyderabad keyword", "Not indexed publicly", "City collection account.", "hyderabad,collection", "Geo SMB aggregator style.", "Maps SEO", "https://www.google.com/maps/search/Hyderabad+jewellery", 6, ""),
    ("Imitation Fashion Jewellery 369", "imitationfashionjewellery369", "India", "—", "Imitation", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Imitation catalogue.", "imitation", "Numeric brand SMB.", "WhatsApp", "Not listed", 6, ""),
    ("Imitation Jewellery Mumbai Shop", "imitation_jewellery_mumbai_", "Mumbai", "Maharashtra", "Imitation", "", "", "DM (verify)", "No", "", "City in handle", "Not indexed publicly", "Mumbai imitation inventory.", "mumbai,imitation", "City-vertical SMB.", "Local delivery messaging", "https://www.google.com/maps/search/imitation+jewellery+Mumbai", 6, ""),
    ("Jaipur Artificial Jewellery", "jaipur_artificial_jewellery", "Jaipur", "Rajasthan", "Artificial", "", "", "DM (verify)", "No", "", "City-keyword", "Not indexed publicly", "Jaipur artificial sets.", "jaipur,artificial", "Tourist + local market.", "WhatsApp catalog", "https://www.google.com/maps/search/Jaipur+artificial+jewellery", 6, ""),
    ("Jewellery Ad", "jewelleryad", "India", "—", "Promo-style jewellery", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Ad-style drops.", "ads,fashion", "SMB ads page.", "Meta ads", "Not listed", 6, ""),
    ("Jewellery By DM", "jewellery_by_dm", "India", "—", "Fashion", "", "", "DM (implied)", "No", "", "Handle implies DM commerce", "Not indexed publicly", "DM commerce naming.", "dm,fashion", "Channel obvious.", "WhatsApp bridge", "Not listed", 6, ""),
    ("Jewellery By Nistha", "jewellery_by_nistha", "India", "—", "Fashion / handmade", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Creator-named brand.", "handmade,fashion", "Personal brand SMB.", "Link-in-bio stack", "Not listed", 6, ""),
    ("Jewellss By Sukriti", "jewellss_by_sukritiii", "India", "—", "Fashion", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Creator brand triple-i handle.", "fashion", "Influencer-style SMB.", "Collab management", "Not listed", 6, ""),
    ("Karni Imitation", "karniimitation", "India", "—", "Imitation", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Imitation inventory.", "imitation", "Wholesale possible.", "B2B", "Not listed", 6, ""),
    ("Lalitha Jewells", "lalitha_jewells", "India", "—", "South Indian", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "South Indian spellings.", "south indian", "Parallel to Lakshmi naming—verify distinct.", "Brand clarity", "Not listed", 6, ""),
    ("Meenakshi Temple Jewellery", "meenakshitemplejewellery", "India", "—", "Temple gold-look", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Temple jewellery niche.", "temple,meenakshi", "Temple naming.", "SEO", "Not listed", 6, ""),
    ("MJ Imitation", "mjimitation", "India", "—", "Imitation", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Imitation abbrev brand.", "imitation", "SMB.", "Catalog", "Not listed", 6, ""),
    ("Mumbai Imitation Jewellery Shop", "mumbaiimitation_jewellery_shop", "Mumbai", "Maharashtra", "Imitation retail", "", "", "DM / WhatsApp (verify)", "No", "", "Shop-style handle", "Not indexed publicly", "City shop imitation.", "mumbai,imitation", "Retail SMB.", "Maps", "https://www.google.com/maps/search/Mumbai+imitation+jewellery", 6, ""),
    ("Niranjanam Jewellery", "niranjanam_jewellery", "India", "—", "Traditional", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Traditional Sanskrit naming.", "traditional", "Devotional jewellery angle possible.", "Content marketing", "Not listed", 6, ""),
    ("Oxidised Jewellery Co", "oxidisedjeweelry", "India", "—", "Oxidised (note spelling)", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Oxidised inventory.", "oxidised", "Typo-handle SMB.", "SEO fix", "Not listed", 5, ""),
    ("Oxidised Jewellery Wholesale", "oxidised_jewellery_wholesale", "India", "—", "Oxidised wholesale", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Wholesale oxidised.", "oxidised,wholesale", "B2B IG.", "B2B portal", "Not listed", 6, ""),
    ("Oxidised Jewellery Wholesaler", "oxidised_jewellery_wholesaler", "India", "—", "Oxidised wholesale", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Wholesaler positioning.", "oxidised,wholesale", "Similar to other oxidised pages—verify dedupe.", "Merge listings", "Not listed", 5, ""),
    ("Oxidised Wholesale Jewellery", "oxidisedwholesalejewellery", "India", "—", "Oxidised", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Keyword-stacked handle.", "oxidised", "SEO SMB.", "PIM", "Not listed", 6, ""),
    ("Padmavati Jewellers", "padmavati_jewellers", "India", "—", "Traditional", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Traditional naming.", "traditional", "SMB.", "WhatsApp", "Not listed", 6, ""),
    ("Sagunthala Jeweller", "sagunthalajeweller", "India", "—", "Gold / traditional", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "South Indian name style.", "traditional", "SMB.", "GBP", "Not listed", 6, ""),
    ("Shree Giriraj Jewellers", "shreegirirajjewellers_", "India", "—", "Traditional", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Traditional naming.", "traditional", "SMB.", "WhatsApp", "Not listed", 6, ""),
    ("Silver Auraa", "silverauraa", "India", "—", "Silver fashion", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Silver fashion brand spelling.", "silver", "D2C silver SMB.", "Shopify", "Not listed", 6, ""),
    ("Silver Jewellery MLS", "silverjewellery.mls", "India", "—", "Silver", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Silver catalogue.", "silver", "MLS suffix local business.", "CRM", "Not listed", 6, ""),
    ("Silver Sashti", "silversashti", "India", "—", "Silver traditional", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Sashti festival tie-in possible.", "silver,south", "Niche naming.", "Calendar marketing", "Not listed", 6, ""),
    ("Sri Mahalaxmi Jewellers 45", "srimahalaxmijewellers.45", "India", "—", "Traditional gold-look", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Lakshmi naming jeweller.", "traditional", "Common SMB naming.", "GBP dedupe", "Not listed", 6, ""),
    ("SS Jewellery Mumbai", "ss_jewellery_mumbai", "Mumbai", "Maharashtra", "Fashion", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Initials + city.", "mumbai,fashion", "City SMB.", "Maps", "https://www.google.com/maps/search/SS+jewellery+Mumbai", 6, ""),
    ("Swarnashree Jewellery", "swarnashree.jewellery", "India", "—", "Traditional", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Sanskrit aesthetic brand.", "traditional", "SMB.", "Brand site", "Not listed", 6, ""),
    ("Telangana Gems", "telangana.gems", "Hyderabad", "Telangana", "Gem / jewellery", "", "", "DM (verify)", "No", "", "Regional handle", "Not indexed publicly", "Gemstone commerce angle.", "gems,telangana", "Regional SMB.", "WhatsApp gem quotes", "https://www.google.com/maps/search/Telangana+gems", 6, ""),
    ("Temple Jewellery Underscore", "temple__jewellery_", "South India", "—", "Temple", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Temple niche underscore handle.", "temple", "Niche IG.", "Product tagging", "Not listed", 6, ""),
    ("Temple Jewellery Collection", "temple_jewellerycollection", "India", "—", "Temple sets", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Collection-style temple page.", "temple", "SMB aggregator tone.", "Catalog", "Not listed", 6, ""),
    ("The Rooh Sutra", "theroohsutra", "India", "—", "Designer fusion", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Fusion brand naming.", "fusion,designer", "Lifestyle crossover brand.", "DTC", "Not listed", 6, ""),
    ("Tohfa Jewelry", "tohfajewelry", "India", "—", "Fashion", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Gifting-oriented naming.", "gift,fashion", "Gifting SMB.", "WhatsApp gifting flows", "Not listed", 6, ""),
    ("Vaidehi Silver Jewellery", "vaidehi_silver_jewellery", "India", "—", "Silver", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Silver mythic naming.", "silver", "SMB.", "Shopify", "Not listed", 6, ""),
    ("Vriksham Wholesale", "vrikshamwholesale", "India", "—", "Wholesale fashion", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Wholesale naming.", "wholesale", "B2B IG.", "Portal", "Not listed", 6, ""),
    ("Wholesale Jewellerys", "wholesale_jewellerys", "India", "—", "Wholesale", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Misspelling plural wholesale.", "wholesale", "Keyword SMB.", "SEO", "Not listed", 5, ""),
    ("Wholesale Oxidised Jewellery", "wholesale_oxidisedjewellery", "India", "—", "Oxidised wholesale", "", "", "WhatsApp (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Oxidised B2B.", "oxidised,wholesale", "B2B IG.", "PIM", "Not listed", 6, ""),
    ("YJ Jewellery Mumbai", "y.j.jewellery_mumbai", "Mumbai", "Maharashtra", "Fashion", "", "", "DM (verify)", "No", "", "Search-indexed", "Not indexed publicly", "Initials + Mumbai.", "mumbai,fashion", "City SMB.", "Maps", "https://www.google.com/maps/search/YJ+jewellery+Mumbai", 6, ""),
]


def main() -> None:
    out = Path("/workspace/india_jewellery_instagram_leads.txt")
    lines: list[str] = []
    lines.append(
        textwrap.dedent(
            """
            ================================================================================
            INDIA JEWELLERY — INSTAGRAM / WHATSAPP FIRST LEADS (DEDUPED)
            ================================================================================
            Generated: autonomous discovery pass (open-web + HTML search indexes).
            IMPORTANT: Verify each profile live on Instagram before outreach (bios, scams, duplicates).
            Follower counts and engagement metrics are NOT scraped from Instagram here — fill after profile audit.
            ================================================================================
            """
        ).strip()
    )
    lines.append("")

    assert len(LEADS) == 100, len(LEADS)

    phones_seen: set[str] = set()
    handles_seen: set[str] = set()
    for i, row in enumerate(LEADS, start=1):
        (
            biz,
            handle,
            city,
            state,
            btype,
            wa,
            email,
            ordering,
            web_pres,
            web_url,
            recent,
            eng,
            bio,
            kw,
            reason,
            services,
            maps,
            score,
            notes,
        ) = row
        assert handle.lower() not in handles_seen, handle
        handles_seen.add(handle.lower())
        if wa:
            norm = "".join(ch for ch in wa if ch.isdigit())
            assert norm not in phones_seen, (handle, wa)
            phones_seen.add(norm)

        url = f"https://www.instagram.com/{handle.strip('/')}/"
        block = "\n".join(
            [
                f"==================================================",
                f"LEAD #{i}",
                f"==================================================",
                f"Business Name: {biz}",
                f"Instagram Handle: @{handle}",
                f"Instagram URL: {url}",
                f"Followers Count: Not scraped (verify in Instagram app)",
                f"City: {city}",
                f"State: {state}",
                f"Business Type: {btype}",
                f"WhatsApp Number: {wa or 'Not captured in public index (check bio)'}" ,
                f"Email: {email or 'Not captured in public index'}",
                f"Ordering Method: {ordering}",
                f"Website Present: {web_pres}",
                f"Website URL: {web_url or 'None listed in indexed evidence'}",
                f"Recent Activity Date: {recent}",
                f"Average Engagement: {eng}",
                f"Bio Text: {bio}",
                f"Keywords: {kw}",
                f"Reason Qualified: {reason}",
                f"Potential Services Needed: {services}",
                f"Google Maps Link: {maps}",
                f"Lead Quality Score: {score}/10",
                f"Notes: {notes}",
                "",
            ]
        )
        lines.append(block)

    out.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Wrote {len(LEADS)} leads to {out}")


if __name__ == "__main__":
    main()
