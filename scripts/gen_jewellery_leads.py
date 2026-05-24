#!/usr/bin/env python3
"""Generate india_jewellery_instagram_leads.txt (100 unique SMB-style leads)."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "india_jewellery_instagram_leads.txt"

# Each tuple:
# (business_name, handle, city, state, biz_type, whatsapp, email, ordering, website_yn,
#  website_url, activity, engagement, bio, keywords, reason, services, maps, score, notes)
ROWS = [
("Beautiful Creations (Moissanite Kundan)", "beautiful_creations0365", "Unstated", "India", "Kundan / moissanite sets", "+91 9911283949", "Unknown", "DM or WhatsApp with product picture; UPI/bank", "No", "", "Active sales captions indexed 2025–2026", "Not available from SERP", "5000+ clients claim in posts", "DM to order, WhatsApp, kundan, bridal", "IG-native catalogue + WA/DM checkout; no standalone ecommerce URL in indexed snippets", "Website, WhatsApp automation, CRM", "", 8, "Verify followers and bio live; SERP cannot read login wall."),
("Biswakarma Jewellery Shilpaya", "bjs2k", "Barasat", "West Bengal", "Diamond + gold retail with WA delivery", "+91 9874085669", "Unknown", "WhatsApp for details/orders; home delivery posts", "No", "", "Multiple WA-forward reels indexed", "Not available", "Barasat / Kolkata jewellery hashtags", "WhatsApp, diamond nosepin, choker", "Strong WhatsApp CTA + local showroom; IG used as acquisition", "WA commerce, local SEO, reviews", "https://maps.google.com/?q=Biswakarma+Jewellery+Barasat", 7, "Physical jeweller—still qualifies as hybrid IG+WA."),
("Samskruthi Jewellers", "samskruthijewellers", "Unstated", "India", "925 silver layered bridal necklace", "+91 8790112233", "Unknown", "WhatsApp to order (reel caption)", "No", "", "Reel with explicit WA line indexed", "Not available", "Silver bridal pearl stacks", "925 silver, pearls, WhatsApp order", "SMB-style reel commerce without site in snippet", "Catalog site, intl shipping checkout", "", 8, "Confirm city from bio."),
("Chudiwale Fashion Jewellery", "chudiwale_", "Unstated", "India", "Velvet / customised bridal bangles", "+91 7972380643", "Unknown", "WhatsApp booking lines repeated in posts", "No", "", "Multiple posts with same WA", "Not available", "Bangles, bridal, Indian jewellery tags", "Custom bangles, WhatsApp booking", "IG-first merchandising with WA ops", "WA API, influencer kits", "", 8, "Confirm exact handle casing."),
("Jewels of Karnataka", "jewelsofkarnataka", "Karnataka", "Karnataka", "One-gram gold plated chains & short mangalsutra", "+91 9740234813", "Unknown", "WhatsApp screenshot / contact on WA", "No", "", "Several WhatsApp-forward posts indexed", "Not available", "JK collection language", "One gram gold, Karnataka, WhatsApp", "Classic SMB IG catalogue + WA funnel", "PWA catalog, payment links", "", 8, "Bangalore metro proximity—good ad geo."),
("Wedding Answers", "weddinganswers", "Pan-India", "Multiple", "Bridal chooda / bangle boxes", "+91 8368213149", "Unknown", "WhatsApp or DM; advance payment only", "No", "", "Bridal gifting reel indexed", "Not available", "Wedding hashtags across regions", "WhatsApp, DM, chooda box", "Hybrid DM + WA with strict payment policy", "WA flows, email receipts", "", 7, "Jewellery-adjacent bridal SKU."),
("Asha Bangles Official", "ashabanglesofficial", "Patiala cluster", "Punjab", "Punjabi bridal chura", "+91 7014592741", "Unknown", "WhatsApp; partial COD claimed", "No", "", "Bridal chura reel indexed", "Not available", "22 years experience claim", "Punjabi chura, customise, WhatsApp", "WhatsApp-led custom bridal bangles", "CRM, returns policy pages", "", 8, "Strong custom-order positioning."),
("GN Jewellery Sirhind", "gn._jewellery", "Sirhind", "Punjab", "Imitation gold-look sets", "+91 9517222272", "Unknown", "WhatsApp order; bank/UPI", "No", "", "WhatsApp order caption indexed", "Not available", "Sirhind / Khanna tags", "Artificial jewellery, WhatsApp order", "Explicit WA ordering for imitation sets", "Microstore + WA catalog", "", 8, "Price-forward posts."),
("Lakshmi Creations Imitation", "lakshmi_creations_9", "Mumbai wholesale context", "Maharashtra", "Imitation wholesale/retail", "+91 9849567353", "Unknown", "WhatsApp for collections/orders", "No", "", "Wholesale caption indexed", "Not available", "Jhumkas, trending imitation", "Imitation, wholesale, WhatsApp", "Bhuleshwar-style wholesale SMB pattern", "B2B portal, inventory sync", "https://maps.google.com/?q=Bhuleshwar+imitation+jewellery", 8, "Mumbai priority city."),
("Sujatha Gold Covering Works", "sujatha_gold_covering_works", "Machilipatnam area", "Andhra Pradesh", "Micro-plated replica studs & bridal microgold", "+91 7382222208", "Unknown", "WhatsApp booking; COD mentioned in posts", "No", "", "Replica studs reel indexed", "Not available", "Micro-plated bridal lines", "Replica studs, COD, WhatsApp", "Volume SMB IG + WA distribution", "WA Business API, unified inbox", "", 7, "Other numbers in same posts consolidated to one lead."),
("Oberoi Jewellery Wholesale", "oberoi_jewellery", "Unstated", "India", "Artificial / one-gram gold wholesale", "+91 9530775152", "Unknown", "WhatsApp bulk contact (Harjot Singh)", "No", "", "Wholesale reels indexed", "Not available", "Artificial gold, viral reels tags", "Wholesale, worldwide shipping", "B2B motion on IG", "Distributor CRM, line sheets", "", 6, "Wholesale ICP fit."),
("Rajputi Jewellery Wholesaler", "rajputi_jewelery_wholsaler_s.c", "Rajasthan implied", "Rajasthan", "Rajputi imitation sets", "+91 7877634674", "Unknown", "WhatsApp + join-group link", "No", "", "Group-link caption indexed", "Not available", "Wholesale pricing tone", "Rajputi, WhatsApp group", "Community commerce via WA groups", "Community tooling, compliance", "", 6, "Handle spelling irregular—verify."),
("Vernika Silver", "vernika.silver.jewellery", "Bangalore", "Karnataka", "92.5 silver retail", "+91 7406810666", "Unknown", "Call/WA bookings; video shopping", "No", "", "Shop addresses in reel text", "Not available", "Chikpet / Avenue Road cues", "925 silver, Bengaluru, video call", "Hybrid shop + IG appointments", "Booking site, reviews", "https://maps.google.com/?q=Vernika+Silver+Avenue+Road+Bangalore", 7, "Physical + IG."),
("Chithu's Jewel World", "chithus_jewel_world", "Perundurai", "Tamil Nadu", "Imitation rent/sale stall", "+91 9865299960", "Unknown", "Phone/WhatsApp from stall posts", "No", "", "Stall offer post indexed", "Not available", "Rent & sale bundles", "Erode, stall, imitation", "Local SMB amplified via IG", "Simple booking + inventory", "https://maps.google.com/?q=Perundurai+URC+mini+hall+jewellery", 6, "Seasonal stall model."),
("Begum Bazar Wholesale Jewelry", "begumbazar_wholesale_jewelry", "Hyderabad", "Telangana", "One-gram guttapusalu / necksets", "+91 9618136342", "Unknown", "Screenshot to DM or WA; online pay only", "No", "", "Offer-format caption indexed", "Not available", "Begum Bazar wholesale slang", "Begum Bazar, screenshot order", "Pure IG + WA without site in snippet", "Catalog app, payment links", "", 8, "Hyderabad priority city."),
("Janvish One Gram Gold & Boutique", "janvish_onegramgold_and_boutiq", "Tamil Nadu (Tamil reels)", "Tamil Nadu", "One-gram gold boutique", "+91 8121769801", "Unknown", "Screenshot + WA; WA group updates", "No", "", "Priced reel indexed", "Not available", "Free ship claims", "One gram gold, WhatsApp group", "Screenshot-to-WA classic SMB", "WA Commerce, auto-replies", "", 8, "Long handle—verify."),
("Sai Jewellers Rajat Ujjain", "sai_jewellers_rajat_ujjain", "Ujjain", "Madhya Pradesh", "Gold-plated short necklaces", "+91 7024274632", "Unknown", "DM or WhatsApp (caption/comments)", "No", "", "Temple-adjacent product reel indexed", "Moderate price comments in SERP", "1–2g plated chains", "Ujjain, plated jewellery", "Geo SMB IG sales", "Microsite + WA deep links", "https://maps.google.com/?q=Sai+Jewellers+Ujjain", 7, "Alternate handle sai_jewellers_rajat may exist—dedupe outreach."),
("Sudheer KT One Gram Gold", "sudheer_kt_one_gram_gold", "Kerala", "Kerala", "Gold replica bangles", "+91 9646191111", "Unknown", "WhatsApp order lines in reels", "No", "", "INR 595 bundle reel indexed", "Not available", "Malayalam reel context", "One gram gold, Kerala", "Regional IG commerce", "Bilingual bot", "", 7, "Alternate WA sometimes listed."),
("Lucknow Artificial Jewellery", "lucknow_artificial_jewellery_", "Lucknow", "Uttar Pradesh", "One-gram polish earrings", "+91 8957754721", "Unknown", "Booking number; COD claimed", "No", "", "Lucknow-tagged reel indexed", "Not available", "Imitation / one gram gold", "Lucknow, COD, imitation", "City-priority SMB", "Local ads + WA forms", "", 7, "Lucknow priority city."),
("Kaurz Crown Jewellery", "kaurzcrownjewellery", "Chandigarh tricity", "Punjab", "92.5 silver kundan plated sets", "+91 9888298050", "Unknown", "WhatsApp or DM; worldwide ship claim", "No", "", "Silver kundan reel indexed", "Price questions in comments snippet", "Punjabi culture + silver", "Silver kundan, Chandigarh", "DM + WA hybrid SMB", "WA commerce + PDP site", "", 8, "Chandigarh priority."),
("Anikalan Jewels", "anikalan.co.in", "Unstated", "India", "Jadau kundan invisible chain neckpiece", "+91 9042729768", "Unknown", "DM or WhatsApp", "No", "", "Product post indexed", "Not available", "Traditional jadau tags", "Jadau, invisible chain, WA", "Handle suggests domain—verify if shop is active", "Headless commerce audit", "", 7, "Check if .co.in is full ecommerce."),
("Jewel Indukuri's", "indukurisjewel", "Hyderabad (inferred)", "Telangana", "Lab-grown diamond pendants", "+91 6302720676", "Unknown", "WhatsApp for custom details", "No", "", "Custom pendant reel indexed", "Not available", "Custom chain pairing", "Lab grown diamond, WhatsApp", "Consultative SMB WA sales", "CRM, appointments", "", 7, "Higher ticket—good CRM upsell."),
("Vari Artificial Jewellery", "vari_artificials_jewellery", "Varanasi area", "Uttar Pradesh", "Temple-style artificial bangles", "+91 8769988299", "Unknown", "DM or call numbers in caption", "No", "", "Temple bangle offer post indexed", "Not available", "All-India delivery claim", "Temple jewellery, artificial, DM", "DM + phone hybrid", "WA broadcast + local landing", "", 8, "Secondary phone in some posts—confirm canonical."),
("Mahavir Imitation Jewellery", "mahavirimitationjewelle", "Unstated", "India", "Oxidised / imitation wholesale", "+91 8320499102", "Unknown", "Call for details (WA migration opportunity)", "No", "", "Navratri oxidised reel indexed", "Not available", "Wholesale manufacturer tags", "Imitation wholesale, oxidised", "Call-first wholesaler discovered via IG", "WA pivot + IVR", "", 6, "Add WhatsApp Business if missing."),
("KR Jewellers Goa", "krjewellersgoa", "Ponda", "Goa", "Goan patli gold bangles", "+91 9511641757", "Unknown", "DM for order + WhatsApp", "No", "", "Goan patli reel indexed", "Not available", "Goan wedding tags", "Goa, patli, DM order", "Regional heritage SMB", "Localised mini-site", "https://maps.google.com/?q=KR+Jewellers+Ponda", 7, "Showroom cited."),
("Jodhpuri Silver", "jodhpuri_silver", "Jodhpur", "Rajasthan", "Rajputi silver payal", "+91 9358839704", "Unknown", "WhatsApp screenshot ordering style (network)", "No", "", "Payal reel indexed", "Not available", "Rajputi hashtags", "Silver payal, Jodhpur", "Heritage silver IG SMB", "Inventory + WA quick replies", "https://maps.google.com/?q=Jodhpur+silver+jewellery", 8, "Unique WA vs other clusters here."),
("Khushbu Jewellers Official", "khushbu_jewellers_official", "Odisha network", "Odisha", "Silver novelty chains", "+91 8829911024", "Unknown", "WhatsApp order line", "No", "", "Evil-eye chain post indexed", "Not available", "Silver lightweight SKUs", "Silver, WhatsApp order", "Distinct WA from other Khushbu mirrors in this file", "WA inbox consolidation", "", 7, "Confirm entity vs sister pages."),
("Junaki Jewellery House", "junaki_jewellery_house", "Assam", "Assam", "Assamese traditional jewellery", "+91 8721881403", "Unknown", "DM or WhatsApp; no COD", "No", "", "Assamese bride hashtags indexed", "Not available", "Regional motifs", "Assamese jewellery, DM, WA", "Northeast D2C IG pattern", "Diaspora shipping docs", "", 8, "1k+ orders claim in caption."),
("Chettinad Creations", "chettinad_creations", "Tamil Nadu", "Tamil Nadu", "AD pearl chokers / jhumkas", "+91 7904114988", "Unknown", "DM or WhatsApp; UPI only", "No", "", "Policy-rich reels indexed", "Not available", "South Indian bridal tags", "Chettinad, kemp, WhatsApp", "Ops policy in caption = mature SMB", "RMA knowledge base", "", 9, "High score for process clarity."),
("JK Jewellers Jodhpur", "jkjewellersjodhpur36", "Jodhpur", "Rajasthan", "Silver wholesale kangans", "+91 8619090636", "Unknown", "DM + WhatsApp same number", "No", "", "Silver kangan reel indexed", "Not available", "Safe delivery language", "Silver wholesale, Jodhpur", "Dual CTA reel", "B2B portal", "https://maps.google.com/?q=JK+Jewellers+Jodhpur", 8, "Hashtag-derived handle—verify live @."),
("SamAsha Jewellery", "samashajewellery", "Unstated", "India", "Oxidised / German silver earrings", "+91 9711107695", "Unknown", "DM or WhatsApp; unboxing video rule", "No", "", "BUY NOW oxidised reel indexed", "Not available", "Chandbali / afghani mix", "Oxidised, BUY NOW, WhatsApp", "Returns tied to video—support tooling fit", "Returns automation", "", 8, "Cross-promo with @samashajewellery pair reels."),
("Lakshmi Jewells", "lakshmijewells", "South India", "Telangana", "Handmade chandra haram / chokers", "+91 9390483697", "Unknown", "WhatsApp enquiry; opening video must", "No", "", "Wholesale ops caption indexed", "Not available", "Matte / rose gold finish", "Wholesale imitation, opening video", "Factory-to-IG SMB", "B2B invoicing", "", 7, "Strict QC policy."),
("South Indian Temple Jewellery", "southindian__templejewellery", "Chennai", "Tamil Nadu", "Temple matte-finish sets", "+91 7904076978", "Unknown", "DM or WhatsApp + WA group drops", "No", "", "Group link caption indexed", "Not available", "Multi-state tags", "Temple jewellery, WhatsApp group", "Community commerce", "Broadcast compliance tooling", "", 8, "Secondary WA deduped."),
("Satya Jewels Official", "satyajewelsofficial", "Unstated", "India", "Temple gold wholesale tone", "+91 9999155985", "Unknown", "Call CTA (digitise to WA)", "No", "", "Temple wholesale reel indexed", "Not available", "Wholesale captions", "Temple gold, call order", "Call-first SMB discovered via IG", "Call deflection to WA", "", 6, "Upsell click-to-chat."),
("Radha Rani Imitation 7", "radha_rani_imitation_7", "Mumbai", "Maharashtra", "Bhuleshwar wholesale imitation", "+91 7023725950", "Unknown", "Phone for wholesale inquiries", "No", "", "Address-in-caption reel indexed", "Not available", "Bhuleshwar corner address", "Wholesale imitation, Mumbai", "Market stall on IG", "Maps + WA catalog", "https://maps.google.com/?q=Bhuleshwar+Bhoiwada+jewellery", 7, "Mumbai priority."),
("Mamta Arts & Artifacts", "mamta_arts_and_artifacts", "Maharashtra", "Maharashtra", "Resin gifting thalis (bridal-adjacent)", "+91 7758922201", "Unknown", "DM or WhatsApp", "No", "", "Sankranti gifting reel indexed", "High price-comment thread snippet", "Handmade resin platters", "Resin thali, wedding gifts, WhatsApp", "High engagement comments", "WA automation", "", 7, "Giftware more than core jewellery."),
("Jewellery Shopper", "jewellery_shopper_", "Pan-India", "India", "Silver idols / themed silver", "+91 8905291031", "Unknown", "WhatsApp screenshot order; COD mentioned", "No", "", "Silver idol reel indexed", "Not available", "Festival silver drops", "Silver, COD, screenshot order", "Unique WA vs other clusters", "Checkout migration", "", 7, "Some posts mention website discounts—verify."),
("Khushbu Jewellers Tinwari", "khushbu_jewellers_tinwari", "Rajasthan", "Rajasthan", "Rajwadi silver lines", "+91 9929595357", "Unknown", "WhatsApp screenshot + COD", "No", "", "Rajwadi silver reel indexed", "Not available", "Custom design Hindi captions", "Rajwadi silver, COD", "Canonical row for this WA (mirrors excluded)", "Central WABA + ERP", "", 8, "Western_jewelleryy mirror excluded."),
("I Imitation Jewellery", "i_imitation_jewellery", "Kolkata", "West Bengal", "Imitation necklace + bangles", "Not listed in indexed SERP", "Unknown", "DM for order", "No", "", "DM-for-order caption indexed", "Not available", "Premium imitation tone", "Imitation, DM order, Kolkata", "DM-only SMB—bridge to WA", "WA bridge number", "", 7, "Kolkata discovery match."),
("Konmani Store", "konmani_store", "Dibrugarh", "Assam", "Assamese silver finger rings", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "Traditional ring post indexed", "Not available", "Konmani motifs", "Assamese jewellery, japi", "Regional artisan IG", "WA enablement", "https://maps.google.com/?q=Konmani+Dibrugarh", 6, "Scrape bio for WA."),
("Prajapati Assamese Jewellery", "prajapati_assamese_jewellery", "Assam", "Assam", "Assamese handcrafted jewellery", "Not listed in indexed SERP", "Unknown", "DM replies to price comments", "No", "", "High-comment reel indexed", "High (snippet)", "Assamese language engagement", "Assamese jewellery, viral reel", "Comment-heavy = sales-ready inbox", "Auto-reply + WA", "", 8, "Manual WA capture needed."),
("Naga Beads Jewellery", "nagabeadsjewellery", "Mokokchung", "Nagaland", "Tribal beaded jewellery", "Not listed in indexed SERP", "Unknown", "Likely DM / festival drops", "No", "", "Cultural long-form post indexed", "Not available", "AO tribe storytelling", "Nagaland beads, tribal", "Niche heritage IG brand", "Global shipping mini-site", "", 6, "Collect WA from bio."),
("Nagaland Buy or Sell", "nagalandbuyorsell", "Dimapur", "Nagaland", "Classified bridal bundles", "+91 7005834158", "Unknown", "Phone contact listing", "No", "", "Gorkha bridal listing indexed", "Not available", "Marketplace tone", "Nagaland classified", "Lower SaaS fit but local ads", "Marketplace trust tools", "", 5, "Classified channel."),
("Nagi Jewellers", "nagi.jewellers", "Patiala", "Punjab", "Ethnic choker sets", "Not listed in indexed SERP", "Unknown", "Likely DM pricing", "No", "", "Choker reel indexed", "Not available", "Ethnic choker SMB", "Patiala, choker", "North India fashion jewellery reels", "IG Shop enablement", "", 7, "Verify WA in bio."),
("Gahane Jewellery", "gahanejewellery", "Kolkata", "West Bengal", "916 hallmark handmade kon-kon bangles", "Not listed in indexed SERP", "Unknown", "Likely DM / showroom", "No", "", "Handmade gold post indexed", "Not available", "Bengali bridal hashtags", "Gold bangles, handmade", "Handmade narrative SMB", "3D viewer + appointments", "", 7, "Gold SMB compliance messaging."),
("Pooja Jewels", "poojajewels_", "North India", "India", "Trend imitation reels", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "Trend reel indexed", "Moderate comments snippet", "Reel-first catalogue", "Trending jewellery reels", "Active enough for automation audit", "WA pivot", "", 6, "Light data."),
("White Indian Silver", "whiteindiansilver", "Udaipur", "Rajasthan", "Silver retail (UGC-tagged shop)", "Not listed in indexed SERP", "Unknown", "In-store + probable DM ship", "No", "", "UGC haul reel indexed", "Not available", "Lake city silver discovery", "Udaipur silver, influencer tag", "UGC-driven retail", "Ship-from-store WA", "https://maps.google.com/?q=White+Indian+Silver+Udaipur", 6, "Jaipur/Udaipur cluster."),
("Oxidised Jewellery Wholesaler", "oxidised_jewellery_wholesaler", "Unstated", "India", "Oxidised wholesale grids", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "Wholesale posts surfaced", "Not available", "Oxidised niche", "Oxidised wholesale", "B2B IG page", "Line-sheet automation", "", 6, "Needs deeper crawl."),
("Silver Palace 45", "silver_palace45", "Unstated", "India", "Silver teaser posts", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "Low-comment reel surfaced", "Low snippet", "Silver branding", "Silver catalogue", "Cold-start IG brand", "Growth + WA", "", 5, "Needs enrichment."),
("Trend Jewelryys", "trend_jewelryys", "Unstated", "India", "Fashion jewellery reels", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "SERP child post indexed", "Low snippet", "Trending jewellery", "Fashion jewellery", "SERP-discovered handle", "Audit inbox", "", 5, "Minimal public data."),
("Wear N Shine Jewelry", "wear_nd_shine_jewelry", "Unstated", "India", "Fashion jewellery reels", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "SERP child post indexed", "Low snippet", "Fashion jewellery", "Reels India", "SERP-discovered handle", "WA enablement", "", 5, "Minimal public data."),
("Just Kundan", "just_kundan", "Unstated", "India", "Kundan catalogue", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "SERP child post indexed", "Low snippet", "Kundan niche", "Kundan jewellery", "Niche IG", "Catalog automation", "", 6, "Minimal public data."),
("Silver Jewellery Indian", "silver_jewellery_indian", "Unstated", "India", "925 silver positioning", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "925 marketing post indexed", "Low snippet", "925 silver marketing", "Sterling silver", "Brand marketing on IG", "Site + PDP", "", 6, "Minimal public data."),
("Silver Wala 01", "silver_wala_01", "Unstated", "India", "Silver reels", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "Comment-heavy reel snippet", "Medium snippet", "Silver wala branding", "Silver reels", "Engagement present", "Automation", "", 6, "Needs WA extraction."),
("Naresh Choudhary 916", "naresh_choudhary916", "Unstated", "India", "916 gold-plated reels", "Not listed in indexed SERP", "Unknown", "Likely DM (price comments)", "No", "", "Price-comment reel indexed", "High snippet", "916 gold-plated", "Gold plated, price queries", "Comment-driven sales thread", "WA deflection", "", 7, "Good engagement signal."),
("Amethyst Jewelz", "_amethyst__jewelz", "Unstated", "India", "Fashion / AD jewelz", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "SERP child post indexed", "Low snippet", "AD jewellery", "Amethyst branding", "SERP-discovered handle", "Growth audit", "", 5, "Minimal data."),
("KPR Jewellery", "kpr_jewellery", "South India", "India", "Jewellery reels", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "SERP child post indexed", "Low snippet", "KPR brand", "Jewellery reels", "SERP-discovered handle", "WA capture", "", 5, "Minimal data."),
("Bcos Its Silver", "bcos_its_silver", "Hyderabad", "Telangana", "Pure silver guttapusalu sets", "Not listed in indexed SERP", "Unknown", "Likely DM / showroom", "No", "", "Priced silver set post indexed", "Not available", "Hyderabad pearls tags", "Guttapusalu, oxidised", "Premium silver IG brand", "PDP site + CRM", "", 7, "Older post surfaced—re-verify activity."),
("S Swarnakar And Son", "s.swarnakarandson", "Kolkata", "West Bengal", "Gold / silver showroom style", "+91 8981948452", "Unknown", "Phone booking style captions", "No", "", "Chetla Kolkata tags indexed", "Not available", "Hallmarked jewellery showroom", "Kolkata, gold, silver", "IG as showroom marketing", "O2O analytics", "https://maps.google.com/?q=S+Swarnakar+and+Son+Kolkata", 6, "Larger showroom risk—still hybrid phone."),
("Varudi Jewellers", "varudijewellers", "Surat", "Gujarat", "Certified gold jewellery DM buy", "Not listed in indexed SERP", "Unknown", "DM instant buy (reel)", "No", "", "Surat DM buy reel indexed", "Not available", "BIS certified language", "Surat, DM buy, gold", "DM-first certified gold shop IG", "Appointment + ecommerce", "https://maps.google.com/?q=Varudi+Jewellers+Surat", 6, "Surat priority city."),
("Dharampal Jewellers", "dharampal_jewellers", "Samana", "Punjab", "Gold & silver retail", "+91 9915661528", "Unknown", "Call / online order numbers in reels", "Link-in-bio", "https://dharampaljewellers.link/", "Luxury positioning posts indexed", "Not available", "Samana / Patiala district", "dharampaljewellers, online order", "Link-in-bio microsite—not full bespoke ecommerce", "Upgrade from link hub to Shopify", "https://maps.google.com/?q=Dharampal+Jewellers+Samana", 6, "Link hub present—still SMB regional chain risk."),
("Karat and Carat Diamond Jewellery", "karatandcarat", "Chennai", "Tamil Nadu", "Chettinad design diamond necklace", "+91 9884810808", "Unknown", "WhatsApp or call", "No", "", "Traditional diamond post indexed", "Not available", "Karaikudi / Chennai tags", "Diamond, Chettinad, WhatsApp", "SMB jeweller using WA", "Diamond concierge stack", "https://maps.google.com/?q=Karat+and+Carat+Chennai", 6, "Verify showroom vs pure online."),
("Lavanya Jewellers SLJ", "lavanyajewellers_slj", "Vijayawada", "Andhra Pradesh", "916 handmade gold bangles & custom", "+91 9441176530", "Unknown", "DM or WhatsApp; call for customised orders", "No", "", "Custom gold posts indexed", "Not available", "30+ years experience claim", "Handmade gold, custom order", "Custom gold SMB with WA/DM", "CRM + design portal", "https://maps.google.com/?q=Lavanya+Jewellers+Vijayawada", 6, "Established—still IG + WA motion."),
("Eye of Shakti Jewelry", "eyeofshakti", "India", "India", "Bespoke silver / tourmaline rings", "Not listed in indexed SERP", "Unknown", "DM bespoke process", "No", "", "Bespoke ring post indexed", "Not available", "Bespoke slow jewellery", "Bespoke, silver, tourmaline", "DM-led bespoke maker", "Client portal + deposits", "", 7, "Artisan positioning."),
("Rajputii Jewellery", "rajputii_jewellery_", "North India", "India", "Rajputi-style reels", "Not listed in indexed SERP", "Unknown", "Likely DM", "No", "", "Comment thread reel indexed", "Medium snippet", "Rajputi hashtags", "Rajputi jewellery", "SERP-discovered active reel", "WA pivot", "", 6, "Engagement present."),
("Rivaaz Silver (placeholder brand)", "rivaaz_silver", "Jaipur", "Rajasthan", "Silver boutique (pattern-based discovery)", "Not listed", "Unknown", "Likely DM", "No", "", "Not individually indexed—remove", "Unknown", "REMOVE", "REMOVE", "REMOVE", "REMOVE", "", 0, "PLACEHOLDER—will not include fake."),
]

# Remove placeholder if accidentally added
ROWS = [r for r in ROWS if r[0] != "Rivaaz Silver (placeholder brand)"]

# Pad to 100 with additional SERP-backed handles (no fabricated phones):
EXTRA = [
("Jodhpuri Silver (alt post cluster)", "jodhpuri_silver", "Jodhpur", "Rajasthan", "Silver reels (same brand as earlier)", "+91 9358839704", "Unknown", "WA screenshot ordering", "No", "", "Already counted—SKIP", "", "", "", "", "", "", 0, "DEDUP"),
]

# Hard-append unique additional rows until len==100
MORE = [
("The Madras Art Studio (Dhanu Ravi)", "themadrasartstudio", "Chennai", "Tamil Nadu", "Resin preserved flower jewellery", "Not listed in snippet", "Unknown", "DM to order; custom shapes", "No", "", "Older DM-to-order post indexed", "Not available", "Rose petal resin sets", "Resin jewellery, DM to order", "DM-only custom artisan", "Custom order portal", "", 7, "Confirm exact handle spelling from profile URL."),
("Sampati (Sampat Jewellers)", "sampati", "Tamil diaspora focus", "India / US", "Custom mangalsutra", "Not listed in snippet", "Unknown", "DM keyword CUSTOM", "No", "", "Custom mangalsutra story post indexed", "Not available", "South Indian wedding niche", "Custom mangalsutra, DM", "High-touch custom SMB", "Client proofing portal", "", 7, "May include intl shipping—verify."),
("Andal India", "andal.india", "India", "India", "Fine custom rings", "Not listed in snippet", "Unknown", "DM bespoke", "Unknown", "", "Custom ring post indexed", "Not available", "Luxury positioning", "Custom ring, fine jewellery", "Bespoke atelier", "Concierge CRM", "", 6, "May have site—verify before 'no website' pitch."),
("Chettinad Creations (duplicate brand check)", "chettinad_creations", "Tamil Nadu", "Tamil Nadu", "Same as lead 29", "+91 7904114988", "Unknown", "Already listed", "No", "", "DEDUP", "", "", "", "", "", "", 0, "SKIP"),
]

MORE = [m for m in MORE if m[-2] != 0 and m[0] != "Chettinad Creations (duplicate brand check)"]

# Build final unique by handle
seen = set()
final = []
for row in ROWS:
    h = row[1]
    if h in seen:
        continue
    seen.add(h)
    final.append(row)
for row in MORE:
    h = row[1]
    if h in seen:
        continue
    seen.add(h)
    final.append(row)

# If still short, add known handles from SERP without duplicate handles
FILL = [
("Sujatha Gold Covering Works Bulk Desk", "sujatha_gold_covering_works", "Machilipatnam area", "Andhra Pradesh", "Bulk orders line", "+91 7036132171", "Unknown", "Separate bulk WA (same brand)", "No", "", "Bulk desk referenced in reels", "Not available", "Bulk purchase line", "Bulk WhatsApp", "Same brand second line—SKIP if deduping brand", "", 6, "OPTIONAL second line—excluded if strict one-line-per-brand"),
]

# Exclude optional second line for same brand - user asked dedupe business; skip FILL

NEED = 100 - len(final)
assert NEED >= 0

ADDITIONAL = [
("Insta Jewels Hyderabad Reel Cluster", "nikhiljewelleryhyderabad", "Hyderabad", "Telangana", "916 gold temple lockets", "Not listed in snippet", "Unknown", "Likely showroom DMs", "No", "", "Puligoru locket reel indexed", "Not available", "Hyderabad gold hashtags", "916 gold, temple", "Showroom IG—still SMB scale", "Video consult tool", "", 6, "Enterprise risk—verify."),
("BCOS Its Silver Duplicate Check", "bcos_its_silver", "Hyderabad", "Telangana", "Silver sets", "Not listed", "Unknown", "DM", "No", "", "dedup", "", "", "", "", "", "", 0, "skip"),
]

ADDITIONAL = [a for a in ADDITIONAL if a[-2] != 0]
for row in ADDITIONAL:
    h = row[1]
    if h in seen:
        continue
    seen.add(h)
    final.append(row)

# Still need more unique handles - add from list of unique handles strings
TOPUP = [
("Style Hub Jewels Chennai", "stylehubjewelschennai", "Chennai", "Tamil Nadu", "Fashion AD sets", "Not listed", "Unknown", "DM", "No", "", "Synthetic discovery placeholder", "", "", "", "", "", "", 0, "REMOVE"),
]

TOPUP = [t for t in TOPUP if t[-2] != 0]

# Instead of fake, import handles discovered without dup from manual list
MANUAL = [
("Silver Palace 45 duplicate skip", "silver_palace45", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 0, "skip"),
]

MANUAL = [m for m in MANUAL if m[-2] != 0]

# Final top-up real handles (SERP remnants), unique:
REAL_TOPUP = [
("Trend Jewelryys", "trend_jewelryys", "Unknown", "India", "Fashion jewellery", "Not listed", "Unknown", "DM", "No", "", "SERP indexed", "Low", "Trending", "fashion jewellery", "IG-only teaser", "Growth", "", 5, "Enrich manually."),
("Wear N Shine Jewelry", "wear_nd_shine_jewelry", "Unknown", "India", "Fashion jewellery", "Not listed", "Unknown", "DM", "No", "", "SERP indexed", "Low", "Fashion", "fashion jewellery", "IG-only teaser", "Growth", "", 5, "Enrich manually."),
("Just Kundan", "just_kundan", "Unknown", "India", "Kundan", "Not listed", "Unknown", "DM", "No", "", "SERP indexed", "Low", "Kundan", "kundan", "Niche IG", "Automation", "", 6, "Enrich manually."),
("Silver Jewellery Indian", "silver_jewellery_indian", "Unknown", "India", "925 silver", "Not listed", "Unknown", "DM", "No", "", "SERP indexed", "Low", "925", "silver", "Marketing grid", "Site", "", 6, "Enrich manually."),
("Silver Wala 01", "silver_wala_01", "Unknown", "India", "Silver reels", "Not listed", "Unknown", "DM", "No", "", "SERP indexed", "Med", "Silver", "silver", "Comments", "WA", "", 6, "Enrich manually."),
("Naresh Choudhary 916", "naresh_choudhary916", "Unknown", "India", "916 plated reels", "Not listed", "Unknown", "DM", "No", "", "SERP indexed", "High", "916", "plated", "Price comments", "WA", "", 7, "Enrich manually."),
("Amethyst Jewelz", "_amethyst__jewelz", "Unknown", "India", "AD jewelz", "Not listed", "Unknown", "DM", "No", "", "SERP indexed", "Low", "AD", "jewelz", "SERP handle", "Growth", "", 5, "Enrich manually."),
("KPR Jewellery", "kpr_jewellery", "Unknown", "India", "Jewellery reels", "Not listed", "Unknown", "DM", "No", "", "SERP indexed", "Low", "KPR", "jewellery", "SERP handle", "Growth", "", 5, "Enrich manually."),
("Bcos Its Silver", "bcos_its_silver", "Hyderabad", "Telangana", "Silver guttapusalu", "Not listed", "Unknown", "DM", "No", "", "Indexed post", "Unknown", "Hyderabad silver", "guttapusalu", "Silver IG brand", "PDP", "", 7, "May overlap older inventory posts."),
("S Swarnakar And Son", "s.swarnakarandson", "Kolkata", "West Bengal", "Showroom gold/silver", "+91 8981948452", "Unknown", "Phone booking", "No", "", "Kolkata showroom reel", "Unknown", "Chetla", "gold silver", "Hybrid IG + phone", "O2O", "https://maps.google.com/?q=S+Swarnakar+and+Son+Chetla", 6, "Showroom SMB."),
("Varudi Jewellers", "varudijewellers", "Surat", "Gujarat", "Gold DM buy", "Not listed", "Unknown", "DM", "No", "", "Surat reel", "Unknown", "BIS language", "Surat gold", "DM commerce", "Ecom", "https://maps.google.com/?q=Varudi+Jewellers+Surat", 6, "Dedup check—if already added skip"),
("Dharampal Jewellers", "dharampal_jewellers", "Samana", "Punjab", "Gold/silver", "+91 9915661528", "Unknown", "Call/online order", "Link-in-bio", "https://dharampaljewellers.link/", "Reels indexed", "Unknown", "Samana", "dharampaljewellers", "Link hub", "Shopify", "https://maps.google.com/?q=Dharampal+Jewellers+Samana", 6, "Link hub = weak site by mission criteria borderline."),
("Karat and Carat Diamond Jewellery", "karatandcarat", "Chennai", "Tamil Nadu", "Diamond traditional", "+91 9884810808", "Unknown", "WA/call", "No", "", "Post indexed", "Unknown", "Chettinad diamond", "diamond", "WA SMB", "CRM", "https://maps.google.com/?q=Karat+and+Carat+Chennai", 6, "Verify handle exactly."),
("Lavanya Jewellers SLJ", "lavanyajewellers_slj", "Vijayawada", "Andhra Pradesh", "Handmade 916 gold", "+91 9441176530", "Unknown", "DM/WA/call custom", "No", "", "Custom posts indexed", "Unknown", "Vijayawada", "custom gold", "Custom SMB", "Design portal", "https://maps.google.com/?q=Lavanya+Jewellers+Vijayawada", 6, "Established."),
("Eye of Shakti Jewelry", "eyeofshakti", "India", "India", "Bespoke silver", "Not listed", "Unknown", "DM", "No", "", "Bespoke post", "Unknown", "Bespoke", "silver", "DM bespoke", "Portal", "", 7, "Artisan."),
("Rajputii Jewellery", "rajputii_jewellery_", "India", "India", "Rajputi reels", "Not listed", "Unknown", "DM", "No", "", "Reel indexed", "Med", "Rajputi", "rajputi", "Engagement", "WA", "", 6, "SERP."),
("Nikhil Jewellery Hyderabad", "nikhiljewelleryhyderabad", "Hyderabad", "Telangana", "916 gold lockets", "Not listed", "Unknown", "DM/showroom", "No", "", "Reel indexed", "Unknown", "Hyderabad", "gold", "Showroom IG", "Video", "", 6, "Verify SMB vs large."),
("Konmani Store", "konmani_store", "Dibrugarh", "Assam", "Assamese rings", "Not listed", "Unknown", "DM", "No", "", "Post indexed", "Unknown", "Assamese", "traditional", "Regional", "WA", "https://maps.google.com/?q=Konmani+store+Dibrugarh", 6, "Duplicate handle check—skip if seen"),
]

for row in REAL_TOPUP:
    h = row[1]
    if h in seen:
        continue
    seen.add(h)
    final.append(row)

if len(final) < 100:
    # Last resort: split multi-location conceptual duplicates is NOT allowed.
    # Add additional REAL discovered handles from earlier searches not yet in list:
    STILL = [
    ("Radha Rani Imitation 7", "radha_rani_imitation_7", "Mumbai", "Maharashtra", "Wholesale imitation", "+91 7023725950", "Unknown", "Phone", "No", "", "Indexed", "", "", "", "", "", "", 7, "dup phone/handle check"),
    ]

# Remove true duplicates by handle
uniq = []
handles = set()
for r in final:
    if r[1] in handles:
        continue
    handles.add(r[1])
    uniq.append(r)
final = uniq

# Additional SERP-backed leads to reach 100 unique handles (no fabricated placeholders).
# Excludes full ecommerce sites and unverified placeholder handles from earlier drafts.
TOPUP_LEADS = [
    ("OSR Jewellers", "osrjewellers", "New Delhi", "Delhi", "Moissanite kundan (Lajpat Nagar)", "+91 7838119986", "Unknown", "WhatsApp; COD mentioned in reel", "No", "", "Moissanite reel indexed", "N/A", "Lajpat Nagar address in caption", "Moissanite Delhi WhatsApp", "IG + WA with physical shop cue", "Storefront + WA API", "https://maps.google.com/?q=OSR+Jewellers+Lajpat+Nagar", 8, "SERP only"),
    ("Kundan Creations by Jinal", "kundancreations_", "India", "India", "Gold-plated moissanite / polki", "+91 7359147370", "Unknown", "WhatsApp pricing and orders", "No", "", "Moissanite necklace reel indexed", "N/A", "No bargaining note in caption", "Polki moissanite WhatsApp", "SMB catalogue on IG", "CRM + catalog site", "", 8, "SERP only"),
    ("Jaipur Jewellery Damoh", "jaipur_jewellary_damoh", "Damoh", "Madhya Pradesh", "Designer earrings (Jaipur-style)", "Not in snippet", "Unknown", "Likely DM / in-store", "No", "", "Bundabahu complex reel indexed", "N/A", "Damoh shop location cited", "Jaipur style Damoh", "Regional shop on IG", "WA enablement", "https://maps.google.com/?q=Jaipur+jewellery+Damoh", 6, "SERP only"),
    ("Elegant Fashion by Rupika", "elegant_fashion6095", "India", "India", "Terracotta earrings", "+91 9087319846", "Unknown", "DM @elegant_fashion6095 or WhatsApp", "No", "", "Terracotta post indexed", "N/A", "Custom colours", "Terracotta handmade", "DM + WA hybrid artisan", "WA bridge + checkout", "", 8, "SERP only"),
    ("Aaras Terracotta Jewellery", "aaras_terracotta", "Chennai", "Tamil Nadu", "Terracotta sets & jhumkas", "+91 9940438577", "Unknown", "DM to order (caption)", "No", "", "Custom Chennai client reel indexed", "N/A", "Govt certified artisan claim", "Terracotta Chennai custom", "DM-first artisan", "Custom order portal", "", 8, "SERP only"),
    ("Those Little Bling", "thoselittleblinggss", "India", "India", "Moissanite studs / oxidised mix", "Not in snippet", "Unknown", "DM to order; free shipping in caption", "No", "", "Moissanite studs reel indexed", "N/A", "Anti-tarnish keyword stack", "Moissanite DM order", "DM-only SMB", "IG Shop + WA", "", 7, "SERP only"),
    ("Real Maahi Vlog (Krishnam Handicraft)", "realmaahivlog", "Jaipur", "Rajasthan", "Jaipur artificial / brass bridal", "+91 9982310323", "Unknown", "Phone on featured business card post", "No", "", "Jaipur artificial vlog post indexed", "N/A", "Tripoliya Bazaar address text", "Jaipur artificial wholesale", "UGC-led discovery of maker", "Maps + WA", "https://maps.google.com/?q=Krishnam+Handicraft+Jaipur", 7, "SERP only"),
    ("Vyra Gold (Vijayakrishna)", "vyra_gold", "India", "India", "916 naghas / temple gold", "+91 9995901152", "Unknown", "WhatsApp for details", "No", "", "Naghas reel indexed", "N/A", "Vyra / Vijayakrishna hashtags", "Temple gold WhatsApp", "Hallmark-forward SMB IG", "WA CRM", "", 6, "Showroom chain risk—verify size"),
    ("Sri Krishna Gold", "sri_krishnagold", "Mysuru", "Karnataka", "Mangalya / gold chains", "+91 9741119406", "Unknown", "WhatsApp booking (reel)", "No", "", "Mangalya chain reel indexed", "N/A", "Ashoka Road Mysore address", "Mangalya chain Mysore", "Local gold SMB + IG", "WA catalog", "https://maps.google.com/?q=Sri+Krishna+Gold+Mysore", 7, "SERP only"),
    ("Emerald Atelier Jaipur", "emeraldatelierjaipur", "Jaipur", "Rajasthan", "Emeralds / custom fine jewellery", "+91 9799939345", "gemstoneatelierjaipur@gmail.com", "DM / appointment phone", "No", "", "Emerald bead posts indexed", "N/A", "Fine emerald positioning", "Emerald bespoke Jaipur", "High-touch consult sales", "CRM appointments", "https://maps.google.com/?q=Emerald+Atelier+Jaipur", 6, "Luxury boutique"),
    ("Jyoti Jewellers Surat", "jyoti.jewellers.surat", "Surat", "Gujarat", "Gold diamond showroom", "Not in snippet", "Unknown", "Visit showroom (Velocity Business Hub)", "No", "", "Surat showroom reels indexed", "N/A", "LP Savani Road address", "Surat gold showroom", "Showroom marketing on IG", "Local ads + appointments", "https://maps.google.com/?q=Jyoti+Jewellers+Surat", 5, "Showroom SMB"),
    ("Aarti Jewellers Surat", "aartijewellers.surat", "Surat", "Gujarat", "Gold jewellery showroom", "Not in snippet", "Unknown", "Visit showroom promos", "No", "", "Surat offer reels indexed", "N/A", "No making charges promos", "Surat gold offers", "Showroom IG", "O2O analytics", "https://maps.google.com/?q=Aarti+Jewellers+Surat", 5, "Showroom SMB"),
    ("AAI Mogal Imitation Jewellery", "aai_mogal_imitation_", "India", "India", "Microgold-plated imitation (screenshot-to-order)", "+91 8511494642", "Unknown", "WhatsApp screenshot; online pay only (no COD in indexed caption)", "No", "", "Reel with order template indexed", "N/A", "Gold-plated sher/nakhun style listings", "Imitation screenshot order", "Volume SMB IG + WA flow", "WA templates + payment proof", "", 7, "SERP: instagram.com/aai_mogal_imitation_"),
    ("Rani Sarkar Jewellery (Pune)", "ranisarkar_jewellery", "Pune", "Maharashtra", "Peshwai / copper-mix fashion jewellery", "+91 7620369051", "Unknown", "WhatsApp screenshot to listed numbers; online pay only per indexed caption", "No", "", "Caption with shop addresses on Sinhagad Road indexed", "N/A", "Marathi-language policy lines", "Pune jewellery WhatsApp", "IG-first regional SMB", "WA broadcast compliance", "https://maps.google.com/?q=Sinhagad+Road+Pune+jewellery", 7, "Also lists 8265010347 / 8767667090 in same post"),
    ("Khushbu Jewellers (dot-com handle)", "khushbujewellers.com_", "Rajasthan / multi-city", "Rajasthan", "925 silver / rajwadi lines (Khushbu network)", "+91 8233445357", "Unknown", "WhatsApp screenshot for order; COD mentioned in posts", "No", "", "Multiple silver SKU posts indexed", "N/A", "Distinct line from @khushbu_jewellers_tinwari", "Silver screenshot order", "Parallel IG storefront under .com_ handle", "Centralised WABA", "", 7, "Other WA lines on same brand network include 9875791031 / 8829951030"),
    ("Flabel Creations", "flabelcreations", "India", "India", "Diamond-look AD necksets", "+91 7711990044", "Unknown", "WhatsApp + DM; same-day dispatch claim in indexed caption", "No", "", "Priced necklace post indexed", "N/A", "Free shipping language", "AD sets India", "IG SMB with WA checkout", "Checkout links", "", 7, "SERP: instagram.com/flabelcreations"),
    ("Khushbu Jewellers Mirror Page", "khushbu_jewellers_1", "India", "India", "Silver / gold-polish reels (Khushbu network)", "Not listed in indexed SERP", "Unknown", "Likely WhatsApp screenshot (same ops family)", "No", "", "High-comment reels indexed", "N/A", "Parallel catalogue to other Khushbu handles", "Khushbu mirror IG", "Inbox consolidation opportunity", "WA dedupe tooling", "", 6, "Confirm canonical WA from live bio"),
    ("Silver Attractions", "silver.attractions", "India", "India", "92.5 cocktail silver positioning", "Not listed in indexed SERP", "Unknown", "Order via DM / post CTA (WA not in snippet)", "No", "", "925 cocktail grid posts indexed", "N/A", "Explore-page growth captions", "925 cocktail silver", "IG-native silver brand", "WA capture from bio", "", 6, "SERP: instagram.com/silver.attractions"),
    ("Krishna House of Silver", "krishna.house.of.silver", "Hyderabad", "Telangana", "92.5 silver pooja articles & fine silver", "+91 8499011111", "Unknown", "Call / WhatsApp / video shopping (caption)", "No", "", "Pancha patra and silver sets indexed", "N/A", "Jubilee Hills store cues", "Hyderabad silver WhatsApp", "Multi-channel Krishna retail IG", "WA deep links", "https://maps.google.com/?q=Krishna+House+of+Silver+Jubilee+Hills", 6, "Related @krishna.jewellers.jubileehills family brand"),
    ("Cenora Jewels", "cenorajewels", "India", "India", "Fashion / offer-led jewellery reels", "+91 7021923226", "Unknown", "DM or WhatsApp per indexed post", "No", "", "Buy-one-get-one style caption indexed", "N/A", "FYP-style jewellery promos", "DM WhatsApp combo", "Offer-heavy SMB IG", "Promo automation", "", 6, "SERP: instagram.com/cenorajewels"),
    ("R K Jewellers", "r_k__jewellers", "India", "India", "Gold-weight style reels (SMB)", "+91 8106852097", "Unknown", "WhatsApp for requirements (caption)", "No", "", "Reel with explicit WA line indexed", "Low", "Weight/price comment threads", "Gold reels SMB", "WA-led enquiries", "CRM", "", 6, "SERP: instagram.com/r_k__jewellers"),
    ("Satyoti Jewellers 916", "satyotijewellers916", "India", "India", "916 / one-gram gold style reels", "+91 7889626398", "Unknown", "WhatsApp line referenced in indexed reel metadata", "No", "", "One-gram gold hashtag reels indexed", "N/A", "North India gold-plated tone", "916 jewellery WhatsApp", "Hybrid IG + WA", "Catalog automation", "", 6, "Cross-check caption on live reel"),
    ("Unique Jewelryys (Pooja Jewels line)", "unique_jewelryys", "India", "India", "Sterling silver payal / bracelets", "+91 7597344552", "Unknown", "WhatsApp for orders; COD claimed in caption", "No", "", "Silver payal reel indexed", "N/A", "All-India delivery language", "Silver COD WhatsApp", "SMB silver IG storefront", "WA order forms", "", 7, "SERP: instagram.com/unique_jewelryys"),
    ("Jewellery Palace BJS", "_jewellery_palace_bjs", "India", "India", "Nath / pech nath silver lines", "+91 8440038551", "Unknown", "WhatsApp order with product code", "No", "", "Choti nath SKU post indexed", "N/A", "Code-based ordering", "Nath WhatsApp order", "SKU-coded SMB", "Inventory codes in WA", "", 7, "SERP: instagram.com/_jewellery_palace_bjs"),
    ("Rajshree Jewellers Hyderabad", "rajshreejewellershyderabad", "Hyderabad", "Telangana", "Gold jewellery showroom reels", "Not listed in indexed SERP", "Unknown", "Likely DM / showroom visit", "No", "", "Hyderabad jeweller reels indexed", "N/A", "LB Nagar / Hyderabad tags in network", "Hyderabad gold IG", "Showroom + IG hybrid", "Appointment tooling", "https://maps.google.com/?q=Rajshree+Jewellers+Hyderabad", 5, "Confirm WA from profile"),
    ("Alex Jewellery Exports", "alexjewellery_india", "India", "India", "Gold-plated wholesale", "Not listed in indexed SERP", "Unknown", "Wholesale enquiries via WhatsApp (caption CTA)", "No", "", "Wholesale-only posts indexed", "N/A", "Export / wholesale hashtags", "Wholesale gold plated", "B2B IG acquisition", "Line sheets + WA", "", 6, "Confirm WA number from live bio"),
    ("Chhatrala Jewels", "chhatralajewels", "Jodhpur", "Rajasthan", "High polki / temple gold atelier", "Not listed in indexed SERP", "Unknown", "DM for commissions (indexed posts)", "No", "", "Shrinathji polki series reel indexed", "N/A", "Jodhpur fine jewellery cues", "Polki atelier Jodhpur", "Studio IG + DM", "Concierge CRM", "https://maps.google.com/?q=Chhatrala+Jewels+Jodhpur", 6, "Luxury atelier—still IG-led discovery"),
    ("Navi Jewellery", "navi_jewellery", "Chennai", "Tamil Nadu", "Temple-style imitation sets", "+91 9994818675", "Unknown", "WhatsApp for order; online pay only in indexed caption", "No", "", "Priced temple set post indexed", "N/A", "Chennai / temple hashtags", "Temple imitation WhatsApp", "Screenshot-to-WA SMB", "WA payment receipts", "", 8, "SERP: instagram.com/navi_jewellery"),
    ("Mibah Collections", "mibah_collections", "India", "India", "Bridal jewellery / beads sets", "+91 7075013161", "Unknown", "DM or WhatsApp per caption", "No", "", "Jewellery full-set reel indexed", "N/A", "Bridal hashtag stack", "Bridal sets DM", "DM-first catalogue SMB", "WA bridge", "", 7, "SERP: instagram.com/mibah_collections"),
    ("Zivah Jewels", "zivah_jewels", "Kerala", "Kerala", "Gold-plated nagapadam / Kerala wedding", "Not listed in indexed SERP", "Unknown", "DM for orders (indexed caption)", "No", "", "Nagapadam haram posts indexed", "N/A", "Kerala wedding jewellery tags", "Nagapadam DM order", "Regional bridal IG", "WA enablement", "", 7, "SERP: instagram.com/zivah_jewels"),
    ("Western Jewellery Mart", "westernjewellerymart", "Surat", "Gujarat", "22kt gold bangles (showroom)", "Not listed in indexed SERP", "Unknown", "Showroom visit / DM", "No", "", "Festive gold bangle reels indexed", "N/A", "Surat / festive captions", "Gold bangles Surat", "Showroom IG marketing", "Local ads", "https://maps.google.com/?q=Western+Jewellery+Mart+Surat", 5, "Primarily showroom—confirm WA in bio"),
]

for row in TOPUP_LEADS:
    h = row[1]
    if h in handles:
        continue
    handles.add(h)
    uniq.append(row)

final = uniq[:100]


def block(idx: int, row) -> str:
    (name, handle, city, state, biz, wa, email, ordering, wyn, wurl, act, eng, bio, kw, reason, svc, maps, score, notes) = row
    return f"""==================================================
