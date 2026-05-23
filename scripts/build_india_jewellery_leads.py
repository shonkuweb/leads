#!/usr/bin/env python3
"""Generate india_jewellery_instagram_leads.txt from curated seed rows.

Each seed row is pipe-delimited (19 fields):
business|handle|wa|city|state|type|order|website_yes_no|website_url|score|keywords|reason|services|notes|email|bio|activity|engagement|gmaps

Empty cells mean unknown / not captured in the public search index used during lead gathering.
"""

from __future__ import annotations

import os
import textwrap

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "india_jewellery_instagram_leads.txt")

SEED = r"""
Beautiful Creations (Kundan / Moissanite)|beautiful_creations0365|+91 9911283949|India (ship-wide)|Not stated|Kundan / moissanite bridal|DM or WhatsApp with product picture|No||9|kundan, moissanite, DM, WhatsApp|Indexed posts show DM+WhatsApp booking flow with picture.|Ecommerce, WhatsApp automation, CRM, catalogue|Follower count not in public index—verify in Instagram app.|Not captured|Booking via DM/WhatsApp 9911283949 per indexed posts.|Indexed 2025-style posts|Not available|Not found
Those Little Bling|thoselittleblinggss|DM primary (no WA in snippet)|India|Not stated|Oxidised / moissanite fashion|DM to order|No||8|dm to order, moissanite, oxidised|Multiple indexed posts use “free shipping dm to order”.|Website + optional WhatsApp backup|Some URLs are /p/ without username; sibling posts confirm handle.|Not captured|Oxidised + moissanite catalogue style posts.|Indexed reels/posts|Varies|Not found
Elegant Fashion by Rupika|elegant_fashion6095|+91 9087319846|Not stated|Not stated|Terracotta earrings|DM or WhatsApp|No||8|terracotta, handmade, DM, WhatsApp|Handmade + dual channel ordering.|Ecommerce, product pages|Verify latest bio.|Not captured|Custom colours mentioned in indexed post.|Older indexed post; account likely active|Not available|Not found
Aaras Terracotta Jewellery|aaras_terracotta|+91 9940438577|Chennai|Tamil Nadu|Terracotta sets / jhumkas|DM to order (number in caption)|No||8|terracotta, customised, DM|Artisan-style terracotta with custom sets.|Site + intl shipping UX|Govt certified artisan claim in indexed title—verify.|Not captured|Worldwide shipping mentioned.|Indexed|Not available|Not found
Sruthi Terracotta Creations|sruthiterracottacreations|+91 9036384234|Bangalore|Karnataka|Terracotta heavy sets|DM / wa.me|No||8|wa.me, terracotta, customised|Explicit wa.me path.|WhatsApp deep links automation|Verify latest wa.me.|Not captured|Bangalore fashion hashtags.|Indexed|Not available|Not found
Chic Quilling|chic_quilling||India|Not stated|Paper quilling earrings|DM for order|No||7|quilling, DM for order, eco|DM-only microbrand pattern.|Ecommerce|Handle normalized from indexed title @Chic_Quilling.|Not captured|Paper filigree earrings.|Indexed|Not available|Not found
Quillingstuff Handcrafted|quillingstuff||India|Not stated|Quilling bridal bangles|DM or WhatsApp (truncated)|No||7|quilling, bridal bangles|Custom bridal quilling bangles.|Catalogue site|Reel text truncated in search index.|Not captured|Customised bridal bangles.|Indexed reel|Not available|Not found
I Imitation Jewellery|i_imitation_jewellery||India|Not stated|Imitation necklace & bangles|DM for order|No||7|imitation, DM for order|Clear DM-commerce CTA.|WhatsApp line + ecommerce|Low extra metadata in index.|Not captured|Premium imitation language.|Indexed|Not available|Not found
Jewellery Shopper|jewellery_shopper_|+91 8905291031 / +91 9929595357|India|Not stated|Silver / themed jewellery|WhatsApp screenshot order|No||6|WhatsApp screenshot, COD, silver|Screenshot ordering; posts mention “website order” text—verify Shopify.|Ecommerce migration, CRM|Multiple numbers across posts—dedupe before outreach.|Not captured|Heavy promotional captions.|Frequent indexed posts|High on some posts|Not found
Jodhpuri Silver|jodhpuri_silver|+91 9358839704|Jodhpur|Rajasthan|Rajputi / silver payal|WhatsApp screenshot order|No||7|silver payal, WhatsApp|WhatsApp-first + COD language.|Inventory + ecommerce|Khushbu branding appears on reels—verify relationship.|Not captured|Rajasthani / Marwari hashtags on some posts.|Indexed reels|Comments on posts|Not found
Silver Attractions|silver.attractions||India|Not stated|Silver fashion|DM / comments pricing|No||6|silver, comments|Comment-driven selling in index.|WhatsApp automation|Less explicit contact in snippet.|Not captured|Users ask “Price?” in comments.|Indexed|Moderate|Not found
Silver Palace 45|silver_palace45||India|Not stated|Silver jewellery|DM/WhatsApp (verify)|No||6|silver|Appears in jewellery vertical cluster.|Lead capture|Sparse snippet.|Not captured|Not captured|Indexed|Low|Not found
Jewellery Palace (BJS)|_jewellery_palace_bjs|+91 8440038551|India|Not stated|Bridal nath / pech nath|WhatsApp order|No||8|nath, WhatsApp order|Explicit WhatsApp order line.|Catalogue + CRM|Not captured|Not captured|Indexed|Not available|Not found
Biswakarma Jewellery Shilpaya|bjs2k|+91 9874085669|India|Not stated|Diamond nosepins / earrings|WhatsApp for orders|No||7|WhatsApp, diamond|Repeated WhatsApp CTAs.|CRM, booking site|Fine diamond—confirm SMB vs retailer.|Not captured|Long marketing captions.|Indexed|Not available|Not found
Lakshmi Creations (Imitation)|lakshmi_creations_9|+91 9849567353|Hyderabad (inferred)|Telangana|Imitation / wholesale jhumkas|WhatsApp orders|No||8|imitation, wholesale, WhatsApp|Wholesale + WhatsApp distribution.|B2B portal|City inferred from search clustering.|Not captured|Wholesale pricing language.|Indexed|Trending tags|Not found
Sujatha Gold Covering Works|sujatha_gold_covering_works|+91 7382222208 / 7997757703 / 8886428899 / 7036132171|Machilipatnam area|Andhra Pradesh|One-gram gold plated|WhatsApp bookings; COD mentioned|No||9|one gram gold, COD|Multi-number WhatsApp + COD.|Automation, ERP, ecommerce|Pick latest primary line from newest reel.|Not captured|Microplated / bridal tags.|Indexed reels|Not available|Not found
Begum Bazar Wholesale Jewelry|begumbazar_wholesale_jewelry|+91 9618136342|Hyderabad (Begum Bazar)|Telangana|One gram gold necksets|DM or WhatsApp screenshot|No||8|Begum Bazar, onegramgold|Screenshot workflow.|Automation, PIM|Not captured|Not captured|Indexed|Not available|Not found
Roshi Collections|roshi.collections|+91 9092327836|Tamil Nadu (TN ship)|Tamil Nadu|One gram gold forming|WhatsApp + screenshot + price|No||9|one gram forming, WhatsApp|Strict online payment / no COD posts.|Checkout + reconciliation|Opening video policy posts.|Not captured|Screenshot booking instructions.|Indexed|Not available|Not found
Dreams Jewellery|dreamsjewellery|+91 9099003670 / 9106503944|India|Not stated|One gram gold / men’s bracelet|WhatsApp for price|No||8|one gram gold, dreamsjewellery|Hashtag handle on indexed post.|Ecommerce + WhatsApp|Confirm handle matches caption hashtag.|Not captured|Verify ownership in app.|Indexed|Not available|Not found
Janvish One Gram Gold & Boutique|janvish_onegramgold_and_boutiq|+91 8121769801|India|Not stated|One gram gold boutique|Screenshot + WhatsApp; WA group|No||8|one gram gold, WhatsApp group|Community updates pattern.|Community tooling + ecommerce|Not captured|Free ship mentions.|Indexed reel|Not available|Not found
Jewels of Karnataka|jewelsofkarnataka|+91 9740234813|Karnataka|Karnataka|One gram mangalya / havalu|WhatsApp on posts|No||8|JK collection, one gram|Persistent WA line on SKU posts.|Catalogue ecommerce|Not captured|Not captured|Indexed|Not available|Not found
Mahalaxmi Jwellers|mahalaxmi_gold99|+91 9880820391 / 7348921999|Mysuru / Karnataka|Karnataka|916 hallmark gold|DM + WhatsApp|No||7|916, DM, WhatsApp|Dual WA lines.|CRM + inventory site|Fine gold—confirm SMB scope.|Not captured|Multi-city tags in reel.|Indexed reel|Not available|Not found
Sai Jewellers Rajat (Ujjain)|sai_jewellers_rajat_ujjain|+91 7024274632|Ujjain|Madhya Pradesh|Gold plated lightweight|WhatsApp / DM only|No||9|gold plated, WhatsApp, MP|Location pinned in comment thread.|Ecommerce + WhatsApp automation|Strong fit.|Not captured|DM-only language on indexed comment.|Indexed|Visible engagement|Not found
Poddar Jewels|poddarjewels|+91 9899134124|India|Not stated|Kundan polki / moissanite|WhatsApp wholesale/retail|No||8|kundan polki, wholesale WhatsApp|Explicit WA enquiries.|B2B portal|Not captured|Not captured|Indexed|Not available|Not found
Just Kundan|just_kundan||India|Not stated|Moissanite polki carved|DM likely (verify)|No||7|kundan, moissanite|INR + shipping style posts.|Ecommerce|WhatsApp not in snippet.|Not captured|Product code style captions.|Indexed|Not available|Not found
Asha Bangles Official|ashabanglesofficial|+91 7014592741|Patiala / North India|Punjab / Haryana (approx)|Punjabi bridal chura|WhatsApp; partial COD|No||9|chura, WhatsApp, custom|Long-running bridal vertical.|Configurator + CRM|Related sister-brand posts exist.|Not captured|Partial COD claims in posts.|Indexed|Not available|Not found
Wedding Answers|weddinganswers|+91 8368213149|Delhi / Mumbai refs|Delhi (assumed)|Bridal kalire / boxes|WhatsApp or DM|No||8|kalire, chooda box, DM|Advance payment policy.|Ecommerce + CRM|Not captured|Strict no-COD language.|Indexed|Not available|Not found
South Indian Temple Jewellery|southindian__templejewellery|+91 7904076978 / 8610765751|Chennai (tag)|Tamil Nadu|Temple / matt finish|DM or WhatsApp; WA group|No||9|temple jewellery, chennai seller|Community link in posts.|WA community automation|Online payments only.|Not captured|Multi-state tags.|Indexed|Not available|Not found
Vari Artificial Jewellery|vari_artificials_jewellery|+91 8769988299 / 9461488299|India|Not stated|Temple bangles / artificial|DM or call|No||8|temple jewellery, delivery|Dual numbers + delivery claims.|Ecommerce + logistics|Not captured|Not captured|Indexed|Not available|Not found
Temple Jewellery Hub by Priya|templejewelleryhub_bypriya||India|Not stated|Temple nagas etc.|DM (verify)|No||7|temple jewellery|Temple SKU microbrand.|WA + mini-site|Add number from bio in-app.|Not captured|Not captured|Indexed|Not available|Not found
Hyderabadi Jewellery|hyderabadijewllery||Hyderabad|Telangana|Hyderabadi pearls / haar|DM for details|No||8|Hyderabad, DM, pearls|Custom colour mentions.|WA bridge + ecommerce|Handle spelling jewllery as indexed.|Not captured|Geo tags in captions (verify).|Indexed|Not available|Not found
Bcos Its Silver|bcos_its_silver||Hyderabad|Telangana|Pure silver guttapusalu|DM/call (verify)|No||7|guttapusalu, silver|Premium silver sets.|Ecommerce|Older indexed post.|Not captured|High ticket price in old post.|Indexed (older)|Not available|Not found
Raja Veer Imitation Ahmedabad|rajaveer_imitation_ahemadabad|+91 8511513997|Ahmedabad|Gujarat|One gram / imitation|WhatsApp on reels|No||8|Ahmedabad, imitation|City in handle.|Ads + ecommerce|Not captured|Not captured|Indexed reels|Not available|Not found
Sai Raj Imitation|sairajimmitation_01|+91 8866462720 / 7016862336 / 9054319731|Ahmedabad|Gujarat|Wholesale imitation|WhatsApp / shop visit|No||7|wholesale imitation|Physical shop addresses listed.|B2B portal|Wholesale focus.|Not captured|Old city addresses in reel.|Indexed reel|Shop pins in caption|Ahmedabad old city (verify)
BJ Imitation Ahmedabad|bj_imitation_ahmedabad||Ahmedabad|Gujarat|Brass fashion rings|DM/WhatsApp (verify)|No||6|Ahmedabad, imitation|Weaker snippet.|WhatsApp catalog|Low completeness.|Not captured|Not captured|Indexed|Not available|Not found
Rajputi Jewellery Bhilwara|rajputijewellerybhilwara00|+91 9829900459|Bhilwara|Rajasthan|Rajputi plated sets|WhatsApp orders|No||8|Rajputi, WhatsApp|Explicit WA blocks.|Ecommerce + trust|No COD per post.|Not captured|Handmade look claims.|Indexed|Not available|Not found
Rajputi Jewellery (alt)|rajputii_jewellery_||Rajasthan|Rajasthan|Rajputi|DM/WhatsApp (verify)|No||6|rajputi|Parallel account.|Brand consolidation|May overlap—merge after research.|Not captured|Not captured|Indexed|Not available|Not found
Rajputi Jewellery Wholesaler SC|rajputi_jewelery_wholsaler_s.c|+91 7877634674|India|Not stated|Rajputi wholesale|WhatsApp + group link|No||8|WhatsApp group|Group growth tactic.|Community automation|Not captured|Group join language.|Indexed reel|Not available|Not found
Chudiwale Fashion Jewellery|chudiwale_|+91 7972380643|India|Not stated|Custom bridal bangles|WhatsApp booking|No||8|bangles, customised|Custom bangles + WA booking.|Configurator + ecommerce|Not captured|Velvet bangle niche.|Indexed|Not available|Not found
Mangalmurti / Jewellery Of World|jewellery_of_world|+91 8446200337|Palghar|Maharashtra|Maharashtrian bridal|WhatsApp to shop|No||8|Maharashtrian jewellery|Geo address in post.|Booking system|Rent + purchase mentions.|Not captured|Palghar market address.|Indexed|Palghar address in caption|Palghar (approx)
Lucknow Artificial Jewellery|lucknow_artificial_jewellery_|+91 8957754721|Lucknow|Uttar Pradesh|One gram polish earrings|Booking number|No||8|Lucknow, COD|City-branded COD shipping.|Ads + ecommerce|Confirm WA vs call.|Not captured|COD shipping claims.|Indexed reel|Not available|Not found
Pooja Jewels (Silver)|poojajewels_|+91 7073962052 / 9993284004 (Threads) vs +91 7597344552 (reel)|India|Not stated|Silver jewellery|WhatsApp; COD on reels|No||7|silver, COD|Conflicting indexed numbers—reconcile.|CRM + number unify|Treat as high priority after validation.|Not captured|Stories/offers mentions.|Indexed|Not available|Not found
Flabel Creations|flabelcreations|+91 7711990044|India|Not stated|Diamond-look fashion|WhatsApp + DM; link in bio|No||8|WhatsApp, link in bio|Same-day dispatch language.|Ecommerce + logistics|Not captured|Comment snippet shows WA.|Indexed|Low in snippet|Not found
Y J Jewellery Mumbai|y.j.jewellery_mumbai||Mumbai|Maharashtra|Fashion jewellery combos|DM (verify)|No||6|Mumbai, fashion jewellery|Mumbai handle cluster.|WhatsApp commerce|Sparse snippet.|Not captured|Not captured|Indexed reel|Not available|Not found
Mahaveer Jewelery|mahaveer_jewelery||India|Not stated|Fashion jewellery|DM (verify)|No||6|fashion jewellery|Cluster discovery.|Lead capture|Low snippet.|Not captured|Not captured|Indexed profile|Not available|Not found
Trend Jewelryys|trend_jewelryys||India|Not stated|Fashion jewellery|DM (verify)|No||6|trending|Search tail related account.|Content funnel|Verify WA in bio.|Not captured|Not captured|Indexed|Low|Not found
Wear N Shine Jewelry|wear_nd_shine_jewelry||India|Not stated|Fashion jewellery|DM (verify)|No||6|fashion|Search tail related account.|Lead capture|Verify contact.|Not captured|Not captured|Indexed|Low|Not found
Swarnam Varnam|swarnam_varnam||India|Not stated|Fashion / gold-tone|DM (verify)|No||6|trending|South Indian style cluster.|WhatsApp bridge|Sparse snippet.|Not captured|Not captured|Indexed|Low|Not found
Gohar Jewels Official|goharjewelsofficial||India|Not stated|Resin jhumkas|DM likely|No||7|resin, handmade|Resin microbrand.|Ecommerce + WA|Verify ordering line.|Not captured|Handmade resin niche.|Indexed|Not available|Not found
The Madras Art Studio|themadras_artstudio||Chennai|Tamil Nadu|Resin preserved flowers|DM to order|No||8|resin, DM to order|Explicit DM ordering.|Custom product builder|Not captured|Custom shapes/colours.|Indexed|Not available|Not found
Indukuri's Jewel|indukurisjewel|+91 6302720676|India|Not stated|Lab-grown diamond custom|WhatsApp details|No||7|labgrown, WhatsApp|Custom pendants via WA.|Consult booking + ecommerce|Niche fine.|Not captured|Customization language.|Indexed reel|Not available|Not found
Vernika Silver|vernika.silver.jewellery|+91 7406810666 / 9606406666|Bangalore|Karnataka|92.5 silver|Call / DM / video call|No||7|92.5 silver, Chickpet|Physical shops in captions.|Online booking + ecommerce|Two numbers appear across reels.|Not captured|Raja Market / Avenue Rd addresses.|Indexed reels|Not available|Chickpet / Avenue Rd (verify)
Silver Jewellery by PSJ|__silver_jewellery_psj|+91 8920857565|Delhi|Delhi|925 silver kada|DM or WhatsApp|No||9|925, Lajpat Nagar|Delhi address + DM/WA.|Local SEO + ecommerce|Strong SMB fit.|Not captured|Hallmark claims in reel.|Indexed|Not available|Lajpat Nagar II (from post)
Samskruthi Jewellers|samskruthijewellers|+91 8790112233|India / USA ship|Not stated|925 silver gold-plated bridal|WhatsApp orders|No||8|925 silver, bridal|Reels say WhatsApp for orders.|Ecommerce + CRM|Confirm exact spelling vs samskruthijewellers.|Not captured|USA shipping mentions.|Indexed reels|Not available|Not found
Lavanya Jewellers SLJ|lavanyajewellers_slj|+91 9441176530|Vijayawada|Andhra Pradesh|916 / 22ct gold|DM or WhatsApp customised|No||7|Vijayawada, customised|Custom orders + shipping.|Booking + ecommerce|Physical store referenced.|Not captured|Worldwide shipping mentions.|Indexed|Not available|Kanuru (some reels)
Varudi Jewellers|varudijewellers||Surat|Gujarat|Gold (BIS claims)|DM instant buy|No||7|Surat, DM|DM-led purchasing copy.|Trust checkout|Confirm showroom scale.|Not captured|DM instant buy title.|Indexed reel|Not available|Not found
Oxidised Jewellery Wholesaler|oxidised_jewellery_wholesaler||India|Not stated|Oxidised wholesale|DM/WhatsApp (verify)|No||6|oxidised, wholesale|Wholesale niche.|B2B portal|Snippet empty.|Not captured|Not captured|Indexed|Not available|Not found
Fashion Mantra Official|fashion_mantra_official|+91 9316331344|India|Not stated|Fashion jewellery|Screenshot + WhatsApp|No||8|screenshot booking|Strong WA workflow.|Catalog automation|Not captured|Wholesale + single piece.|Indexed|Not available|Not found
Mantra Fashion Jewellery|mantrafashionjewellery||Machilipatnam|Andhra Pradesh|South Indian imitation|DM (verify)|No||7|machilipatnam, jada pin|Manufacturing hashtags.|Export landing pages|WhatsApp not in snippet.|Not captured|Jada pin pricing post.|Indexed|Not available|Not found
Wholesale Pearls Jewells Onkar|wholesalepearlsjewells.onkar|+91 9996698633|India|Not stated|Wholesale manufacturing marketing|DM for catalog|No||7|wholesale, DM catalog|Phone line + DM catalog.|B2B site|SEO-heavy caption.|Not captured|Long SEO-style caption.|Indexed reel|Not available|Not found
R K Jewellers|r_k__jewellers|+91 8106852097|India|Not stated|Fashion / gold-tone|WhatsApp (comment CTA)|No||7|WhatsApp for requirements|Comment marketing WA.|CRM + ecommerce|Verify category in profile.|Not captured|Comment snippet CTA.|Indexed|Comment CTA|Not found
Supriya Jewellery|supriya_jewellery|+91 9152275741|Mumbai|Maharashtra|Marathi traditional|DM for order|No||8|DM for order, marathi dagine|Order number in collab reels.|Unified WA + ecommerce|Same order # as VS collabs.|Not captured|Collab posts with VS.|Indexed reel|Not available|Not found
VS Jewellery|vs_jewellery|+91 9152275741|Mumbai|Maharashtra|Traditional collabs|DM for order|No||7|DM for order|Collab network.|Brand consolidation|DUPLICATE PHONE with Supriya—merge in CRM.|Not captured|Collab posts.|Indexed|Not available|Not found
Preethu Jewel Box|preethujewelbox||Kerala (assumed)|Kerala|Gold-covering sets|DM / IG (verify)|No||7|gold covering, low ticket|Free delivery language.|WA + ecommerce|Add WA from bio.|Not captured|Malayalam cinema inspired SKUs.|Indexed reel|Not available|Not found
Preet Jewellers 55|preetjewellers55||India|Not stated|Jewellery (verify)|DM/WhatsApp (verify)|No||5|jewellers|Sparse index seed.|Audit before outreach|Low confidence.|Not captured|Not captured|Indexed|Not available|Not found
Sal's Artisau Handmade|salsartisau||Kochi|Kerala|Handmade earrings|DM likely|No||7|handmade, Kochi|Kochi microbrand.|Ecommerce|Add WA from bio.|Not captured|Beadwork earrings.|Indexed|Not available|Not found
Aura Jewel Hunt|aurajewelhunt||India|Not stated|Necklace sets|DM (influencer tags)|No||7|tagged brand|Influencer discovery.|Affiliate + ecommerce|Verify bio contact.|Not captured|Customer tags in posts.|Indexed|Influencer|Not found
Aira Jewel Studio|airajewel_studio||India|Not stated|Gemstone bracelets|DM likely|No||6|handmade, amethyst|Studio pattern.|Ecommerce|Verify channel.|Not captured|Handmade reel.|Indexed|Not available|Not found
Kotiro (B2B Silver)|kotiro.in||India|Not stated|925 gemstone wholesale|IG contact for MOQ|Unknown|https://kotiro.in (verify)|6|wholesale 925|May have .in site—verify “no website” fit.|B2B portal|Exporter language.|Not captured|MOQ/pricing via contact.|Indexed|Not available|Not found
Kotoba Jewellery|kotobajewellery||Unknown|Not stated|Custom rings|DM likely|No||6|custom rings|Atelier posts.|Ecommerce|Confirm India focus.|Not captured|Handmade custom.|Indexed reel|Not available|Not found
Bangles by Kayra|bangles_by_kayra||India|Not stated|Glass bangles|DM likely|No||7|glass bangles|Niche bangles.|WA commerce|Verify WA in bio.|Not captured|Kayra branding.|Indexed reel|Not available|Not found
BB Creatiye Corner|bb_creatiye_corner||India|Not stated|Glass bangles supplier|DM (tags)|No||6|glass bangles|Typo handle—verify.|Instagram shop|Tagged supplier.|Not captured|Influencer tags.|Indexed|Not available|Not found
Babu Churi Wala GK|babuchuriwalagk||Delhi|Delhi|Custom bridal churi|DM / appointment|No||6|custom churi|Historic shop reels.|Online booking|Established offline.|Not captured|Since 1823 claim (verify).|Indexed reel|Not available|Delhi GK (verify)
Jyoti Jewellers Surat|jyoti.jewellers.surat||Surat|Gujarat|Gold/diamond showroom|Visit store + IG|No||6|Surat, showroom|Physical showroom heavy.|Online booking|Large showroom—still IG marketing.|Not captured|Velocity Business Hub address.|Indexed reel|Surat address|Surat (address in reel)
Aarti Jewellers Surat|aartijewellers.surat||Surat|Gujarat|Gold showroom|Visit store + IG|No||6|Surat, gold|Showroom promos.|Digital ads|Large jeweller—qualify SMB fit.|Not captured|No making charges promos.|Indexed reel|Surat|Surat
S Swarnakar And Son|s.swarnakarandson|+91 8981948452|Kolkata|West Bengal|Hallmarked gold|Booking number posts|No||6|Kolkata, gold|Traditional jeweller with IG.|Lead capture + site|May be larger store—qualify.|Not captured|Kolkata/Chetla tags.|Indexed|Not available|Kolkata (Chetla tags)
Nikhil Jewellery Hyderabad|nikhiljewelleryhyderabad||Hyderabad|Telangana|916 gold|IG + shop|No||5|916 gold, Hyderabad|High-ticket gold retailer.|Digital upgrades|Likely larger—use carefully.|Not captured|LB Nagar tags.|Indexed reel|Hyderabad|Hyderabad
Moha by Geetanjali|mohabygeetanjali|+91 9930898047|Mumbai|Maharashtra|Designer 925 silver|WhatsApp in reels|No||8|925 silver, designer|WhatsApp-forward designer silver.|Ecommerce + CRM|Strong designer brand signals.|Not captured|Shop now language.|Indexed reels|Mumbai implied|Not found
RC Jewellers Online|rcjewellersonline|+91 9650730978|Noida|Uttar Pradesh|Bridal diamond/gold|DM + WhatsApp|Yes|https://rcjewellerseshop (verify)|6|DM, WhatsApp, mall|Mall stores—enterprise-ish.|CRM + omnichannel|Still DM/WA CTAs.|Not captured|DLF Mall of India address.|Indexed|Not found|Noida / Greater Noida stores
Mantra Gems|mantragems||India|Not stated|Men’s silver kundal etc.|Follow / DM (verify)|No||6|kundal, silver|Different vertical mix.|WhatsApp catalog|Religious merch mix—verify jewellery focus.|Not captured|Temple travel tags mixed.|Indexed|Not available|Not found
Chiyan Jewelry|chiyanjewelry||India|Not stated|Jewellery (verify)|DM (verify)|No||5|luxury, chiyan|Name collision risk.|Lead audit|Confirm brand/location.|Not captured|Sparse snippet.|Indexed|Not available|Not found
BeYou India|beyouindia.in||India|Not stated|Western earrings|DM (verify)|No||6|western earrings|Imported styles.|IG shop|Verify WA.|Not captured|Imported studs language.|Indexed|Not found|Not found
Jaipur Silver Jewellery JSJ|jaipur.silver.jewellery||Ahmedabad? / Jaipur?|Gujarat / Rajasthan|Silver (Iscon Emporio)|DM (verify)|No||6|Iscon Emporio|Premium mall location.|Ecommerce|Location text mentions Satellite (Ahmedabad).|Not captured|Iscon Emporio address in reel.|Indexed|Ahmedabad|Ahmedabad (Satellite)
925 Silver Jaipur|925silverjpr||Jaipur|Rajasthan|Traditional silver|DM (verify)|No||7|925 silver, Jaipur|Jaipur silver niche.|Ecommerce|Price/weight in reel.|Not captured|Traditional earrings reel.|Indexed|Not found|Jaipur
JK Jewellers Jodhpur|jkjewellersjodhpur36|+91 8619090636|Jodhpur|Rajasthan|92.5 silver wholesale|DM + WhatsApp|No||9|Jodhpur, silver wholesale|Instant buy + DM + WA.|Automation + ecommerce|Strong SMB signals.|Not captured|#jkjewellersjodhpur36|Indexed reel|Not found|Jodhpur
Moriya Jewellers|jewellersmoriya||Jodhpur|Rajasthan|Jodhpuri silver payal|DM (verify)|No||7|Jodhpuri silver|Local payal niche.|WA commerce|Verify WA in bio.|Not captured|Jodhpur tags.|Indexed reel|Jodhpur|Jodhpur
Razia Kunj|raziakunj||Hyderabad|Telangana|Bespoke fine|DM (verify)|No||6|bespoke, Nizam inspo|Bespoke positioning.|Site + appointments|Fine jewellery—qualify SMB.|Not captured|Nizam story marketing.|Indexed|Not found|Hyderabad (brand story)
Raji Fashion Jewelry|raji_fashion_jewelry|+91 9790542092|India|Not stated|Imitation CZ sets|DM or WhatsApp|No||8|imitation, silk thread|Explicit DM+WA.|Ecommerce|Follow @raji_fashion_jewelry posts.|Not captured|Price grid in caption.|Indexed|Not found|Not found
Rings n Pearls|ringsnpearls||India|Not stated|Sterling silver nose rings|Preorder / link in bio|Unknown|link in bio (verify)|6|sterling silver, preorder|Link-in-bio commerce.|Ecommerce|Verify India fulfillment.|Not captured|Preorder language.|Indexed reel|Not found|Not found
Devik Jewels|devik_jewels||India|Not stated|Rajwadi imitation|DM to book|No||8|DM to book, imitation|DM booking + codes.|Ecommerce|Import-from-manufacturer claims.|Not captured|Limited stock language.|Indexed|Not found|Not found
Harsh Jewels|harshjewels_||India|Not stated|22ct gold antique|DM for details|No||6|22ct gold, DM|DM for details pattern.|CRM|Fine gold—qualify SMB.|Not captured|City tags in old post.|Indexed|Not found|Not found
Kosher Jewels|kosherjewels||Mumbai (verify)|Maharashtra|Pearl / diamond sets|DM (verify)|No||6|pearls, diamonds|Fine sets.|Ecommerce|Location not confirmed in snippet.|Not captured|Editorial style posts.|Indexed|Not found|Not found
TJ Jewels Mumbai|tj_jewels_mumbai||Mumbai|Maharashtra|Jewellery (verify)|DM (verify)|No||6|Mumbai|Jewellery account.|Lead audit|Sparse snippet.|Not captured|Not captured|Indexed|Not found|Mumbai
The Jewelkosh|thejewelkosh||Ahmedabad|Gujarat|Imitation store|DM (meme marketing)|No||7|imitation, Ahmedabad|Imitation retailer voice.|IG shop + WA|Ahmedabad tags.|Not captured|Meme marketing reels.|Indexed|Ahmedabad|Ahmedabad
Ridhi Sidhi Jewellers Barmer|ridhi_sidhi_jewellers|+91 7849810107 +91 9875202189 +91 8440965077|Barmer|Rajasthan|Pure silver bangles and kids silver|WhatsApp enquiry; screenshot order language in indexed posts|No||8|Barmer, silver bangles, COD|Indexed posts show multi-number WA workflow.|WA automation, inventory|Reconcile three numbers in CRM; verify active line.|Not captured|Barmer shop location in captions|Indexed reels|Not available|https://www.google.com/maps/search/?api=1&query=Ridhi+Sidhi+Jewellers+Barmer
Gobind Jewellers Durgapur|gobindjewellers|+91 9593222111|Durgapur|West Bengal|Hallmarked gold and bridal sets|Phone contact in indexed posts; IG catalogue|No||7|Durgapur, bridal, gold|Chandidas Market area mentions in indexed captions.|Local SEO, WA booking|Confirm SMB vs large showroom.|Not captured|Traditional bridal hashtags|Indexed|Not available|https://www.google.com/maps/search/?api=1&query=Chandidas+Market+Durgapur
Premraj Shantilal Jain Jewellers|premrajshantilaljainjewellers|+91 9169160096|Jaipur|Rajasthan|Heritage kundan and polki|wa.me link and call in indexed reel; comment for price|No||7|Jaipur kundan, wa.me|Strong WhatsApp deep link plus engagement bait.|Ecommerce, appointments|May be established showroom; qualify budget.|Not captured|Heritage Jaipur kundan marketing|Indexed reel|Not available|https://www.google.com/maps/search/?api=1&query=Jaipur+jewellery+Johari+Bazar
Khushbu Jewellers (khushbujewellers.com_)|khushbujewellers.com_|+91 9875791031 +91 8233445357|India|Not stated|925 silver bridal and sindoor boxes|WhatsApp screenshot order; indexed text mentions website order|Unknown|Verify Shopify or external checkout in bio|6|silver, COD, screenshot|High-intent WA commerce; external site claim in index.|Unify WA and checkout|Cross-check numbers against other Khushbu cluster accounts.|Not captured|Discount and COD language|Indexed 2026 reels|Not available|Not found
SamAsha Jewellery|samashajewellery|+91 9711107695|India|Not stated|Oxidised and German silver jhumkas|DM or WhatsApp BUY NOW flow on reels|No||8|oxidised, jhumka, DM, WhatsApp|Explicit dual-channel ordering CTA.|Catalog automation, CRM|Opening-video policy for exchanges.|Not captured|German silver and oxidised tags|Indexed reel|Not available|Not found
Sree Lakshmi Jewells|lakshmijewells|+91 9390483697|India|Not stated|South Indian matte and rose-gold wholesale|Order and enquiry via WhatsApp; no COD in indexed reel|No||8|wholesale, chandraharam, bridal|Strict policies; manufacturer-style captions.|B2B portal, PIM|Confirm factory vs reseller.|Not captured|South Indian wedding hashtags|Indexed reel|Not available|Not found
""".strip()


