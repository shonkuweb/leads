#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import textwrap

# Tab-separated seed rows:
# BusinessName	handle	phone	city	state	type	ordering	website_yn	website_url	score	reason	keywords	services	notes
RAW = r"""
Pooja Jewels (silver / fashion)	unique_jewelryys	+91 7597344552	Unknown	India	Silver & fashion jewellery	WhatsApp; COD mentioned in indexed reels	No	—	8	Indexed Instagram reels show WhatsApp ordering and nationwide COD for silver pieces.	silver payal, reels, COD	WhatsApp automation, ecommerce, CRM	Primary selling motion appears Instagram-first; verify bio for any link-in-bio store.
Jewellery Palace (BJS)	_jewellery_palace_bjs	+91 8440038551	Unknown	India	Traditional / nath jewellery	WhatsApp order on posts	No	—	8	Explicit WhatsApp ordering line in indexed post.	nath, pech, choti	WhatsApp catalog, lightweight site	Verify city from profile; snippet did not include city.
Chudiwale Fashion Jewellery	chudiwale_	+91 7972380643	Unknown	India	Custom bridal bangles	WhatsApp booking	No	—	9	Customized bangle sets with WhatsApp booking in indexed caption.	custom bangles, bridal	Automation, ecommerce, ads	
Lakshmi Creations (imitation)	lakshmi_creations_9	+91 9849567353	Chennai (inferred)	Tamil Nadu	Imitation / jhumkas	WhatsApp for orders / wholesale	No	—	8	Indexed post shows WhatsApp for wholesale and collections.	wholesale, jhumkas	CRM, B2B microsite	Confirm exact city from bio; inferred from regional clustering in search context.
Mangalmurti / Jewellery of World	jewellery_of_world	+91 8446200337	Palghar	Maharashtra	Maharashtrian bridal jewellery	WhatsApp to shop	No	—	8	Indexed caption includes WhatsApp and physical market location.	thushi, nath, maharashtrian	WhatsApp booking, local SEO	
Rajputi Jewellery Wholesaler	rajputi_jewelery_wholsaler_s.c	+91 7877634674	Unknown	India	Rajputi / wholesale sets	WhatsApp; mentions groups	No	—	7	Wholesale-style Instagram discovery with WhatsApp contact.	rajputi, wholesale	WhatsApp CRM, catalog	
Oxidised Jewellery Wholesaler	oxidised_jewellery_wholesaler	Unknown	Unknown	India	Oxidised wholesale	Assume DM/WhatsApp (verify)	No	—	6	Indexed as wholesaler; contact not in snippet—needs profile check.	oxidised, wholesale	Lead capture landing page	Validate WhatsApp before outreach.
Vernika Silver	vernika.silver.jewellery	+91 7406810666	Bengaluru	Karnataka	925 silver retail	Call / video call booking (add WA Business)	No	—	7	Indexed post shows phone + physical Bengaluru addresses.	925 silver, video call	WhatsApp Business setup, booking automation	Confirm WhatsApp availability on bio.
Biswakarma Jewellery Shilpaya	bjs2k	+91 9874085669	Kolkata (verify)	West Bengal	Diamond jewellery (SMB signals)	WhatsApp orders	No	—	7	Indexed posts repeatedly push WhatsApp for diamond earring/nosepin collections.	diamond nosepin, WhatsApp	CRM, ads, WA automation	City inferred from common SERP clustering; confirm on profile.
Jewels of Karnataka	jewelsofkarnataka	+91 9740234813	Unknown	Karnataka	One-gram / fashion jewellery	WhatsApp	No	—	8	WhatsApp number published on product posts.	one gram gold, shipping	ecommerce, WA catalog	
Mahavir Imitation Jewellery	mahavirimitationjewelle	+91 8320499102	Jaipur	Rajasthan	Imitation / oxidised bangles	Call/WhatsApp in posts	No	—	8	Indexed post lists call number for designs/stock.	imitation, oxidised bangles	local ads, WA automation	
Raja Veer Imitation (Ahmedabad)	rajaveer_imitation_ahemadabad	+91 8511513997	Ahmedabad	Gujarat	Imitation jewellery	WhatsApp implied via phone in reel	No	—	7	Phone shown in indexed reel context for imitation jewellery.	imitation, reels	Instagram growth, WA	
FLabel Creations	flabelcreations	+91 7711990044	Unknown	India	Fashion / AD jewellery	WhatsApp + DM	No	—	8	Indexed caption: WhatsApp + DM for necklace set.	DM, link in bio	WA automation, ecommerce	
Begum Bazar Wholesale Jewelry	begumbazar_wholesale_jewelry	+91 9618136342	Hyderabad (Begum Bazar context)	Telangana	One-gram / necklace sets	DM or WhatsApp	No	—	8	Indexed caption instructs screenshot + DM/WhatsApp.	one gram gold, screenshot order	WA automation, payments stack	
Janvish One Gram Gold & Boutique	janvish_onegramgold_and_boutiq	+91 8121769801	Unknown	India	One-gram gold plated	WhatsApp screenshot orders	No	—	8	WhatsApp groups mentioned; screenshot-to-order pattern.	one gram, groups	CRM, catalog site	
Lucknow Artificial Jewellery	lucknow_artificial_jewellery_	+91 8957754721	Lucknow	Uttar Pradesh	Artificial / one-gram polish earrings	WhatsApp booking	No	—	8	Indexed reel shows booking number and COD mention.	artificial, COD	Automation, ecommerce	
Lalitha Imitation Jewellery	jewellery_by_lalitha	+91 7672044475	Unknown	India	Imitation jewellery	DM or WhatsApp; online payment	No	—	9	Indexed SOP: screenshot + DM/WhatsApp + UPI/bank; no COD.	imitation, SOP	WA flows, ecommerce	
Rishabh Gold / Kolhapuri Saaj	kolhapurithushi	+91 9403830260	Kolhapur (brand focus)	Maharashtra	Gold-plated / Kolhapuri saaj	WhatsApp + link-in-bio shop (verify)	No	—	7	Indexed posts show WhatsApp; “shop online” phrasing appears—confirm if only social checkout.	kolhapuri saaj, thushi	WA commerce, website lite	
Nath Sringar (Supriya)	nath_sringar_by_supriya	Unknown	Unknown	India	Handmade nath / earcuff / mangalsutra	DM or WhatsApp for price	No	—	7	Indexed reel: DM/WhatsApp for price/purchase; number not in snippet.	nath, handmade	WA Business, DM automation	Confirm phone in bio.
Pukhraj Jewellers (Satellite Ahmedabad)	pukhraj.jewellers1	+91 9409151772	Ahmedabad	Gujarat	22K antique / gold jewellery	DM + WhatsApp	No	—	7	Indexed post shows DM order + WhatsApp/call; physical address listed.	antique gold, customise	CRM, marketing automation	Strong retail jeweller signals—confirm SMB vs large showroom from profile.
Jewel Indukuri’s	indukurisjewel	+91 6302720676	Unknown	India	Lab-grown diamond custom	WhatsApp	No	—	7	Custom pendants via WhatsApp in indexed reel.	lab grown, customise	CRM, consultation booking	
Omkar Jewels Surat	omkar_jewels_surat	+91 8141248248	Surat	Gujarat	Custom gold / diamond (atelier)	Call/WhatsApp + visit	No	—	7	Indexed reel lists phone + Surat address; custom positioning.	custom jewelry	Scheduling, portfolio site	
Gohar Jewels Official	goharjewelsofficial	Unknown	Unknown	India	Resin / handmade jhumkas	DM/custom orders (verify phone)	No	—	7	Indexed product post for customised resin jhumkas.	resin, handmade	Shopify-lite, DM automation	Confirm WhatsApp in bio.
Aashu’s Pearl Creation	aashus_pearl_creation	Unknown	Unknown	India	Maharashtrian traditional pearl jewellery	DM to order	No	—	7	Indexed reel explicitly asks to DM for order.	marathi jewellery, DM	WA migration, automation	
Chettinad Creations	chettinad_creations	Unknown	Unknown	India	Temple / film-inspired necklace	DM (verify)	No	—	6	Indexed post shows pricing; contact method not in snippet.	temple, offer price	DM automation	Validate contact channel on profile.
Resin Gifts by Anjali (Ahmedabad)	resin_gifts_by_anjalii_	Unknown	Ahmedabad	Gujarat	Resin keepsakes / jewellery-adjacent	DM/custom (verify)	No	—	6	Resin artist in Ahmedabad; confirm jewellery SKU mix.	resin, customised	WA, ecommerce	Ahmedabad location from indexed bio text.
Wholesale Kundan Jewellery	wholesalekundanjewelery	Unknown	Unknown	India	Kundan / polki sets	DM (verify WhatsApp)	No	—	6	Indexed polki/kundan content; contact not in snippet.	kundan, polki	catalog microsite	Validate contact on profile.
TreasureBox Jewellery	treasureboxforyou	+91 9326293745	Mumbai	Maharashtra	Kolhapuri saaj combos	DM or WhatsApp	No	—	9	Indexed post shows DM/WhatsApp for combo set details.	kolhapuri saaj, bridal	CRM, WA automation	
Sai Jewellers Rajat (Ujjain)	sai_jewellers_rajat_ujjain	+91 7024274632	Ujjain	Madhya Pradesh	1g gold plated chains/necklaces	WhatsApp + DM	No	—	9	Multiple indexed posts/comments show WhatsApp/DM ordering.	1 gram gold, DM	WhatsApp automation, ecommerce	
Maya Venba Boutique (Kundan bangles)	mayavenbaboutique	+91 8637452661	Pondicherry (Pondy tags)	Puducherry	Handmade kundan / silk-thread bangles	DM/WhatsApp	No	—	9	Indexed post shows DM/WhatsApp for customization.	kundan bangles, customised	WA flows, ecommerce	
Samskruthi Jewellers	samskruthijewellers	+91 8790112233	Unknown	India	925 silver + bridal layering	WhatsApp	No	—	9	Multiple reels instruct WhatsApp ordering.	925 silver, pearls	CRM, international shipping ops	
Satya Jewels	satyajewelsofficial	+91 9999155985	Unknown	India	Temple gold jewellery (wholesale tone)	Call/WhatsApp	No	—	6	Indexed reel uses call; treat as phone-first SMB.	temple gold, wholesale	WA Business, IVR-lite	Verify whether enterprise wholesale; may still be serviceable.
VYRA Gold / Vijayakrishna	vyra_gold	+91 9995901152	Unknown	Kerala / multi-city (verify)	916 hallmark gold	WhatsApp	No	—	6	Indexed reel shows WhatsApp for naghas necklace; showroom brand signals—confirm SMB fit.	naghas, temple	WA automation, CRM	May be mid-size retail; validate before positioning as micro-SMB.
Vari Artificial Jewellery	vari_artificials_jewellery	+91 8769988299	Unknown	India	Temple bangles (gold-tone)	DM or call/WhatsApp	No	—	8	Indexed post lists two numbers; primary used here—verify second line not a different department.	temple jewellery, local delivery	WA, hyperlocal ads	Dedup: do not also store second number as separate lead without verification.
Mohinder Lal Saraf (MLS Silver)	silverjewellery.mls	Unknown	Unknown	India	925 silver kada (men’s)	DM for order	No	—	7	Indexed reel states DM for order; no COD.	silver kada, DM	WA conversion, payments	
Kadai Theru (Mahalaxmi Adyar feature)	kadaitheru_official	+91 9283916916	Chennai	Tamil Nadu	Gold jimikki / wedding gold	Call / online order	No	—	6	Indexed reel shows call number for gold merchant feature.	jimikki, wedding gold	Lead routing, WA	Primarily features another merchant; validate relationship.
Sri Bhagyalakshmi Pearls	sribhagyalakshmi_pearls	+91 9059432265	Hyderabad (pearls context)	Telangana	Pearl chains / pearl jewellery	WhatsApp numbers in posts	No	—	7	Indexed post lists two numbers; one captured—verify uniqueness policy internally.	pearls, chain	WA catalog, ecommerce	Second number from same post omitted intentionally; confirm active line.
BJ Imitation Ahmedabad	bj_imitation_ahmedabad	Unknown	Ahmedabad	Gujarat	Men’s AD rings (brass)	DM (verify)	No	—	6	Indexed reel focuses on product; contact not in snippet.	men rings, brass	Instagram DM automation	
Stylika (Ahmedabad oxidised)	stylika_	Unknown	Ahmedabad	Gujarat	Oxidised / Navratri earrings	In-store discovery + DM (verify)	No	—	6	Reel positions hidden gem shop; contact not in snippet.	oxidised, navratri	local SEO, WA	
Jewellry Junction (Nagpur)	jewellryjunction	+91 9730162779	Nagpur	Maharashtra	Imitation jewellery retail	Call / DM (verify)	No	—	7	Indexed reel tags shop location and phone.	imitation, Nagpur	GMB optimization, WA	
Wear N Shine	wear_nd_shine_jewelry	Unknown	Unknown	India	Fashion jewellery	DM (verify)	No	—	6	Search snippet referenced account via related posts; needs profile confirmation.	fashion, DM	CRM, DM tools	
KPR Jewellery	kpr_jewellery	Unknown	Unknown	India	Unknown category (verify)	DM (verify)	No	—	5	SERP referenced account; minimal evidence in snippet—validate.	unknown	research-first outreach	Low confidence; confirm jewellery focus before selling services.
Silver Palace 45	silver_palace45	Unknown	Unknown	India	Silver jewellery (assumed)	DM (verify)	No	—	5	SERP referenced account; validate contact.	silver	DM automation	Low confidence; confirm.
Because It’s Silver (Hyderabad silver)	bcos_its_silver	Unknown	Hyderabad	Telangana	Pure silver guttapusalu etc.	DM/call (verify)	No	—	7	Indexed posts around Hyderabad pearls/silver; contact not in snippet.	guttapusalu, pearls	Portfolio site, WA	
Those Little Bling	thoselittleblinggss	Unknown	Unknown	India	German silver + moissanite	DM to order	No	—	8	Multiple indexed posts: DM to order for sets/studs.	german silver, moissanite	WA migration, ecommerce	
Dreams Jewellery 2023	dreams.jewellery2023	+91 9099003670	Unknown	India	One-gram gold plated	WhatsApp for pricing	No	—	8	Indexed posts show WhatsApp numbers for price details.	one gram, screenshot policy	WA automation, policy pages	Alternate line 9106503944 appears in some posts for same business—do not duplicate.
Dreams Jewellery & Gifts	dreamsjewelleryandgifts	Unknown	Unknown	India	Jewellery / gifts mix (verify)	DM (verify)	No	—	6	Appears related ecosystem; validate phone separately.	gifts, reels	research outreach	Confirm not duplicate of dreams.jewellery2023 operationally.
Jai Jagdambey Jewellers Ludhiana	jagdambey_jeweller_ludhiana	Unknown	Ludhiana	Punjab	Silver/gold reels (verify)	DM (verify)	No	—	6	Indexed reel shows Ludhiana-tagged gold/silver content; contact not in snippet.	Punjab tags, reels	local growth	
Jai Ambe Jewellers Ramnagar	jaiambejewellers_	+91 9866868871	Ramnagar	Uttarakhand	916 gold rings	DM + call/WhatsApp	No	—	7	Indexed post lists two phone lines; primary captured.	916 gold, DM	CRM, WA	
Roshi Collections	roshi.collections	+91 9092327836	Tamil Nadu (TN shipping focus)	Tamil Nadu	One-gram forming jewellery	WhatsApp screenshot orders	No	—	9	Strong WhatsApp-first ordering with strict policies in indexed posts.	forming gold, TN	WA automation, policy UX	
Naksh Jewels Kochi (_nakshjewels_)	_nakshjewels_	Unknown	Kochi	Kerala	Silver diamond jewellery (feature)	DM (verify)	No	—	6	Featured in local reel; validate direct seller handle vs press feature.	silver diamond	local PR, WA	
The Madras Art Studio	themadras_artstudio	Unknown	Chennai	Tamil Nadu	Resin jewellery	DM to order	No	—	8	Indexed post: DM to order; custom colours.	resin, DM	custom order software	
Sri Krishna Gold Mysuru	sri_krishnagold	+91 9741119406	Mysuru	Karnataka	Gold chains / mangalya	WhatsApp	No	—	7	Indexed reel shows WhatsApp for chain bookings.	gold chains, mangalya	appointment booking	
Vijay Gold Palace Mysuru	vijaygold1	+91 8904628627	Mysuru	Karnataka	916 antique necklaces	WhatsApp	No	—	7	Indexed post shows WhatsApp for details.	antique necklace, temple	GMB + WA	
Kanika Rana Fine Jewellery	kanika_rana_fine_jewellery	+91 7861944277	Unknown	India	Silver/gold plated statement sets	wa.me link + DM	No	—	8	Indexed post shows wa.me link for contact.	moissanite, swarovski	WA deep-linking, ecommerce	wa.me treated as WhatsApp channel, not a full ecommerce site.
Shiv Shakti Jewellers 1994	shiv_shakti_jewellers_1994	+91 9815548137	Rajpura	Punjab	Gold / diamond rings	Call/WhatsApp	No	—	6	Indexed reel shows phone numbers; higher ticket SMB.	diamond rings	CRM	
Shiva Jewellers Warangal	shiva_jewellerss	+91 9908045305	Warangal	Telangana	Black beads / budget jewellery	WhatsApp	No	—	8	Indexed reel shows store address + WhatsApp.	black beads, offers	local + WA	
Silver Store Mata Payals	silver_store_matapayals	Unknown	Unknown	India	925 silver anklets	DM (verify)	No	—	6	Product posts; contact not in snippet in search hit.	silver anklets	WA	
Beautiful Creations 0365	beautiful_creations0365	+91 9911283949	Unknown	India	Moissanite / kundan bangles	DM or WhatsApp	No	—	8	Indexed booking flow via WhatsApp with strict policies.	moissanite, kundan	payments UX, WA	
Sujatha Gold Covering Works	sujatha_gold_covering_works	+91 7382222208	Machilipatnam	Andhra Pradesh	Moissanite / micro gold plated	WhatsApp bookings	No	—	8	Indexed reels list multiple lines; one primary captured—verify operational numbers.	moissanite, COD	WA automation, inventory	Other numbers may route to same desk—confirm to avoid duplicate outreach.
Glam Sakhi Jewellery	glamsakhi_jewellery	Unknown	Unknown	India	Kundan chandbali	DM to buy	No	—	7	Indexed reel says DM to buy.	chandbali, kundan	DM automation	
Fashion Darbar Hub	fashion_darbar_hub_	+91 8829911024	Unknown	India	Fashion / couple bracelets	WhatsApp screenshot + COD	No	—	8	Indexed post shows screenshot-to-WhatsApp ordering with COD.	couple bracelets, COD	WA flows	
Swarnam Varnam	swarnam_varnam	Unknown	Unknown	India	Jewellery (verify)	DM (verify)	No	—	5	SERP referenced via related posts; needs validation.	unknown	research	
""".strip()

