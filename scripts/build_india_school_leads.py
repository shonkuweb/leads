#!/usr/bin/env python3
"""Build and export India private-school leads (weak digital presence focus)."""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from website_checker import check_website, is_domain_email, is_generic_email, normalize_url

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
MASTER_PATH = DATA_DIR / "master_school_leads.json"

# Curated from public search snippets — verify before outreach.
CURATED_LEADS: list[dict] = [
    {
        "school_name": "Crystal International School",
        "year_established": "2024",
        "board": "CBSE (proposed)",
        "school_type": "CBSE English medium (proposed)",
        "address": "Lunawada, Gujarat",
        "area": "Lunawada",
        "city": "Lunawada",
        "district": "Mahisagar",
        "state": "Gujarat",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "https://www.instagram.com/crystalschoollunawada/",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Crystal+International+School+Lunawada",
        "justdial": "",
        "sulekha": "",
        "source": "instagram",
        "discovery_query": "proposed CBSE school instagram admissions",
        "notes": "Proposed CBSE; admissions 2024-25 promoted on Instagram; no official site found in public index.",
    },
    {
        "school_name": "Fun & Learn Day School",
        "year_established": "2020",
        "board": "State/Govt registered (English medium)",
        "school_type": "Primary / play group chain",
        "address": "Hridaypur, Barasat",
        "area": "Hridaypur",
        "city": "Barasat",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "pincode": "Unknown",
        "phone": "+919123798656",
        "whatsapp": "+919123798656",
        "email": "fun.learn.barasat@gmail.com",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://funlearnbarasat.in/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Fun+Learn+Day+School+Barasat",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "play school West Bengal gmail admissions",
        "notes": "Govt registered WB school; Gmail contact; admissions 2025-26 open.",
    },
    {
        "school_name": "Greenfield Kids Excellent Play School",
        "year_established": "2022",
        "board": "Preschool",
        "school_type": "Play school / kindergarten",
        "address": "Near Purbayan, Lalkuthi, Rajarhat Narayanpur",
        "area": "Rajarhat",
        "city": "Kolkata",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "pincode": "700135",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Greenfield+Kids+Excellent+Play+School+Rajarhat",
        "justdial": "https://www.justdial.com/Kolkata/Greenfield-Kids-Excellent-Play-School-Near-Purbayan-Lalkuthi-Rajarhat-Narayanpur-Rajarhat/033PXX33-XX33-220521095401-I8L5_BZDET",
        "sulekha": "",
        "source": "justdial",
        "discovery_query": "justdial play school West Bengal WhatsApp",
        "notes": "JustDial listing shows Visit Website CTA but merchant website not confirmed; WhatsApp enquiry on JD.",
    },
    {
        "school_name": "Sanjivani World School",
        "year_established": "2022",
        "board": "CBSE / State",
        "school_type": "Private day/boarding",
        "address": "C Block, Gom Defence Colony, Urmila Marg, Hanuman Nagar, Vaishali Nagar",
        "area": "Vaishali Nagar",
        "city": "Jaipur",
        "district": "Jaipur",
        "state": "Rajasthan",
        "pincode": "302021",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Sanjivani+World+School+Jaipur",
        "justdial": "https://www.justdial.com/Jaipur/Sanjivani-World-School-Vaishali-Nagar-Hanuman-Nagar/0141PX141-X141-220609222410-I5I9_BZDET",
        "sulekha": "",
        "source": "justdial",
        "discovery_query": "justdial CBSE school Rajasthan Add Website",
        "notes": "JustDial shows Add Website — weak owned web presence; CBSE+State board.",
    },
    {
        "school_name": "Tiny Hug Play School",
        "year_established": "2024",
        "board": "Preschool",
        "school_type": "Play school",
        "address": "Gerugambakkam, Chennai",
        "area": "Gerugambakkam",
        "city": "Chennai",
        "district": "Chengalpattu",
        "state": "Tamil Nadu",
        "pincode": "Unknown",
        "phone": "+919940209198",
        "whatsapp": "+916382877619",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "https://www.instagram.com/tinyhugpreschool/",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Tiny+Hug+Play+School+Gerugambakkam",
        "justdial": "",
        "sulekha": "",
        "source": "instagram",
        "discovery_query": "site:instagram.com playschool admissions Chennai",
        "notes": "Instagram-first admissions 2025-26; dual mobile contacts in caption.",
    },
    {
        "school_name": "Teddy Kids Pre School (Teddy Smart Kids)",
        "year_established": "Unknown",
        "board": "Private (Class 1-8)",
        "school_type": "Pre primary + primary",
        "address": "Unknown (verify from Instagram bio)",
        "area": "Unknown",
        "city": "Unknown",
        "district": "Unknown",
        "state": "India",
        "pincode": "Unknown",
        "phone": "+919753132132",
        "whatsapp": "+919753132132",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "https://www.instagram.com/teddykidspreschool/",
        "facebook": "",
        "linkedin": "",
        "google_maps": "",
        "justdial": "",
        "sulekha": "",
        "source": "instagram",
        "discovery_query": "site:instagram.com Teddy Kids school admission",
        "notes": "Classes 1-8 admission reel; confirm city/state from profile bio.",
    },
    {
        "school_name": "Sandipani Academy",
        "year_established": "Unknown",
        "board": "Unknown",
        "school_type": "Private school",
        "address": "Achhoti, Durg",
        "area": "Achhoti",
        "city": "Durg",
        "district": "Durg",
        "state": "Chhattisgarh",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "https://www.instagram.com/sandipani.socialmedia/",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Sandipani+Academy+Achhoti+Durg",
        "justdial": "",
        "sulekha": "",
        "source": "instagram",
        "discovery_query": "Sandipani Academy admissions instagram",
        "notes": "Session 2024-25 admission post on Instagram hub account.",
    },
    {
        "school_name": "Pt. Deendayal Upadhyay Public School",
        "year_established": "Unknown",
        "board": "Unknown",
        "school_type": "Private school",
        "address": "Firozabad, Uttar Pradesh",
        "area": "Firozabad",
        "city": "Firozabad",
        "district": "Firozabad",
        "state": "Uttar Pradesh",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "https://www.facebook.com/pdupschool/",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Pt+Deendayal+Upadhyay+Public+School+Firozabad",
        "justdial": "",
        "sulekha": "",
        "source": "facebook",
        "discovery_query": "site:facebook.com school admissions Uttar Pradesh",
        "notes": "Facebook Messenger primary CTA; admissions 2025-26.",
    },
    {
        "school_name": "Mindstein Montessori & Activity Center",
        "year_established": "Unknown",
        "board": "Montessori",
        "school_type": "Montessori preschool",
        "address": "Adelmar House, 16th Cross, Khar West, Mumbai",
        "area": "Khar West",
        "city": "Mumbai",
        "district": "Mumbai Suburban",
        "state": "Maharashtra",
        "pincode": "400052",
        "phone": "+919819658790",
        "whatsapp": "Unknown",
        "email": "mindstein.edu@gmail.com",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://www.mindsteinmontessori.in/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Mindstein+Montessori+Khar",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "montessori school gmail.com admissions India",
        "notes": "Generic Gmail for admissions; website present but Gmail indicates weak email branding.",
    },
    {
        "school_name": "Komal Play School",
        "year_established": "2009",
        "board": "Preschool",
        "school_type": "Play school",
        "address": "Naharkanta, Bhubaneswar",
        "area": "Naharkanta",
        "city": "Bhubaneswar",
        "district": "Khordha",
        "state": "Odisha",
        "pincode": "Unknown",
        "phone": "+917008431800",
        "whatsapp": "Unknown",
        "email": "kpsbbsr2009@gmail.com",
        "principal_name": "Unknown (Chairman cum Principal per site)",
        "director_name": "Unknown",
        "website": "https://komalplayschool.com/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Komal+Play+School+Bhubaneswar",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "play school Odisha gmail admissions",
        "notes": "Gmail contact on website; tier-2 city preschool.",
    },
    {
        "school_name": "Merry Babes Play School",
        "year_established": "2005",
        "board": "Preschool",
        "school_type": "Play school",
        "address": "Adarsh Vihar, KIIT Square, Patia, Bhubaneswar",
        "area": "Patia",
        "city": "Bhubaneswar",
        "district": "Khordha",
        "state": "Odisha",
        "pincode": "Unknown",
        "phone": "+9198765432310",
        "whatsapp": "Unknown",
        "email": "merrybabes@gmail.com",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://merrybabesschool.com/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Merry+Babes+Play+School+Patia",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "play school Bhubaneswar gmail",
        "notes": "Gmail on site; multi-campus group but local SMB digital stack.",
    },
    {
        "school_name": "Chhatrapati Shivaji Maharaj International School",
        "year_established": "2024",
        "board": "CBSE",
        "school_type": "International / CBSE",
        "address": "Shivaji Nagar, Ghatkopar Mankhurd Link Road, Govandi West",
        "area": "Govandi West",
        "city": "Mumbai",
        "district": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400043",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Chhatrapati+Shivaji+Maharaj+International+School+Govandi",
        "justdial": "https://www.justdial.com/Mumbai/Chhatrapati-Shivaji-Maharaj-International-School-Govandi-West/022PXX22-XX22-240111152034-M7L7_BZDET",
        "sulekha": "",
        "source": "justdial",
        "discovery_query": "justdial CBSE school Maharashtra 2024",
        "notes": "JustDial listing ID suggests 2024 listing; verify standalone website health.",
    },
    {
        "school_name": "Indo British Global School Chikkabanavara",
        "year_established": "2025",
        "board": "CBSE (proposed)",
        "school_type": "CBSE English medium",
        "address": "Survey No. 3, H.M.R Nagar, Medaralli, Chikkabanavara",
        "area": "Chikkabanavara",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560090",
        "phone": "+919104419104",
        "whatsapp": "Unknown",
        "email": "enquiry@indo-british.com",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://indo-british.com/ibgs-chikkabanavara/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Indo+British+Global+School+Chikkabanavara",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "proposed CBSE school launched 2025 India",
        "notes": "Launched mid-2025; proposed CBSE; expanding grades — greenfield digital opportunity.",
    },
    {
        "school_name": "Indo British Global School Pawdewadi",
        "year_established": "2025",
        "board": "CBSE (proposed)",
        "school_type": "CBSE English medium",
        "address": "Purna road, Guruji Chowk, Pawdewadi, Nanded",
        "area": "Pawdewadi",
        "city": "Nanded",
        "district": "Nanded",
        "state": "Maharashtra",
        "pincode": "431605",
        "phone": "+919104419104",
        "whatsapp": "Unknown",
        "email": "enquiry@indo-british.com",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://indo-british.com/ibgs-pawdewadi/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Indo+British+Global+School+Nanded",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "proposed CBSE Nanded school",
        "notes": "Tier-2/3 city new campus; shared enquiry line with group.",
    },
    {
        "school_name": "JMK Pre School",
        "year_established": "2024",
        "board": "Preschool",
        "school_type": "Play school",
        "address": "Abrol Nagar, Near Punjab Mahal Palace, Pathankot",
        "area": "Abrol Nagar",
        "city": "Pathankot",
        "district": "Pathankot",
        "state": "Punjab",
        "pincode": "Unknown",
        "phone": "+919357896882",
        "whatsapp": "+919465781783",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "https://www.instagram.com/p/C1GYEN-vx0Y/",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/JMK+Pre+School+Pathankot",
        "justdial": "",
        "sulekha": "",
        "source": "instagram",
        "discovery_query": "play school WhatsApp India instagram",
        "notes": "Instagram post with dual phone lines; no website in snippet.",
    },
    {
        "school_name": "Autumn Leaves Preschool (Ullal)",
        "year_established": "Unknown",
        "board": "Preschool",
        "school_type": "Montessori / preschool",
        "address": "Ullal, Bengaluru",
        "area": "Ullal",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "https://www.instagram.com/autumnleavesullal/",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Autumn+Leaves+Preschool+Ullal",
        "justdial": "",
        "sulekha": "",
        "source": "instagram",
        "discovery_query": "site:instagram.com preschool admissions 2025-26",
        "notes": "Active 2025-26 admission reels; verify website in bio.",
    },
    {
        "school_name": "The New Tulip International School",
        "year_established": "Unknown",
        "board": "CBSE",
        "school_type": "CBSE international",
        "address": "Sterling City, Bopal, Ahmedabad",
        "area": "Bopal",
        "city": "Ahmedabad",
        "district": "Ahmedabad",
        "state": "Gujarat",
        "pincode": "380058",
        "phone": "+917819069210",
        "whatsapp": "Unknown",
        "email": "info@thenentlinitinalchb",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "https://www.facebook.com/Thetulipschool/",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/New+Tulip+International+School+Bopal+Ahmedabad",
        "justdial": "",
        "sulekha": "",
        "source": "facebook",
        "discovery_query": "site:facebook.com CBSE admissions open",
        "notes": "Facebook-first admission creative; email typo in graphic — verify domain.",
    },
    {
        "school_name": "GD Goenka Public School Bhagalpur",
        "year_established": "Unknown",
        "board": "CBSE",
        "school_type": "Private CBSE",
        "address": "Bishunpur Jichho, Bhagalpur",
        "area": "Bhagalpur",
        "city": "Bhagalpur",
        "district": "Bhagalpur",
        "state": "Bihar",
        "pincode": "812002",
        "phone": "+917672800010",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://gdgoenkabhagalpur.com/",
        "instagram": "",
        "facebook": "https://www.facebook.com/GDGoenkaBhagalpur/",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/GD+Goenka+Bhagalpur",
        "justdial": "",
        "sulekha": "",
        "source": "facebook",
        "discovery_query": "site:facebook.com school admissions Bihar",
        "notes": "Hybrid FB + website; Bihar priority state.",
    },
    {
        "school_name": "Nand English High School",
        "year_established": "Unknown",
        "board": "SEBA",
        "school_type": "English medium",
        "address": "No.2 Birkuchi, Guwahati",
        "area": "Birkuchi",
        "city": "Guwahati",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "pincode": "781026",
        "phone": "+919864111154",
        "whatsapp": "Unknown",
        "email": "info@nandhighschool.in",
        "principal_name": "Unknown (30+ yrs exp cited)",
        "director_name": "Unknown",
        "website": "https://nandhighschool.in/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Nand+English+High+School+Birkuchi",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "English medium school Assam admissions",
        "notes": "Assam tier-2 area; active 2026-27 admission push.",
    },
    {
        "school_name": "JTS English Medium School",
        "year_established": "Unknown",
        "board": "CBSE pattern",
        "school_type": "English medium K-12",
        "address": "North Raipur Part 3, Bisondai, Golakganj, Dhubri",
        "area": "Golakganj",
        "city": "Dhubri",
        "district": "Dhubri",
        "state": "Assam",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://www.jtsemschool.in/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/JTS+English+Medium+School+Dhubri",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "English medium school Assam semi-urban",
        "notes": "Semi-urban Assam; mentions WhatsApp parent groups on site.",
    },
    {
        "school_name": "Tree House Play Group Lewis Road",
        "year_established": "Unknown",
        "board": "Preschool",
        "school_type": "Play group franchise unit",
        "address": "2132/5037 Nageswar Tangi, Lewis Road, Bhubaneswar",
        "area": "Nageswar Tangi",
        "city": "Bhubaneswar",
        "district": "Khordha",
        "state": "Odisha",
        "pincode": "751002",
        "phone": "+917682816362",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Tree+House+Play+Group+Lewis+Road+Bhubaneswar",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "play school Bhubaneswar contact",
        "notes": "Directory listing only; franchise unit may lack dedicated site.",
    },
    {
        "school_name": "Firstcry Intellitots Preschool Bangur Avenue",
        "year_established": "2023",
        "board": "Preschool",
        "school_type": "Play school chain unit",
        "address": "Plot 270, Block-B, Bangur Avenue, Kolkata",
        "area": "Bangur Avenue",
        "city": "Kolkata",
        "district": "Kolkata",
        "state": "West Bengal",
        "pincode": "700055",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Firstcry+Intellitots+Bangur+Avenue",
        "justdial": "https://www.justdial.com/Kolkata/Firstcry-Intellitots-Preschool-Bangur-Avenue/033PXX33-XX33-230523115801-R9X1_BZDET",
        "sulekha": "",
        "source": "justdial",
        "discovery_query": "justdial play school Kolkata WhatsApp",
        "notes": "JD listing May 2023; WhatsApp enquiry; Visit Website on JD — verify owned site.",
    },
    {
        "school_name": "Bachpan Play School Baguiati",
        "year_established": "2023",
        "board": "Preschool",
        "school_type": "Play school chain unit",
        "address": "P-2 VIP Road, Deshbandhu Nagar, Baguiati",
        "area": "Baguiati",
        "city": "Kolkata",
        "district": "Kolkata",
        "state": "West Bengal",
        "pincode": "700059",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Bachpan+Play+School+Baguiati",
        "justdial": "https://www.justdial.com/Kolkata/Bachpan-Play-School-Deshbandhu-Nagar-Near-VIP-Enclave-Baguiati/033PXX33-XX33-230217173132-T6L3_BZDET",
        "sulekha": "",
        "source": "justdial",
        "discovery_query": "justdial play school West Bengal",
        "notes": "Feb 2023 JustDial listing; WhatsApp on JD.",
    },
    {
        "school_name": "Little Millennium Preschool Magarpatta",
        "year_established": "Unknown",
        "board": "Preschool",
        "school_type": "Preschool chain",
        "address": "Bungalow 14 & 17, Mulberry Gardens 2, Magarpatta City, Pune",
        "area": "Magarpatta",
        "city": "Pune",
        "district": "Pune",
        "state": "Maharashtra",
        "pincode": "411013",
        "phone": "+919604647727",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "https://www.instagram.com/littlemillenniummagarpatta/",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://maps.app.goo.gl/WgWbA5haeeRAwfj18",
        "justdial": "",
        "sulekha": "",
        "source": "instagram",
        "discovery_query": "site:instagram.com preschool admissions Pune",
        "notes": "Instagram + Google Maps link; admissions 2025-26.",
    },
    {
        "school_name": "Abhinav CBSE School Manjari",
        "year_established": "Unknown",
        "board": "CBSE",
        "school_type": "CBSE Sr Sec",
        "address": "Sr.No.659-660, Manjari, Theur Rd, Tal Haveli",
        "area": "Manjari",
        "city": "Pune",
        "district": "Pune",
        "state": "Maharashtra",
        "pincode": "412110",
        "phone": "+919067546711",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://abhinavcbseschool.com/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Abhinav+CBSE+School+Manjari",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "CBSE school admissions 2026-27 Maharashtra",
        "notes": "Admissions 2026-27; verify site quality/SSL.",
    },
    {
        "school_name": "Serdihun English School",
        "year_established": "2007",
        "board": "State/Primary",
        "school_type": "Rural English medium primary",
        "address": "Hidipi, Bokajan, Karbi Anglong",
        "area": "Bokajan",
        "city": "Bokajan",
        "district": "Karbi Anglong",
        "state": "Assam",
        "pincode": "782460",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Serdihun+English+School+Bokajan",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "rural English medium school Assam",
        "notes": "Rural Assam; no website in CBSE directory data; weak digital infra.",
    },
    {
        "school_name": "Rosewood World School",
        "year_established": "Unknown",
        "board": "Unknown",
        "school_type": "Private school",
        "address": "Itki Bazar, Ratu Road, Ranchi",
        "area": "Ratu Road",
        "city": "Ranchi",
        "district": "Ranchi",
        "state": "Jharkhand",
        "pincode": "834005",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Rosewood+World+School+Ranchi",
        "justdial": "",
        "sulekha": "https://www.sulekha.com/rosewood-world-school-ratu-road-ranchi-contact-address",
        "source": "sulekha",
        "discovery_query": "sulekha private school Ranchi",
        "notes": "Sulekha listing; weak web — verify establishment year.",
    },
    {
        "school_name": "Seventh Day Adventist High School Ranchi",
        "year_established": "Unknown",
        "board": "Unknown",
        "school_type": "Private English medium",
        "address": "Bariatu Road, Ranchi",
        "area": "Bariatu",
        "city": "Ranchi",
        "district": "Ranchi",
        "state": "Jharkhand",
        "pincode": "834009",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "sdahighschoolranchi@yahoo.com",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Seventh+Day+Adventist+High+School+Ranchi",
        "justdial": "",
        "sulekha": "https://www.sulekha.com/seventh-day-adventist-high-school-ranchi-ranchi-contact-address",
        "source": "sulekha",
        "discovery_query": "sulekha school Ranchi yahoo email",
        "notes": "Yahoo mail — no domain email; Sulekha directory presence.",
    },
    {
        "school_name": "Krishna Public School Nehru Nagar Bhilai",
        "year_established": "Unknown",
        "board": "CBSE (verify)",
        "school_type": "Private school",
        "address": "Nehru Nagar, Bhilai",
        "area": "Nehru Nagar",
        "city": "Bhilai",
        "district": "Durg",
        "state": "Chhattisgarh",
        "pincode": "Unknown",
        "phone": "07882292715",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://www.krishnapublicschool.com/",
        "instagram": "",
        "facebook": "https://www.facebook.com/kpsnehrunagar/",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Krishna+Public+School+Bhilai",
        "justdial": "",
        "sulekha": "",
        "source": "facebook",
        "discovery_query": "site:facebook.com admissions open private school",
        "notes": "Facebook admissions posts with multi-line phone desk.",
    },
    {
        "school_name": "Hosannah House Montessori",
        "year_established": "Unknown",
        "board": "Montessori",
        "school_type": "Montessori preschool",
        "address": "Andheri cha Raja, Veera Desai, Andheri West, Mumbai",
        "area": "Andheri West",
        "city": "Mumbai",
        "district": "Mumbai Suburban",
        "state": "Maharashtra",
        "pincode": "Unknown",
        "phone": "+919820770352",
        "whatsapp": "Unknown",
        "email": "info@hosannahousemontessori.co.in",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://hosannahousemontessori.co.in/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Hosannah+House+Montessori+Andheri",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "montessori school admissions Mumbai 2026",
        "notes": "Phone-led admissions CTA on homepage.",
    },
    {
        "school_name": "Happy Kidz Preschool",
        "year_established": "2008",
        "board": "Preschool",
        "school_type": "Preschool",
        "address": "Bhubaneswar, Odisha",
        "area": "Unknown",
        "city": "Bhubaneswar",
        "district": "Khordha",
        "state": "Odisha",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://happykidzpreschool.com/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Happy+Kidz+Preschool+Bhubaneswar",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "preschool Bhubaneswar admissions",
        "notes": "Odisha chain unit; verify local branch contacts on site.",
    },
    {
        "school_name": "Shiksha Little Kids Pre School",
        "year_established": "Unknown",
        "board": "Preschool",
        "school_type": "Preschool",
        "address": "L7/13 ITER College Road, Khandagiri, Dumduma, Bhubaneswar",
        "area": "Khandagiri",
        "city": "Bhubaneswar",
        "district": "Khordha",
        "state": "Odisha",
        "pincode": "751019",
        "phone": "+917848885450",
        "whatsapp": "Unknown",
        "email": "info@shikshalittlekids.com",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://shikshalittlekids.com/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Shiksha+Little+Kids+Bhubaneswar",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "play school Odisha contact",
        "notes": "Domain email but SMB site — Odisha priority.",
    },
    {
        "school_name": "Singapore International School Play Kolkata",
        "year_established": "Unknown",
        "board": "International preschool",
        "school_type": "Preschool franchise",
        "address": "Kolkata",
        "area": "Unknown",
        "city": "Kolkata",
        "district": "Kolkata",
        "state": "West Bengal",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://sisplay.in/kolkata/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/SIS+Play+Kolkata",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "play school Kolkata admissions",
        "notes": "Franchise microsite; local branch may need stronger GMB/SEO.",
    },
    {
        "school_name": "Dew Drop Kindergarten School",
        "year_established": "Unknown",
        "board": "Preschool",
        "school_type": "Play school",
        "address": "Dum Dum, Kolkata",
        "area": "Dum Dum",
        "city": "Kolkata",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://www.dewdropschool.in/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Dew+Drop+Kindergarten+Dum+Dum",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "play school West Bengal admissions",
        "notes": "Legacy play school branding; admissions 2024-25 office visit model.",
    },
    {
        "school_name": "New Sainik School Bihar",
        "year_established": "2024",
        "board": "CBSE",
        "school_type": "Sainik / residential",
        "address": "Bihar",
        "area": "Unknown",
        "city": "Unknown",
        "district": "Unknown",
        "state": "Bihar",
        "pincode": "Unknown",
        "phone": "Unknown",
        "whatsapp": "Unknown",
        "email": "Unknown",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://sainikschoolbihar.com/",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/New+Sainik+School+Bihar",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "new school Bihar CBSE admissions",
        "notes": "New institution marketing site; verify MoD affiliation claims before outreach.",
    },
    {
        "school_name": "Manava Bharati International School Patna",
        "year_established": "Unknown",
        "board": "CBSE",
        "school_type": "International / CBSE",
        "address": "NH-98, Nawada More, Near AIIMS Patna",
        "area": "Gosai Math",
        "city": "Patna",
        "district": "Patna",
        "state": "Bihar",
        "pincode": "Unknown",
        "phone": "+918102450507",
        "whatsapp": "Unknown",
        "email": "admin@mbispatna.org",
        "principal_name": "Unknown",
        "director_name": "Unknown",
        "website": "https://mbispatna.org",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Manava+Bharati+International+School+Patna",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "CBSE school Patna admissions enquiry",
        "notes": "Third-party enquiry portal also indexed; dual web stack.",
    },
    {
        "school_name": "Rustomjie International School",
        "year_established": "2005",
        "board": "CBSE",
        "school_type": "CBSE private",
        "address": "Ghat No. 99/1, Mohadi Shivar, Jalgaon",
        "area": "Mohadi Shivar",
        "city": "Jalgaon",
        "district": "Jalgaon",
        "state": "Maharashtra",
        "pincode": "425002",
        "phone": "02572264892",
        "whatsapp": "Unknown",
        "email": "virafpesuna@gmail.com",
        "principal_name": "Viraf Pesuna",
        "director_name": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
        "linkedin": "",
        "google_maps": "https://www.google.com/maps/search/Rustomjie+International+School+Jalgaon",
        "justdial": "",
        "sulekha": "",
        "source": "web_search",
        "discovery_query": "CBSE school gmail principal India",
        "notes": "Principal Gmail on CBSE directory; tier-3 city — exclude if >5yr rule strict (est 2005).",
        "exclude": True,
        "exclude_reason": "Established 2005 — older than 5-year window",
    },
]