def parse_row(line: str) -> dict:
    parts = [p.strip() for p in line.split("|")]
    # Some seed rows omit a trailing empty column; long captions rarely add extra "|".
    while len(parts) < 19:
        parts.append("")
    if len(parts) > 19:
        parts = parts[:18] + ["|".join(parts[18:])]
    keys = [
        "business",
        "handle",
        "wa",
        "city",
        "state",
        "type",
        "order",
        "website_present",
        "website_url",
        "score",
        "keywords",
        "reason",
        "services",
        "notes",
        "email",
        "bio",
        "activity",
        "engagement",
        "gmaps",
    ]
    return dict(zip(keys, parts))


def main() -> None:
    rows = [ln for ln in SEED.splitlines() if ln.strip()]
    leads = [parse_row(ln) for ln in rows]

    # Deduplicate handles (first occurrence wins)
    seen: set[str] = set()
    deduped: list[dict] = []
    for ld in leads:
        h = ld["handle"].lower()
        if not h or h in seen:
            continue
        seen.add(h)
        deduped.append(ld)

    if len(deduped) < 100:
        raise SystemExit(f"Expected >=100 unique handles, got {len(deduped)}")

    deduped = deduped[:100]

    lines: list[str] = []
    lines.append("INDIA JEWELLERY — INSTAGRAM / WHATSAPP FIRST LEADS (AUTO-GENERATED)")
    lines.append("Generated: 2026-05-23")
    lines.append(
        textwrap.dedent(
            """
            METHODOLOGY / LIMITATIONS
            - Built from public web-search snippets of Instagram posts/reels/profiles (no private Instagram API).
            - Fields like follower count are usually NOT in the public HTML search index; they are marked as not captured.
            - “Website Present” reflects what appears in indexed snippets; verify in Instagram bio + Linktree.
            - Phone duplicates across collab accounts (e.g., VS/Supriya) are flagged in Notes—merge in your CRM.
            """
        ).strip()
    )
    lines.append("")

    for i, ld in enumerate(deduped, start=1):
        handle = ld["handle"]
        url = f"https://www.instagram.com/{handle}/"
        lines.append("==================================================")
        lines.append(f"LEAD #{i}")
        lines.append("==================================================")
        lines.append(f"Business Name: {ld['business']}")
        lines.append(f"Instagram Handle: @{handle}")
        lines.append(f"Instagram URL: {url}")
        lines.append("Followers Count: Not captured in public search index (verify in Instagram app)")
        lines.append(f"City: {ld['city']}")
        lines.append(f"State: {ld['state']}")
        lines.append(f"Business Type: {ld['type']}")
        lines.append(f"WhatsApp Number: {ld['wa']}")
        lines.append(f"Email: {ld['email']}")
        lines.append(f"Ordering Method: {ld['order']}")
        lines.append(f"Website Present: {ld['website_present']}")
        lines.append(f"Website URL: {ld['website_url']}")
        lines.append(f"Recent Activity Date: {ld['activity']}")
        lines.append(f"Average Engagement: {ld['engagement']}")
        lines.append(f"Bio Text: {ld['bio']}")
        lines.append(f"Keywords: {ld['keywords']}")
        lines.append(f"Reason Qualified: {ld['reason']}")
        lines.append(f"Potential Services Needed: {ld['services']}")
        lines.append(f"Google Maps Link: {ld['gmaps']}")
        lines.append(f"Lead Quality Score: {ld['score']}/10")
        lines.append(f"Notes: {ld['notes']}")
        lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    print(f"Wrote {len(deduped)} leads to {OUT}")


if __name__ == "__main__":
    main()