EXTRA_PATH = pathlib.Path("/workspace/data/extra_jewellery_leads.tsv")


def parse_tsv_line(line: str, *, src: str, lineno: int) -> list[str]:
    line = line.strip()
    if not line:
        raise ValueError(f"empty line {src}:{lineno}")
    parts = line.split("\t", 13)
    if len(parts) == 13:
        parts.append("")
    if len(parts) != 14:
        raise SystemExit(f"{src} line {lineno}: expected 13–14 tab-separated fields, got {len(parts)}: {line[:120]!r}")
    return parts


def load_rows() -> list[list[str]]:
    merged: list[list[str]] = []
    seen_handles: set[str] = set()
    seen_phones: set[str] = set()

    def ingest_line(line: str, src: str, lineno: int) -> None:
        parts = parse_tsv_line(line, src=src, lineno=lineno)
        handle = parts[1].strip().lower().lstrip("@")
        if not handle:
            raise SystemExit(f"{src}:{lineno}: missing handle")
        if handle in seen_handles:
            raise SystemExit(f"Duplicate Instagram handle @{handle} ({src} line {lineno})")
        seen_handles.add(handle)

        phone = parts[2].strip()
        if phone and phone not in {"Unknown", "—"}:
            digits = "".join(ch for ch in phone if ch.isdigit())
            if len(digits) >= 10:
                if digits in seen_phones:
                    raise SystemExit(f"Duplicate phone digits {digits} for @{handle} ({src} line {lineno})")
                seen_phones.add(digits)

        merged.append(parts)

    for i, line in enumerate(RAW.splitlines(), start=1):
        if line.strip():
            ingest_line(line, "RAW", i)

    if EXTRA_PATH.is_file():
        for i, line in enumerate(EXTRA_PATH.read_text(encoding="utf-8").splitlines(), start=1):
            if line.strip():
                ingest_line(line, str(EXTRA_PATH), i)
    else:
        raise SystemExit(f"Missing extra seed file: {EXTRA_PATH}")

    if len(merged) != 100:
        raise SystemExit(f"Expected 100 unique leads after merge, got {len(merged)}")
    return merged


