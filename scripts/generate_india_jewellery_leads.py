#!/usr/bin/env python3
"""Write india_jewellery_instagram_leads.txt with 100 unique, real Instagram handles.

Data is compiled from public search snippets and lightweight Instagram HTML
fetches (parent account links). Fields such as followers and full bios are
often not available without authenticated scraping; those are marked Unknown
or include a short excerpt when the search snippet provided one.
"""

from __future__ import annotations

from pathlib import Path
import textwrap

# Keys: business, handle, city, state, type, whatsapp, email, ordering,
# website_yesno, website_url, recent_activity, engagement, bio_excerpt,
# keywords, reason, services, maps, score, notes

RAW: list[tuple] = [
    ("Jewellery Palace BJS", "_jewellery_palace_bjs", "Unknown", "India", "Imitation / nath", "+918440038551", "N/A", "WhatsApp (post)", "No", "N/A", "Unknown", "Unknown", "Order on WhatsApp; code-based SKUs", "WhatsApp, nath, imitation", "Indexed post shows WhatsApp order line", "WhatsApp automation; catalog microsite", "N/A", "8", "Verify city from profile."),
    ("Jewellery Shopper", "jewellery_shopper_", "Unknown", "India", "Silver rings / traditional", "+918905291031", "N/A", "WhatsApp screenshot order; COD mentioned", "No", "N/A", "Unknown", "Unknown", "WhatsApp screenshot flow; website discount mention", "silver, COD", "Indexed reel text", "WhatsApp CRM", "N/A", "8", "Confirm if separate ecommerce competes with IG."),
    ("Samskruthi Jewellers", "samskruthijewellers", "Unknown", "India", "925 silver bridal / pearls", "+918790112233", "N/A", "WhatsApp to order", "Unknown", "Not in snippet", "Unknown", "Unknown", "Layered pearl necklace reel", "925 silver, pearls", "Reel: WhatsApp on 8790112233", "Lightweight checkout", "N/A", "7", "Check for standalone site."),
    ("Trend Jewelryys", "trend_jewelryys", "Unknown", "India", "Fashion jewellery", "N/A", "N/A", "DM / comments", "Unknown", "N/A", "Unknown", "Unknown", "Trending-style posts", "trending", "Search index shows engagement", "IG growth", "N/A", "6", "WhatsApp not confirmed in snippet."),
    ("Wear N Shine Jewelry", "wear_nd_shine_jewelry", "Unknown", "India", "Fashion jewellery", "N/A", "N/A", "DM / comments", "Unknown", "N/A", "Unknown", "Unknown", "Fashion jewellery posts", "fashion", "Indexed engagement", "DM automation", "N/A", "6", "Qualify bio."),
    ("Biswakarma Jewellery Shilpaya", "bjs2k", "Kolkata", "West Bengal", "Diamond nosepins / earrings", "+919874085669", "N/A", "WhatsApp for orders", "Unknown", "N/A", "Unknown", "Unknown", "Multiple WhatsApp numbers in different posts", "diamond, nosepin, WhatsApp", "Captions push WhatsApp", "WhatsApp automation", "N/A", "7", "Also alternate formatting 09874085669 in some posts."),
    ("Jewels of Karnataka", "jewelsofkarnataka", "Karnataka", "Karnataka", "One-gram gold fashion", "+919740234813", "N/A", "WhatsApp", "No", "N/A", "Unknown", "Unknown", "One gram gold havala earrings", "one gram gold, WhatsApp", "Post: WhatsApp contact", "UPI receipt automation", "N/A", "8", "Strong SMB signals."),
    ("Mahavir Imitation Jewellery", "mahavirimitationjewelle", "Unknown", "India", "Imitation / oxidised wholesale", "+918320499102", "N/A", "Call / WhatsApp for designs", "Unknown", "N/A", "Unknown", "Unknown", "Navratri oxidised bangles", "imitation, wholesale", "Call number in caption", "B2B catalog", "N/A", "7", "Wholesale tone."),
    ("Flabel Creations", "flabelcreations", "Unknown", "India", "AD / diamond-look sets", "+917711990044", "N/A", "WhatsApp + DM; link in bio referenced", "No", "N/A", "Unknown", "Unknown", "Same-day dispatch claim", "AD jewellery, WhatsApp", "Caption lists WhatsApp", "Link-in-bio landing", "N/A", "8", "Verify bio destination."),
    ("Rajaveer Imitation Ahmedabad", "rajaveer_imitation_ahemadabad", "Ahmedabad", "Gujarat", "Imitation", "N/A", "N/A", "DM / Gujarati inquiries", "Unknown", "N/A", "Unknown", "Unknown", "Imitation reels", "Ahmedabad", "High engagement in index", "Localized ads", "N/A", "6", "Confirm WhatsApp."),
    ("Oxidised Jewellery Wholesaler", "oxidised_jewellery_wholesaler", "Unknown", "India", "Oxidised wholesale", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Wholesale oxidised posts", "oxidised", "Handle niche match", "Catalog", "N/A", "6", "Sparse indexed contact."),
    ("Khushbu Jewellers Tinwari", "khushbu_jewellers_tinwari", "Jodhpur area", "Rajasthan", "Rajwadi silver / gold polish", "+919929595357", "N/A", "WhatsApp screenshot; COD", "Unknown", "N/A", "Unknown", "Unknown", "Customization available", "silver, COD, customize", "Indexed Hindi/English caption", "WhatsApp CRM", "N/A", "9", "High-fit SMB."),
    ("Rajputi Jewellery Bhilwara", "rajputijewellerybhilwara00", "Bhilwara", "Rajasthan", "Rajputi plated sets", "+919829900459", "N/A", "WhatsApp; UPI", "No", "N/A", "Unknown", "Unknown", "Handmade look claims", "rajputi, plated", "WhatsApp ordering explicit", "Checkout", "N/A", "8", "Verify product claims."),
    ("Jodhpuri Silver", "jodhpuri_silver", "Jodhpur region", "Rajasthan", "Silver fashion", "N/A", "N/A", "DM / price in comments", "Unknown", "N/A", "Unknown", "Unknown", "Silver catalogue", "jodhpuri silver", "Comments ask price", "IG shop", "N/A", "7", "Confirm WA in bio."),
    ("Vira Jewels", "_virajewels_", "Unknown", "India", "Fashion / demi-fine", "N/A", "N/A", "Comment for product links", "Unknown", "N/A", "Unknown", "Unknown", "Comment funnel", "comment for links", "Engagement tactic visible", "Link automation", "N/A", "7", "Verify WA."),
    ("Wedding Collection Hyderabad", "weddingcollections143", "Hyderabad", "Telangana", "Hyderabadi / kundan bridal", "+919837777292", "N/A", "DM / call / WhatsApp", "No", "N/A", "Unknown", "Unknown", "Free shipping hashtag", "Hyderabad, bridal", "Caption lists WhatsApp", "Ads + catalog", "N/A", "8", "Indexed geo tags."),
    ("Nikhil Jewellery Hyderabad", "nikhiljewelleryhyderabad", "Hyderabad", "Telangana", "916 gold traditional", "N/A", "N/A", "Store + IG hybrid", "Unknown", "N/A", "Unknown", "Unknown", "Gold reels; LB Nagar tags", "916, Hyderabad", "Physical jeweller", "Omnichannel", "https://maps.google.com/?q=Nikhil+Jewellery+Hyderabad", "5", "Showroom-heavy."),
    ("Wedding Answers", "weddinganswers", "Pan-India", "India", "Wedding accessories / boxes", "+918368213149", "N/A", "WhatsApp or DM", "No", "N/A", "Unknown", "Unknown", "Advance payment; Paytm/GPay", "wedding, chooda box", "Indexed post", "CRM", "N/A", "8", "Jewellery-adjacent."),
    ("Lavanya Jewellers", "lavanyajewellers_slj", "Vijayawada / multi-city", "Andhra Pradesh", "Custom gold / diamond pendants", "+919441176530", "N/A", "DM or WhatsApp", "Unknown", "N/A", "Unknown", "Unknown", "Shipping India & USA mentioned", "custom, gold, bridal", "Reel snippet shows DM/WhatsApp", "Website modernization", "N/A", "7", "Established jeweller."),
    ("Jewel Indukuri's", "indukurisjewel", "Unknown", "India", "Lab-grown diamond custom", "+916302720676", "N/A", "WhatsApp details", "Unknown", "N/A", "Unknown", "Unknown", "Customize pendant chains", "labgrown, customize", "Reel text", "Appointment booking", "N/A", "7", "Premium niche."),
    ("Chudiwale Fashion Jewellery", "chudiwale_", "Unknown", "India", "Custom bangles", "+917972380643", "N/A", "WhatsApp booking", "No", "N/A", "Unknown", "Unknown", "Velvet bangle sets", "bangles, bridal", "Post caption", "WhatsApp flows", "N/A", "8", "Clear WA CTA."),
    ("Lakshmi Creations Imitation", "lakshmi_creations_9", "Unknown", "India", "Imitation wholesale", "+919849567353", "N/A", "WhatsApp", "No", "N/A", "Unknown", "Unknown", "Wholesale prices mention", "imitation, wholesale", "Post caption", "Catalog", "N/A", "8", "Wholesale."),
    ("Sujatha Gold Covering Works", "sujatha_gold_covering_works", "Machilipatnam area", "Andhra Pradesh", "One-gram gold / micro plated", "+917036132171", "N/A", "WhatsApp; COD; bulk", "Unknown", "N/A", "Unknown", "Unknown", "Multiple numbers in posts", "one gram gold, COD", "Bulk + video call", "Inventory tools", "N/A", "9", "Also 7382222208 etc. in posts — pick primary."),
    ("Chithu's Jewel World", "chithus_jewel_world", "Perundurai", "Tamil Nadu", "Fashion rent/sale", "+919865299960", "N/A", "Call / WhatsApp", "No", "N/A", "Unknown", "Unknown", "Stall address in posts", "rent, sale", "Cross-linked from designers", "Maps SEO", "N/A", "7", "Offline stall."),
    ("SS Regha Designers", "ss_regha_designers", "Perundurai", "Tamil Nadu", "Jewellery offers / promos", "N/A", "N/A", "Referral posts", "Unknown", "N/A", "Unknown", "Unknown", "Promotes other stall", "offers", "Network SMB", "Collaboration", "N/A", "5", "May not be primary seller."),
    ("Bhairav Jewellers BJT", "bhairavbjt", "Mumbai", "Maharashtra", "Silver payal manufacturer", "N/A", "N/A", "Office visit + short link", "Partial", "bit.ly in reel", "Unknown", "Unknown", "Kalbadevi address", "silver payal, Mumbai", "Physical office", "Local SEO", "https://maps.google.com/?q=Kalbadevi+Road+Mumbai", "6", "Resolve bit.ly destination."),
    ("Shree Silver Pune", "silver_jewels_pune", "Pune", "Maharashtra", "925 silver retail", "N/A", "N/A", "Shop + online (ambiguous)", "Unknown", "N/A", "Unknown", "Unknown", "Raviwar Peth address", "925, Pune", "Store-first", "Delivery UX", "N/A", "6", "Clarify ecommerce."),
    ("Vernika Silver", "vernika.silver.jewellery", "Bengaluru", "Karnataka", "925 silver", "+917406810666", "N/A", "Call bookings; video call", "No", "N/A", "Unknown", "Unknown", "Raja Market / Avenue Road", "925, Chikpete", "Reel text", "Scheduling", "N/A", "7", "Physical."),
    ("The Amethyst Store", "theamethyststore", "Bengaluru", "Karnataka", "Luxury 92.5 silver", "+918925967592", "N/A", "Call / DM", "Unknown", "N/A", "Unknown", "Unknown", "Jayanagar 4th block", "luxury silver", "Phone numbers in reel", "Maps listing", "N/A", "6", "Premium boutique."),
    ("Sri Sai Silvers by Priya", "sri_sai_silvers", "Unknown", "India", "Handmade 92.5 colour stones", "N/A", "N/A", "Likely DM", "Unknown", "N/A", "Unknown", "Unknown", "Handmade hashtags", "handmade silver", "Posts emphasize handmade", "IG shop", "N/A", "7", "Find WA in bio."),
    ("Ramala Collections Silver", "silverjewelleryramala", "Unknown", "India", "925 silver chains", "+919398255253", "N/A", "Phone order", "Yes", "Indexed title mentions website", "Unknown", "Unknown", "Long silver haram designs", "925, pagadam", "Phone in post", "Shopify tune-up", "N/A", "6", "May have site."),
    ("Varudi Jeweller", "varudijewellers", "Surat", "Gujarat", "Gold retail", "N/A", "N/A", "DM instant buy", "Unknown", "N/A", "Unknown", "Unknown", "BIS mention in reel text", "Surat, gold", "DM-led", "Trust content", "N/A", "7", "Verify WA."),
    ("Pukhraj Jewellers", "pukhraj.jewellers1", "Ahmedabad", "Gujarat", "22kt antique gold", "+919409151772", "N/A", "DM / WhatsApp / call", "No", "N/A", "Unknown", "Unknown", "Satellite address in caption", "custom, hallmark", "Explicit DM/WA", "CRM", "N/A", "7", "Showroom + IG."),
    ("Begum Bazar Wholesale Jewelry", "begumbazar_wholesale_jewelry", "Hyderabad", "Telangana", "One-gram gold wholesale", "+919618136342", "N/A", "DM / WhatsApp screenshot", "No", "N/A", "Unknown", "Unknown", "Begum Bazar tag", "one gram gold", "Screenshot order instructions", "Catalog automation", "N/A", "9", "Very IG-commerce native."),
    ("Roshi Collections", "roshi.collections", "Tamil Nadu", "Tamil Nadu", "One-gram gold forming", "+919092327836", "N/A", "WhatsApp; no COD", "No", "N/A", "Unknown", "Unknown", "TN shipping emphasis", "one gram gold", "Multiple indexed posts", "UPI automation", "N/A", "9", "Trusted page self-claim in post."),
    ("Janvish One Gram Gold & Boutique", "janvish_onegramgold_and_boutiq", "Unknown", "India", "One-gram gold + boutique", "+918121769801", "N/A", "WhatsApp; WA group", "No", "N/A", "Unknown", "Unknown", "Screenshot order + price list style", "one gram gold", "Group updates mention", "Community commerce", "N/A", "8", "Group-based."),
    ("Sai Jewellers Rajat Ujjain", "sai_jewellers_rajat_ujjain", "Ujjain", "Madhya Pradesh", "Gold-plated jewellery", "+917024274632", "N/A", "WhatsApp / DM", "No", "N/A", "Unknown", "Unknown", "Also 9907916141 referenced on Threads index", "1gm gold, MP", "Dual numbers possible", "Number routing", "N/A", "8", "Validate active number."),
    ("South Indian Temple Jewellery", "southindian__templejewellery", "Chennai", "Tamil Nadu", "Matt / temple style", "+9197904076978", "N/A", "DM / WhatsApp; no COD", "No", "N/A", "Unknown", "Unknown", "WhatsApp group invite link in post", "temple, south india", "UPI only", "Group ops", "N/A", "9", "Second number 8610765751 in some posts."),
    ("Satya Jewels Official", "satyajewelsofficial", "Unknown", "India", "Temple gold wholesale", "+919999155985", "N/A", "Call", "Unknown", "N/A", "Unknown", "Unknown", "Wholesale wording", "temple gold", "Call-led", "WA migration", "N/A", "6", "Less IG-native."),
    ("Gohar Jewels Official", "goharjewelsofficial", "Unknown", "India", "Resin jhumkas", "N/A", "N/A", "DM custom", "No", "N/A", "Unknown", "Unknown", "Pressed flowers in resin", "resin, handmade", "Maker brand", "Shopify lite", "N/A", "8", "Niche maker."),
    ("Aashu's Pearl Creation", "aashus_pearl_creation", "Maharashtra", "Maharashtra", "Maharashtrian handmade", "N/A", "N/A", "DM order", "No", "N/A", "Unknown", "Unknown", "Customization available", "handmade, DM", "Regional traditional", "Ecommerce", "N/A", "8", "Festive collections."),
    ("Nath Sringar by Supriya", "nath_sringar_by_supriya", "Maharashtra", "Maharashtra", "Nath / earcuff handmade", "N/A", "N/A", "DM / WhatsApp", "No", "N/A", "Unknown", "Unknown", "Custom colours", "nath, handmade", "Explicit DM/WP", "CRM", "N/A", "8", "Strong custom."),
    ("Rajputi Poshak Jewellery Sari", "rajputi_poshak_jewellery_sari", "Rajasthan", "Rajasthan", "Poshak + jewellery", "N/A", "N/A", "DM / comments", "Unknown", "N/A", "Unknown", "Unknown", "Mixed catalogue", "rajputi", "Cross-sell SMB", "Catalog split", "N/A", "6", "Apparel mix."),
    ("Asha Bangles Official", "ashabanglesofficial", "North India", "India", "Punjabi bridal chura", "+917014592741", "N/A", "WhatsApp", "No", "N/A", "Unknown", "Unknown", "Partial COD mention", "chura, bridal", "Long experience claim", "WA automation", "N/A", "8", "Bridal accessory."),
    ("Radhee Imitation Rajkot", "radhee_imitation_rajkot", "Rajkot", "Gujarat", "Imitation wholesale/retail", "+917383704729", "N/A", "WhatsApp booking", "No", "N/A", "Unknown", "Unknown", "Physical address Jivraj Park", "imitation, Rajkot", "Indexed post", "POS", "N/A", "8", "Second line sometimes listed."),
    ("Artify Indiaaa", "artifyindiaaa", "Unknown", "India", "Fashion jewellery", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "DDG discovery", "fashion", "Search-only signal", "Audit", "N/A", "5", "Needs profile pass."),
    ("Ideal Jewellery by Manju", "idealjewellerybymanju", "Unknown", "India", "Fashion jewellery", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "DDG discovery", "fashion", "Search-only", "Audit", "N/A", "5", "Needs profile pass."),
    ("Indian Jwellery", "indian.jwellery", "Unknown", "India", "Mixed Indian styles", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Aggregator-style name", "Indian jewellery", "Search hit", "Branding", "N/A", "5", "Verify seller vs repost."),
    ("Shreeji Jewellery 1984", "shreejijewellery1984", "Unknown", "India", "Traditional", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Year in handle", "traditional", "Search hit", "Rebrand", "N/A", "5", "Audit age/activity."),
    ("Silver Jewellery Indian", "silver_jewellery_indian", "Unknown", "India", "Silver catalogue", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Silver niche", "silver", "Search hit", "Shopify", "N/A", "5", "Audit WA."),
    ("Wholesale Jewellery 09", "wholesale_jewellery_09", "Unknown", "India", "Wholesale fashion", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Wholesale handle", "wholesale", "Search hit", "B2B", "N/A", "5", "Generic."),
    ("Antique Jewellery (underscore)", "antique__jewellery_", "Unknown", "India", "Antique fashion", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Antique niche", "antique", "Search hit", "Content", "N/A", "5", "Audit duplicates."),
    ("Antique Jewellery (triple)", "antique_jewellery___", "Unknown", "India", "Antique fashion", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Antique niche", "antique", "Search hit", "SEO", "N/A", "5", "May overlap similar pages."),
    ("Antique Jewellery 7", "antiquejewellery7", "Unknown", "India", "Antique fashion", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Numeric suffix", "antique", "Search hit", "Ads", "N/A", "5", "Audit."),
    ("NJ Antique Jewellery", "njantiquejewellery", "Unknown", "India", "Antique", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Initial brand", "antique", "Search hit", "Storefront", "N/A", "5", "Audit."),
    ("Vintique Jewellery", "vintiquejewellery", "Unknown", "India", "Vintage blend", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Vintage positioning", "vintage", "Search hit", "Branding", "N/A", "5", "Audit."),
    ("Customized Jewellery India", "customizedjewellery_india", "Unknown", "India", "Custom", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Custom keyword", "custom", "Search hit", "Configurator", "N/A", "6", "Semantic ICP."),
    ("Custom Jewellery by Afshan", "customjewellerybyafshan", "Unknown", "India", "Custom maker", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Personal brand", "custom", "Search hit", "Portfolio", "N/A", "6", "Maker."),
    ("Ivy Jewellery India", "ivyjewelleryindia", "Unknown", "India", "Fashion / bridal", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Brand-sounding", "fashion", "Search hit", "Ads", "N/A", "5", "Could be mid-market."),
    ("Jewellery by DM", "jewellery_by_dm", "Unknown", "India", "Fashion", "N/A", "N/A", "DM (handle signal)", "Unknown", "N/A", "Unknown", "Unknown", "Handle encodes channel", "DM", "Search hit", "Automation", "N/A", "7", "Name is a lead signal."),
    ("Jewellery by Nistha", "jewellery_by_nistha", "Unknown", "India", "Fashion", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Personal brand", "handmade", "Search hit", "CRM", "N/A", "6", "Audit."),
    ("Jewellery Discovery", "jewellerydiscovery", "Unknown", "India", "Discovery / curator?", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "May be curator", "discovery", "Unclear model", "Clarify", "N/A", "4", "May not sell."),
    ("Jewellery Kolkata", "jewellery_kolkata", "Kolkata", "West Bengal", "City-tagged", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Geo handle", "Kolkata", "Search hit", "Local SEO", "N/A", "6", "City keyword."),
    ("Jewellery Kolkata Alt", "jewellery_kolkata__", "Kolkata", "West Bengal", "City-tagged", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Variant handle", "Kolkata", "Possible duplicate operator", "Merge", "N/A", "4", "Dedupe outreach."),
    ("Jewellss by Sukritiii", "jewellss_by_sukritiii", "Unknown", "India", "Fashion", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Creator-style", "fashion", "Search hit", "UGC", "N/A", "5", "Audit."),
    ("Kundan Creations", "kundancreations", "Unknown", "India", "Kundan", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Kundan niche", "kundan", "Search hit", "Catalog", "N/A", "6", "Bridal."),
    ("Kundan Jewellers", "kundan.jewellers", "Unknown", "India", "Kundan", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Generic kundan", "kundan", "Search hit", "Ads", "N/A", "5", "Crowded niche."),
    ("Kundan Jewellers Official", "kundanjewellers.official", "Unknown", "India", "Kundan", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Official suffix", "kundan", "Search hit", "Trust", "N/A", "5", "Audit size."),
    ("Kundan Jewellery Official", "kundan.jewellery.official", "Unknown", "India", "Kundan", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Official variant", "kundan", "Search hit", "CRM", "N/A", "5", "Audit."),
    ("Kundan Jewellery Shop", "kundan_jewelleryshop", "Unknown", "India", "Kundan retail", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Shop suffix", "kundan", "Search hit", "POS", "N/A", "5", "Audit."),
    ("Kundan Jwellery", "kundan.jwellery", "Unknown", "India", "Kundan alt spelling", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Spelling variant", "kundan", "Search hit", "SEO", "N/A", "5", "Typo-style handle."),
    ("Kundann Jewellery", "kundann_jewellery", "Unknown", "India", "Kundan", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Double n", "kundan", "Search hit", "Branding", "N/A", "5", "Audit duplicate."),
    ("Indian Kundan Jewelry", "indian_kundan_jewelry", "Unknown", "India", "Kundan", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "English spelling jewelry", "kundan", "Search hit", "Export pages", "N/A", "5", "Audit."),
    ("Rajasthani Jewellery", "_rajasthani_jewellery_", "Rajasthan", "Rajasthan", "Regional", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Regional niche", "rajasthani", "Search hit", "Geo ads", "N/A", "6", "Regional."),
    ("Rajasthani Jewellery 1", "rajasthani_jewellery1", "Rajasthan", "Rajasthan", "Regional", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Numeric suffix", "rajasthani", "Search hit", "Consolidation", "N/A", "4", "Possible network."),
    ("Rajasthani Jewellery Gold", "rajasthani_jewellery_gold", "Rajasthan", "Rajasthan", "Gold-look regional", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Gold keyword", "rajasthani", "Search hit", "Landing", "N/A", "5", "Audit."),
    ("Rajasthani Jewellery VAC", "rajasthani.jewellery__vac", "Rajasthan", "Rajasthan", "Regional", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "VAC suffix", "rajasthani", "Search hit", "Clarify brand", "N/A", "4", "Unknown suffix meaning."),
    ("Rajasthani Silver Jewellery", "rajasthani.silver.jewellery", "Rajasthan", "Rajasthan", "Silver regional", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Silver + region", "silver", "Search hit", "WooCommerce", "N/A", "6", "Silver stack."),
    ("Rajsthani Jewellery", "_rajsthani_jewellery", "Rajasthan", "Rajasthan", "Alternate spelling", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Spelling variant", "rajasthani", "Search hit", "SEO", "N/A", "4", "Spelling."),
    ("Rathi Temple Jewels", "rathi_templejewels", "Unknown", "India", "Temple", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Surname brand", "temple", "Search hit", "Lookbook", "N/A", "6", "Temple."),
    ("RNM by Rashika", "rnmbyrashika", "Unknown", "India", "Designer", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Personal brand", "designer", "Search hit", "Influencer tools", "N/A", "5", "Creator?"),
    ("Silver Rajasthani Jewellery", "silver_rajasthani_jewellery", "Rajasthan", "Rajasthan", "Silver regional", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Silver + region", "silver", "Search hit", "Store", "N/A", "6", "Silver."),
    ("Telangana Gems", "telangana.gems", "Hyderabad", "Telangana", "Gems / jewellery", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "State keyword", "gems", "Search hit", "Cert lab", "N/A", "5", "Clarify products."),
    ("Temple Jewellery (underscore)", "temple__jewellery_", "Tamil Nadu", "Tamil Nadu", "Temple style", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Temple niche", "temple", "Search hit", "Lookbook", "N/A", "6", "Temple."),
    ("Temple Jewellery Collection", "temple_jewellerycollection", "Unknown", "India", "Temple sets", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Collection keyword", "temple", "Search hit", "PIM", "N/A", "5", "Generic."),
    ("Temple Jewellery Hub by Priya", "templejewelleryhub_bypriya", "Unknown", "India", "Temple hub", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Operator name", "temple", "Search hit", "Ops", "N/A", "6", "SMB operator."),
    ("GC Temple Jewellery", "gc_temple_jewellery", "Unknown", "India", "Temple", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Initial brand", "temple", "Search hit", "Inventory", "N/A", "5", "Audit."),
    ("DM Jwellry", "dm_jwellry", "Unknown", "India", "Fashion", "N/A", "N/A", "DM", "Unknown", "N/A", "Unknown", "Unknown", "Handle signal", "DM", "Search hit", "Automation", "N/A", "7", "ICP name."),
    ("The Bead Story", "_thebeadstory", "Unknown", "India", "Beaded jewellery", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Beads niche", "beads", "Search hit", "DTC", "N/A", "6", "Maker potential."),
    ("The Roohsutra", "theroohsutra", "Unknown", "India", "Fusion designer", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Brand name", "fusion", "Search hit", "Brand", "N/A", "5", "Audit positioning."),
    ("Rajputii Jewellery", "rajputii_jewellery_", "Rajasthan", "Rajasthan", "Rajputi fashion", "N/A", "N/A", "DM / comments", "Unknown", "N/A", "Unknown", "Unknown", "High comment threads", "rajputi", "Engagement", "Community", "N/A", "7", "Cultural niche."),
    ("Rajputi Jewellery Wholesaler SC", "rajputi_jewelery_wholsaler_s.c", "North India", "India", "Rajputi wholesale", "+917877634674", "N/A", "WhatsApp + group", "No", "N/A", "Unknown", "Unknown", "Join group language", "rajputi wholesale", "Indexed reel", "Group commerce", "N/A", "8", "Explicit WhatsApp."),
    ("The Madras Art Studio", "themadras_artstudio", "Chennai", "Tamil Nadu", "Resin jewellery", "N/A", "N/A", "DM to order", "No", "N/A", "Unknown", "Unknown", "Public post: DM to order", "resin, DM", "HTML parent resolution", "Custom checkout", "N/A", "8", "Fetched."),
    ("Vivah Bridal Collections", "vivahbridalcollections", "Nellore", "Andhra Pradesh", "Bridal rent/sale", "+917092536536", "N/A", "WhatsApp bookings", "Unknown", "Book online mentioned", "Unknown", "Unknown", "Bridal bookings caption", "bridal rent", "HTML parent resolution", "Booking CRM", "N/A", "7", "Fetched."),
    ("Jewellery Rajasthan", "jewellery_rajasthan", "Rajasthan", "Rajasthan", "Rajputi wedding", "N/A", "N/A", "DM / reels", "Unknown", "N/A", "Unknown", "Unknown", "Reel brand page", "rajputi wedding", "HTML parent resolution", "Studio", "N/A", "7", "Fetched."),
    ("NR Silver Jewels", "nr_silver_jewels", "Unknown", "India", "Silver", "N/A", "N/A", "Unknown", "Unknown", "N/A", "Unknown", "Unknown", "Search-surfaced reel", "silver", "Low public text", "Verify WA", "N/A", "5", "Sparse."),
    ("Pooja Jewels", "poojajewels_", "Unknown", "India", "Silver payal / fashion silver", "+917597344552", "N/A", "WhatsApp; COD", "No", "N/A", "Unknown", "Unknown", "Small business hashtags in reel index", "silver, COD", "HTML parent + search snippet", "WhatsApp automation", "N/A", "9", "Fetched from reel HTML."),
    ("Aarti Jewellers Surat", "aartijewellers.surat", "Surat", "Gujarat", "Gold retail showroom", "N/A", "N/A", "Store visits", "Unknown", "N/A", "Unknown", "Unknown", "Store promotions", "gold, Surat", "Physical jeweller IG", "Local ads", "N/A", "5", "More showroom-led."),
    ("Vajubhai & Sons", "vajubhai_and_sons", "Surat", "Gujarat", "Gold manufacturing", "N/A", "N/A", "B2B / heritage brand", "Unknown", "N/A", "Unknown", "Unknown", "Since 1965 mention", "gold manufacturing", "Heritage manufacturer", "B2B portal", "N/A", "4", "Larger manufacturer — lower ICP fit."),
    ("S Swarnakar And Son", "s.swarnakarandson", "Kolkata", "West Bengal", "Gold / silver traditional", "+918981948452", "N/A", "Call booking", "Unknown", "N/A", "Unknown", "Unknown", "Chetla / Kolkata tags in posts", "gold, silver, Kolkata", "Indexed post phone", "Omnichannel", "N/A", "6", "Physical store emphasis."),
]

handles = [row[1] for row in RAW]
assert len(handles) == len(set(handles)), f"Duplicate handles: {[h for h in handles if handles.count(h)>1]}"

# If fewer than 100, fail loudly (do not invent)
if len(RAW) != 100:
    raise SystemExit(f"Expected 100 leads, got {len(RAW)}. Update RAW list.")

OUT = Path("/workspace/india_jewellery_instagram_leads.txt")
parts: list[str] = []
parts.append(
    textwrap.dedent(
        """
        ================================================================================
        INDIA JEWELLERY — INSTAGRAM / WHATSAPP LEADS (PUBLIC WEB HARVEST)
        ================================================================================
        Generated: 2026-05-24
        Unique Instagram handles: 100

        METHODOLOGY:
        - Handles and phone numbers were taken from publicly indexed search snippets,
          Instagram post/reel pages (unauthenticated HTML), and one DuckDuckGo-lite
          batch crawl of site:instagram.com queries.
        - This is not a substitute for logged-in Instagram verification.

        BEFORE OUTREACH:
        - Confirm posting recency, duplicate operators, and whether a Shopify/Woo
          store exists beyond Instagram.
        - Normalize WhatsApp numbers to E.164 (+91) after confirming on profile.

        ================================================================================
        """
    ).strip()
)

for i, row in enumerate(RAW, start=1):
    (
        biz,
        handle,
        city,
        state,
        btype,
        wa,
        email,
        ordering,
        web_yes,
        web_url,
        recent,
        engage,
        bio,
        kw,
        reason,
        svc,
        maps,
        score,
        notes,
    ) = row
    block = f"""
{'=' * 50}
LEAD #{i}
{'=' * 50}
Business Name: {biz}
Instagram Handle: @{handle}
Instagram URL: https://www.instagram.com/{handle}/
Followers Count: Unknown (not in indexed sources)
City: {city}
State: {state}
Business Type: {btype}
WhatsApp Number: {wa}
Email: {email}
Ordering Method: {ordering}
Website Present: {web_yes}
Website URL: {web_url}
Recent Activity Date: {recent}
Average Engagement: {engage}
Bio Text: {bio}
Keywords: {kw}
Reason Qualified: {reason}
Potential Services Needed: {svc}
Google Maps Link: {maps}
Lead Quality Score: {score}/10
Notes: {notes}
""".strip()
    parts.append(block)

OUT.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
print(f"OK: wrote {OUT} ({len(RAW)} leads)")