SEED_BATCH_DIR = DATA_DIR / "seed_batches"
MIN_FOLLOWERS = 300
REJECT_WEBSITE_STATUSES = {"active"}

EXPORT_FIELDS = [
    "school_name",
    "city",
    "state",
    "phone",
    "whatsapp",
    "email",
    "instagram",
    "facebook",
    "youtube",
    "followers",
    "engagement",
    "principal_name",
    "director_name",
    "google_maps",
    "website_status",
    "lead_score",
    "notes",
]

PRIORITY_STATES = {
    "West Bengal",
    "Uttar Pradesh",
    "Bihar",
    "Jharkhand",
    "Odisha",
    "Assam",
    "Maharashtra",
    "Karnataka",
    "Telangana",
    "Tamil Nadu",
    "Rajasthan",
    "Gujarat",
}


def _digits_last10(value: str | None) -> str | None:
    if not value or str(value).lower() == "unknown":
        return None
    digits = re.sub(r"\D", "", str(value))
    if len(digits) >= 10:
        return digits[-10:]
    return None


def _slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:80] or "unknown-school"


def _parse_followers(value: str | int | None) -> int | None:
    if value is None or str(value).lower() in {"", "unknown"}:
        return None
    raw = str(value).lower().replace(",", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*k", raw)
    if m:
        return int(float(m.group(1)) * 1000)
    m = re.search(r"(\d+)", raw)
    return int(m.group(1)) if m else None


def has_social_signal(lead: dict) -> bool:
    return bool(
        lead.get("instagram")
        or lead.get("facebook")
        or lead.get("youtube")
        or lead.get("justdial")
        or lead.get("sulekha")
    )


def is_qualified_lead(lead: dict) -> bool:
    """Strict rule: reject any school with a working website."""
    if lead.get("website_status") in REJECT_WEBSITE_STATUSES:
        return False
    if not has_social_signal(lead):
        return False
    followers = _parse_followers(lead.get("followers"))
    if followers is not None and followers < MIN_FOLLOWERS:
        return False
    return True


def load_seed_batches() -> list[dict]:
    leads: list[dict] = []
    if not SEED_BATCH_DIR.exists():
        return leads
    for path in sorted(SEED_BATCH_DIR.glob("batch_*.json")):
        try:
            batch = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(batch, list):
                leads.extend(batch)
        except json.JSONDecodeError:
            continue
    return leads


def filter_qualified(leads: list[dict]) -> list[dict]:
    return [l for l in leads if is_qualified_lead(l)]


def compute_lead_score(lead: dict) -> int:
    score = 3
    ws = lead.get("website_status", "no_website")
    if ws in {"no_website", "unreachable", "broken", "parked_domain", "blank_page", "facebook_redirect"}:
        score += 2
    elif ws in {"timeout", "ssl_error", "wordpress_default"}:
        score += 1

    try:
        year = int(str(lead.get("year_established", ""))[:4])
        if year >= 2021:
            score += 2
        elif year >= 2019:
            score += 1
    except ValueError:
        pass

    if lead.get("instagram") or lead.get("facebook"):
        score += 1
    if is_generic_email(lead.get("email")):
        score += 1
    if _digits_last10(lead.get("whatsapp")) or _digits_last10(lead.get("phone")):
        score += 1
    if lead.get("state") in PRIORITY_STATES:
        score += 1
    if lead.get("board", "").upper().startswith("CBSE") or "CBSE" in lead.get("board", "").upper():
        score += 1
    if lead.get("justdial") or lead.get("sulekha"):
        score += 1

    return min(score, 10)


def enrich_lead(lead: dict, check_urls: bool = True) -> dict:
    out = dict(lead)
    out.setdefault("id", _slug(out["school_name"]) + "-" + (out.get("city") or "india")[:20].lower())
    out["updated_at"] = datetime.now(timezone.utc).isoformat()

    if check_urls and out.get("website"):
        chk = check_website(out["website"])
        out["website_status"] = chk["website_status"]
        out["website_http_code"] = chk["http_code"]
        out["has_ssl"] = chk["has_ssl"]
        if chk.get("notes"):
            out["website_check_notes"] = chk["notes"]
    elif not out.get("website"):
        out["website_status"] = "no_website"
        out["website_http_code"] = None
        out["has_ssl"] = False
    else:
        out.setdefault("website_status", "unknown")

    out["uses_gmail"] = is_generic_email(out.get("email"))
    out["uses_domain_email"] = is_domain_email(out.get("email"), out.get("website"))
    out["lead_score"] = compute_lead_score(out)
    out["priority_state"] = out.get("state") in PRIORITY_STATES
    out["qualified"] = is_qualified_lead(out)
    return out


def dedupe_key(lead: dict) -> str:
    name = re.sub(r"\s+", " ", lead.get("school_name", "").lower().strip())
    city = lead.get("city", "").lower().strip()
    phone = _digits_last10(lead.get("phone")) or _digits_last10(lead.get("whatsapp")) or ""
    return f"{name}|{city}|{phone}"


def load_master() -> list[dict]:
    if MASTER_PATH.exists():
        data = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
        return data.get("leads", [])
    return []


def save_master(leads: list[dict], meta: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "meta": meta,
        "leads": leads,
    }
    MASTER_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def merge_leads(existing: list[dict], incoming: list[dict]) -> tuple[list[dict], int]:
    by_key: dict[str, dict] = {dedupe_key(l): l for l in existing}
    added = 0
    for lead in incoming:
        if lead.get("exclude"):
            continue
        key = dedupe_key(lead)
        enriched = enrich_lead(lead)
        if key in by_key:
            prev = by_key[key]
            for field, value in enriched.items():
                if value and (not prev.get(field) or prev.get(field) == "Unknown"):
                    prev[field] = value
            prev["updated_at"] = enriched["updated_at"]
            by_key[key] = enrich_lead(prev, check_urls=False)
        else:
            by_key[key] = enriched
            added += 1
    return list(by_key.values()), added


def write_exports(leads: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    qualified = filter_qualified(leads)

    # JSON API-ready
    api_path = OUTPUT_DIR / "india_school_leads.json"
    api_path.write_text(
        json.dumps(
            {
                "generated_at": now,
                "count": len(qualified),
                "rejected_active_website": len(leads) - len(qualified),
                "leads": qualified,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # CSV
    csv_path = OUTPUT_DIR / "india_school_leads.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPORT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for lead in qualified:
            row = {k: lead.get(k, "") for k in EXPORT_FIELDS}
            writer.writerow(row)

    # TXT detailed
    txt_path = OUTPUT_DIR / "india_school_leads.txt"
    lines = [
        "INDIA PRIVATE SCHOOL LEADS — NO WORKING WEBSITE + SOCIAL/DIRECTORY PRESENCE",
        f"Generated: {now}",
        f"Qualified leads: {len(qualified)} (master total: {len(leads)})",
        "Source: browser MCP + public search + JustDial (verify before outreach).",
        "",
    ]
    for i, lead in enumerate(sorted(qualified, key=lambda x: -x.get("lead_score", 0)), start=1):
        lines.append("=" * 60)
        lines.append(f"LEAD #{i} | Score: {lead.get('lead_score')}/10")
        lines.append("=" * 60)
        for k in EXPORT_FIELDS:
            lines.append(f"{k}: {lead.get(k, '')}")
        lines.append(f"board: {lead.get('board', '')}")
        lines.append(f"school_type: {lead.get('school_type', '')}")
        lines.append(f"justdial: {lead.get('justdial', '')}")
        lines.append(f"sulekha: {lead.get('sulekha', '')}")
        lines.append(f"uses_gmail: {lead.get('uses_gmail', '')}")
        lines.append(f"priority_state: {lead.get('priority_state', '')}")
        lines.append("")
    txt_path.write_text("\n".join(lines), encoding="utf-8")

    # Priority lists (qualified only)
    no_web = [l for l in qualified if l.get("website_status") == "no_website"]
    high = [l for l in qualified if l.get("lead_score", 0) >= 8]
    priority = [l for l in qualified if l.get("priority_state")]

    def _write_list(path: Path, subset: list[dict], title: str) -> None:
        body = [title, f"Count: {len(subset)}", ""]
        for l in sorted(subset, key=lambda x: -x.get("lead_score", 0)):
            body.append(
                f"- [{l.get('lead_score')}] {l.get('school_name')} | {l.get('city')}, {l.get('state')} | "
                f"Ph: {l.get('phone') or l.get('whatsapp') or '—'} | {l.get('website_status')}"
            )
        path.write_text("\n".join(body) + "\n", encoding="utf-8")

    _write_list(OUTPUT_DIR / "schools_without_websites.txt", no_web, "SCHOOLS WITHOUT WEBSITES")
    _write_list(OUTPUT_DIR / "high_conversion_prospects.txt", high, "HIGH-CONVERSION PROSPECTS (score >= 8)")
    _write_list(OUTPUT_DIR / "priority_outreach_list.txt", priority, "PRIORITY STATE OUTREACH LIST")


def main() -> None:
    existing = load_master()
    incoming = CURATED_LEADS + load_seed_batches()
    merged, added = merge_leads(existing, incoming)

    # Re-check websites: reject active sites from exports
    refreshed = [enrich_lead(l, check_urls=bool(l.get("website"))) for l in merged]
    qualified = filter_qualified(refreshed)

    meta = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "added_this_run": added,
        "total": len(refreshed),
        "qualified": len(qualified),
        "rejected_active_website": sum(1 for l in refreshed if l.get("website_status") == "active"),
        "target": 10000,
    }
    save_master(refreshed, meta)
    write_exports(refreshed)
    print(
        f"Master DB: {len(refreshed)} leads (+{added} new). "
        f"Qualified export: {len(qualified)}. Outputs in {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()