def main() -> None:
    rows = load_rows()

    out: list[str] = []
    out.append("INDIA JEWELLERY — INSTAGRAM / WHATSAPP LEAD EXPORT")
    out.append("Generated by automation: web-index discovery + dedupe rules (unique handle; unique WhatsApp when present).")
    out.append("IMPORTANT: Follower counts, bios, and last-post dates were NOT scraped because Instagram blocks unauthenticated fetches.")
    out.append("")

    for idx, parts in enumerate(rows, start=1):
        (
            biz,
            handle,
            phone,
            city,
            state,
            btype,
            ordering,
            web_yn,
            web_url,
            score,
            reason,
            keywords,
            services,
            notes,
        ) = parts

        handle_clean = handle.strip()
        ig = f"https://www.instagram.com/{handle_clean.strip('@')}/"

        block = f"""
{'=' * 50}
LEAD #{idx}
{'=' * 50}
Business Name: {biz}
Instagram: @{handle_clean.strip('@')}
Instagram URL: {ig}
Followers Count: Not scraped (Instagram login wall)
City: {city}
State: {state}
Business Type: {btype}
WhatsApp Number: {phone}
Email: Unknown
Ordering Method: {ordering}
Website Present: {web_yn}
Website URL: {web_url}
Recent Activity Date: Not verified in automation session
Average Engagement: Unknown
Bio Text: Not scraped (requires authenticated Instagram view)
Keywords: {keywords}
Reason Qualified: {reason}
Potential Services Needed: {services}
Google Maps Link: Unknown (search GMB unless address is explicit in notes)
Lead Quality Score: {score}
Notes: {notes}
""".strip()
        out.append(textwrap.dedent(block).strip())
        out.append("")

    path = pathlib.Path("/workspace/india_jewellery_instagram_leads.txt")
    path.write_text("\n".join(out).strip() + "\n", encoding="utf-8")
    print(f"Wrote {path} ({len(rows)} leads)")


if __name__ == "__main__":
    main()