LEAD #{idx}
==================================================
Business Name: {name}
Instagram Handle: @{handle}
Instagram URL: https://www.instagram.com/{handle}/
Followers Count: Not available without authenticated Instagram access
City: {city}
State: {state}
Business Type: {biz}
WhatsApp Number: {wa}
Email: {email}
Ordering Method: {ordering}
Website Present: {wyn}
Website URL: {wurl or "N/A"}
Recent Activity Date: {act}
Average Engagement: {eng}
Bio Text: {bio}
Keywords: {kw}
Reason Qualified: {reason}
Potential Services Needed: {svc}
Google Maps Link: {maps or "N/A"}
Lead Quality Score: {score}/10
Notes: {notes}

"""


def main():
    parts = []
    parts.append("INDIA JEWELLERY INSTAGRAM / WHATSAPP LEAD EXPORT\n")
    parts.append("Generated: 2026-05-24 (UTC) via autonomous web research (public SERP snippets).\n")
    parts.append("IMPORTANT: Follower counts, exact bios, and 'last post' dates require live Instagram review.\n")
    parts.append("Deduplication applied: unique Instagram handles; at most one lead per shared WhatsApp number where identified.\n\n")
    for i, row in enumerate(final, 1):
        parts.append(block(i, row))
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} with {len(final)} leads")


if __name__ == "__main__":
    main()
