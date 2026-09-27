"""
Smart Scheduler & Time Zone Intelligence Engine
Detects country, university time zone, and calculates optimal academic delivery
windows for PhD cold outreach, strictly avoiding Friday and weekend inbox drops.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
import zoneinfo

# Known university domain to (Country, City, Timezone) mappings
UNIVERSITY_DOMAINS = {
    # New Zealand
    "auckland.ac.nz": ("New Zealand", "Auckland", "Pacific/Auckland"),
    "otago.ac.nz": ("New Zealand", "Dunedin", "Pacific/Auckland"),
    "canterbury.ac.nz": ("New Zealand", "Christchurch", "Pacific/Auckland"),
    "vuw.ac.nz": ("New Zealand", "Wellington", "Pacific/Auckland"),
    "waikato.ac.nz": ("New Zealand", "Hamilton", "Pacific/Auckland"),
    "massey.ac.nz": ("New Zealand", "Palmerston North", "Pacific/Auckland"),
    "aut.ac.nz": ("New Zealand", "Auckland", "Pacific/Auckland"),
    "lincoln.ac.nz": ("New Zealand", "Lincoln", "Pacific/Auckland"),

    # Australia
    "unimelb.edu.au": ("Australia", "Melbourne", "Australia/Melbourne"),
    "sydney.edu.au": ("Australia", "Sydney", "Australia/Sydney"),
    "anu.edu.au": ("Australia", "Canberra", "Australia/Sydney"),
    "unsw.edu.au": ("Australia", "Sydney", "Australia/Sydney"),
    "uq.edu.au": ("Australia", "Brisbane", "Australia/Brisbane"),
    "monash.edu": ("Australia", "Melbourne", "Australia/Melbourne"),
    "uwa.edu.au": ("Australia", "Perth", "Australia/Perth"),
    "adelaide.edu.au": ("Australia", "Adelaide", "Australia/Adelaide"),
    "uts.edu.au": ("Australia", "Sydney", "Australia/Sydney"),
    "rmit.edu.au": ("Australia", "Melbourne", "Australia/Melbourne"),
    "qut.edu.au": ("Australia", "Brisbane", "Australia/Brisbane"),

    # US Pacific (UTC-8 / UTC-7)
    "stanford.edu": ("United States", "Stanford, CA", "America/Los_Angeles"),
    "berkeley.edu": ("United States", "Berkeley, CA", "America/Los_Angeles"),
    "ucla.edu": ("United States", "Los Angeles, CA", "America/Los_Angeles"),
    "washington.edu": ("United States", "Seattle, WA", "America/Los_Angeles"),
    "caltech.edu": ("United States", "Pasadena, CA", "America/Los_Angeles"),
    "ucsd.edu": ("United States", "San Diego, CA", "America/Los_Angeles"),
    "uci.edu": ("United States", "Irvine, CA", "America/Los_Angeles"),
    "ucdavis.edu": ("United States", "Davis, CA", "America/Los_Angeles"),
    "ucsb.edu": ("United States", "Santa Barbara, CA", "America/Los_Angeles"),
    "usc.edu": ("United States", "Los Angeles, CA", "America/Los_Angeles"),
    
    # US Eastern (UTC-5 / UTC-4)
    "mit.edu": ("United States", "Cambridge, MA", "America/New_York"),
    "harvard.edu": ("United States", "Cambridge, MA", "America/New_York"),
    "cmu.edu": ("United States", "Pittsburgh, PA", "America/New_York"),
    "columbia.edu": ("United States", "New York, NY", "America/New_York"),
    "princeton.edu": ("United States", "Princeton, NJ", "America/New_York"),
    "cornell.edu": ("United States", "Ithaca, NY", "America/New_York"),
    "yale.edu": ("United States", "New Haven, CT", "America/New_York"),
    "upenn.edu": ("United States", "Philadelphia, PA", "America/New_York"),
    "gatech.edu": ("United States", "Atlanta, GA", "America/New_York"),
    "jhu.edu": ("United States", "Baltimore, MD", "America/New_York"),
    "nyu.edu": ("United States", "New York, NY", "America/New_York"),
    "brown.edu": ("United States", "Providence, RI", "America/New_York"),
    "umich.edu": ("United States", "Ann Arbor, MI", "America/New_York"),
    "duke.edu": ("United States", "Durham, NC", "America/New_York"),
    "unc.edu": ("United States", "Chapel Hill, NC", "America/New_York"),
    "bu.edu": ("United States", "Boston, MA", "America/New_York"),
    "northeastern.edu": ("United States", "Boston, MA", "America/New_York"),

    # US Central (UTC-6 / UTC-5)
    "uchicago.edu": ("United States", "Chicago, IL", "America/Chicago"),
    "northwestern.edu": ("United States", "Evanston, IL", "America/Chicago"),
    "utexas.edu": ("United States", "Austin, TX", "America/Chicago"),
    "illinois.edu": ("United States", "Urbana-Champaign, IL", "America/Chicago"),
    "wisc.edu": ("United States", "Madison, WI", "America/Chicago"),
    "purdue.edu": ("United States", "West Lafayette, IN", "America/Indiana/Indianapolis"),
    "umn.edu": ("United States", "Minneapolis, MN", "America/Chicago"),
    "tamu.edu": ("United States", "College Station, TX", "America/Chicago"),
    "rice.edu": ("United States", "Houston, TX", "America/Chicago"),

    # United Kingdom (UTC+0 / UTC+1)
    "ox.ac.uk": ("United Kingdom", "Oxford", "Europe/London"),
    "cam.ac.uk": ("United Kingdom", "Cambridge", "Europe/London"),
    "imperial.ac.uk": ("United Kingdom", "London", "Europe/London"),
    "ucl.ac.uk": ("United Kingdom", "London", "Europe/London"),
    "ed.ac.uk": ("United Kingdom", "Edinburgh", "Europe/London"),
    "manchester.ac.uk": ("United Kingdom", "Manchester", "Europe/London"),
    "brunel.ac.uk": ("United Kingdom", "London", "Europe/London"),
    "kcl.ac.uk": ("United Kingdom", "London", "Europe/London"),
    "warwick.ac.uk": ("United Kingdom", "Coventry", "Europe/London"),
    "bristol.ac.uk": ("United Kingdom", "Bristol", "Europe/London"),
    "southampton.ac.uk": ("United Kingdom", "Southampton", "Europe/London"),
    "gla.ac.uk": ("United Kingdom", "Glasgow", "Europe/London"),
    "leeds.ac.uk": ("United Kingdom", "Leeds", "Europe/London"),
    "sheffield.ac.uk": ("United Kingdom", "Sheffield", "Europe/London"),
    "bham.ac.uk": ("United Kingdom", "Birmingham", "Europe/London"),
    "st-andrews.ac.uk": ("United Kingdom", "St Andrews", "Europe/London"),

    # Ireland
    "tcd.ie": ("Ireland", "Dublin", "Europe/Dublin"),
    "ucd.ie": ("Ireland", "Dublin", "Europe/Dublin"),
    "nuigalway.ie": ("Ireland", "Galway", "Europe/Dublin"),
    "ucc.ie": ("Ireland", "Cork", "Europe/Dublin"),

    # Germany / Switzerland / Central Europe (UTC+1 / UTC+2)
    "tum.de": ("Germany", "Munich", "Europe/Berlin"),
    "lmu.de": ("Germany", "Munich", "Europe/Berlin"),
    "rwth-aachen.de": ("Germany", "Aachen", "Europe/Berlin"),
    "uni-heidelberg.de": ("Germany", "Heidelberg", "Europe/Berlin"),
    "kit.edu": ("Germany", "Karlsruhe", "Europe/Berlin"),
    "tu-berlin.de": ("Germany", "Berlin", "Europe/Berlin"),
    "uni-bonn.de": ("Germany", "Bonn", "Europe/Berlin"),
    "ethz.ch": ("Switzerland", "Zurich", "Europe/Zurich"),
    "epfl.ch": ("Switzerland", "Lausanne", "Europe/Zurich"),
    "usi.ch": ("Switzerland", "Lugano", "Europe/Zurich"),
    "unige.ch": ("Switzerland", "Geneva", "Europe/Zurich"),
    "uzh.ch": ("Switzerland", "Zurich", "Europe/Zurich"),
    "unibas.ch": ("Switzerland", "Basel", "Europe/Zurich"),
    "tudelft.nl": ("Netherlands", "Delft", "Europe/Amsterdam"),
    "uva.nl": ("Netherlands", "Amsterdam", "Europe/Amsterdam"),
    "uu.nl": ("Netherlands", "Utrecht", "Europe/Amsterdam"),
    "kth.se": ("Sweden", "Stockholm", "Europe/Stockholm"),
    "lu.se": ("Sweden", "Lund", "Europe/Stockholm"),
    "uu.se": ("Sweden", "Uppsala", "Europe/Stockholm"),
    "sorbonne-universite.fr": ("France", "Paris", "Europe/Paris"),
    "polytechnique.edu": ("France", "Palaiseau", "Europe/Paris"),
    "uio.no": ("Norway", "Oslo", "Europe/Oslo"),
    "ku.dk": ("Denmark", "Copenhagen", "Europe/Copenhagen"),
    "helsinki.fi": ("Finland", "Helsinki", "Europe/Helsinki"),
    "aalto.fi": ("Finland", "Espoo", "Europe/Helsinki"),

    # Canada
    "utoronto.ca": ("Canada", "Toronto, ON", "America/Toronto"),
    "ubc.ca": ("Canada", "Vancouver, BC", "America/Vancouver"),
    "mcgill.ca": ("Canada", "Montreal, QC", "America/Toronto"),
    "uwaterloo.ca": ("Canada", "Waterloo, ON", "America/Toronto"),
    "ualberta.ca": ("Canada", "Edmonton, AB", "America/Edmonton"),
    "sfu.ca": ("Canada", "Burnaby, BC", "America/Vancouver"),

    # Asia & Middle East
    "nus.edu.sg": ("Singapore", "Singapore", "Asia/Singapore"),
    "ntu.edu.sg": ("Singapore", "Singapore", "Asia/Singapore"),
    "smu.edu.sg": ("Singapore", "Singapore", "Asia/Singapore"),
    "u-tokyo.ac.jp": ("Japan", "Tokyo", "Asia/Tokyo"),
    "kyoto-u.ac.jp": ("Japan", "Kyoto", "Asia/Tokyo"),
    "titech.ac.jp": ("Japan", "Tokyo", "Asia/Tokyo"),
    "osaka-u.ac.jp": ("Japan", "Osaka", "Asia/Tokyo"),
    "hku.hk": ("Hong Kong", "Hong Kong", "Asia/Hong_Kong"),
    "cuhk.edu.hk": ("Hong Kong", "Hong Kong", "Asia/Hong_Kong"),
    "ust.hk": ("Hong Kong", "Hong Kong", "Asia/Hong_Kong"),
    "kaist.ac.kr": ("South Korea", "Daejeon", "Asia/Seoul"),
    "snu.ac.kr": ("South Korea", "Seoul", "Asia/Seoul"),
    "tsinghua.edu.cn": ("China", "Beijing", "Asia/Shanghai"),
    "pku.edu.cn": ("China", "Beijing", "Asia/Shanghai"),
    "fudan.edu.cn": ("China", "Shanghai", "Asia/Shanghai"),
    "iisc.ac.in": ("India", "Bengaluru", "Asia/Kolkata"),
    "iitb.ac.in": ("India", "Mumbai", "Asia/Kolkata"),
    "iitd.ac.in": ("India", "New Delhi", "Asia/Kolkata"),
    "iitm.ac.in": ("India", "Chennai", "Asia/Kolkata"),
    "iitk.ac.in": ("India", "Kanpur", "Asia/Kolkata"),
    "tifr.res.in": ("India", "Mumbai", "Asia/Kolkata"),
    "tau.ac.il": ("Israel", "Tel Aviv", "Asia/Jerusalem"),
    "weizmann.ac.il": ("Israel", "Rehovot", "Asia/Jerusalem"),
}

# Country-Code Top Level Domain (ccTLD) mappings
TLD_DEFAULTS = {
    # New Zealand
    "ac.nz": ("New Zealand", "Auckland / Wellington", "Pacific/Auckland"),
    "org.nz": ("New Zealand", "New Zealand", "Pacific/Auckland"),
    "school.nz": ("New Zealand", "New Zealand", "Pacific/Auckland"),
    "govt.nz": ("New Zealand", "Wellington", "Pacific/Auckland"),
    "nz": ("New Zealand", "New Zealand", "Pacific/Auckland"),

    # Australia
    "edu.au": ("Australia", "Sydney / Melbourne", "Australia/Sydney"),
    "ac.au": ("Australia", "Australia", "Australia/Sydney"),
    "gov.au": ("Australia", "Canberra", "Australia/Sydney"),
    "au": ("Australia", "Australia (Eastern)", "Australia/Sydney"),

    # United Kingdom
    "ac.uk": ("United Kingdom", "London / Oxford", "Europe/London"),
    "gov.uk": ("United Kingdom", "United Kingdom", "Europe/London"),
    "uk": ("United Kingdom", "United Kingdom", "Europe/London"),

    # Ireland
    "edu.ie": ("Ireland", "Dublin", "Europe/Dublin"),
    "ie": ("Ireland", "Dublin", "Europe/Dublin"),

    # Canada
    "gc.ca": ("Canada", "Ottawa, ON", "America/Toronto"),
    "ca": ("Canada", "Canada (Eastern)", "America/Toronto"),

    # Europe
    "de": ("Germany", "Berlin / Munich", "Europe/Berlin"),
    "ch": ("Switzerland", "Zurich / Geneva", "Europe/Zurich"),
    "fr": ("France", "Paris", "Europe/Paris"),
    "nl": ("Netherlands", "Amsterdam / Delft", "Europe/Amsterdam"),
    "se": ("Sweden", "Stockholm", "Europe/Stockholm"),
    "dk": ("Denmark", "Copenhagen", "Europe/Copenhagen"),
    "no": ("Norway", "Oslo", "Europe/Oslo"),
    "fi": ("Finland", "Helsinki", "Europe/Helsinki"),
    "at": ("Austria", "Vienna", "Europe/Vienna"),
    "be": ("Belgium", "Brussels", "Europe/Brussels"),
    "it": ("Italy", "Rome / Milan", "Europe/Rome"),
    "es": ("Spain", "Madrid / Barcelona", "Europe/Madrid"),
    "pt": ("Portugal", "Lisbon / Porto", "Europe/Lisbon"),
    "pl": ("Poland", "Warsaw", "Europe/Warsaw"),
    "cz": ("Czech Republic", "Prague", "Europe/Prague"),
    "hu": ("Hungary", "Budapest", "Europe/Budapest"),
    "gr": ("Greece", "Athens", "Europe/Athens"),
    "ro": ("Romania", "Bucharest", "Europe/Bucharest"),
    "ru": ("Russia", "Moscow", "Europe/Moscow"),
    "tr": ("Turkey", "Istanbul / Ankara", "Europe/Istanbul"),

    # Asia & Oceania
    "edu.sg": ("Singapore", "Singapore", "Asia/Singapore"),
    "sg": ("Singapore", "Singapore", "Asia/Singapore"),
    "edu.hk": ("Hong Kong", "Hong Kong", "Asia/Hong_Kong"),
    "hk": ("Hong Kong", "Hong Kong", "Asia/Hong_Kong"),
    "ac.jp": ("Japan", "Tokyo", "Asia/Tokyo"),
    "jp": ("Japan", "Tokyo", "Asia/Tokyo"),
    "ac.kr": ("South Korea", "Seoul", "Asia/Seoul"),
    "kr": ("South Korea", "Seoul", "Asia/Seoul"),
    "edu.cn": ("China", "Beijing / Shanghai", "Asia/Shanghai"),
    "cn": ("China", "Beijing / Shanghai", "Asia/Shanghai"),
    "edu.tw": ("Taiwan", "Taipei", "Asia/Taipei"),
    "tw": ("Taiwan", "Taipei", "Asia/Taipei"),
    "ac.in": ("India", "Bengaluru / Delhi", "Asia/Kolkata"),
    "res.in": ("India", "India", "Asia/Kolkata"),
    "edu.in": ("India", "India", "Asia/Kolkata"),
    "in": ("India", "India", "Asia/Kolkata"),
    "edu.my": ("Malaysia", "Kuala Lumpur", "Asia/Kuala_Lumpur"),
    "my": ("Malaysia", "Kuala Lumpur", "Asia/Kuala_Lumpur"),
    "ac.th": ("Thailand", "Bangkok", "Asia/Bangkok"),
    "th": ("Thailand", "Bangkok", "Asia/Bangkok"),
    "ac.id": ("Indonesia", "Jakarta", "Asia/Jakarta"),
    "id": ("Indonesia", "Jakarta", "Asia/Jakarta"),
    "edu.vn": ("Vietnam", "Hanoi", "Asia/Ho_Chi_Minh"),
    "vn": ("Vietnam", "Hanoi", "Asia/Ho_Chi_Minh"),
    "edu.ph": ("Philippines", "Manila", "Asia/Manila"),
    "ph": ("Philippines", "Manila", "Asia/Manila"),

    # Middle East & Africa
    "ac.il": ("Israel", "Tel Aviv / Jerusalem", "Asia/Jerusalem"),
    "il": ("Israel", "Israel", "Asia/Jerusalem"),
    "edu.sa": ("Saudi Arabia", "Riyadh", "Asia/Riyadh"),
    "sa": ("Saudi Arabia", "Saudi Arabia", "Asia/Riyadh"),
    "ac.ae": ("United Arab Emirates", "Dubai / Abu Dhabi", "Asia/Dubai"),
    "ae": ("United Arab Emirates", "United Arab Emirates", "Asia/Dubai"),
    "ac.za": ("South Africa", "Cape Town / Johannesburg", "Africa/Johannesburg"),
    "za": ("South Africa", "South Africa", "Africa/Johannesburg"),

    # Americas
    "edu.br": ("Brazil", "Sao Paulo", "America/Sao_Paulo"),
    "br": ("Brazil", "Brazil", "America/Sao_Paulo"),
    "edu.mx": ("Mexico", "Mexico City", "America/Mexico_City"),
    "mx": ("Mexico", "Mexico", "America/Mexico_City"),
    "cl": ("Chile", "Santiago", "America/Santiago"),
    "ar": ("Argentina", "Buenos Aires", "America/Argentina/Buenos_Aires"),

    # Generic & US
    "edu": ("United States", "USA (Academic)", "America/New_York"),
    "org": ("International", "International", "UTC"),
    "com": ("International", "International", "UTC"),
    "net": ("International", "International", "UTC"),
    "io": ("International", "International", "UTC"),
}

class SmartScheduler:
    def _get_timezone_obj(self, tz_name: str):
        try:
            return zoneinfo.ZoneInfo(tz_name)
        except Exception:
            fallback_offsets = {
                "Pacific/Auckland": timedelta(hours=12),
                "Australia/Sydney": timedelta(hours=10),
                "Australia/Melbourne": timedelta(hours=10),
                "Australia/Brisbane": timedelta(hours=10),
                "Australia/Perth": timedelta(hours=8),
                "Australia/Adelaide": timedelta(hours=9, minutes=30),
                "America/Los_Angeles": timedelta(hours=-7),
                "America/New_York": timedelta(hours=-4),
                "America/Chicago": timedelta(hours=-5),
                "America/Indiana/Indianapolis": timedelta(hours=-4),
                "Europe/London": timedelta(hours=1),
                "Europe/Dublin": timedelta(hours=1),
                "Europe/Berlin": timedelta(hours=2),
                "Europe/Zurich": timedelta(hours=2),
                "Europe/Amsterdam": timedelta(hours=2),
                "Europe/Stockholm": timedelta(hours=2),
                "Europe/Paris": timedelta(hours=2),
                "America/Toronto": timedelta(hours=-4),
                "America/Vancouver": timedelta(hours=-7),
                "America/Edmonton": timedelta(hours=-6),
                "Asia/Singapore": timedelta(hours=8),
                "Asia/Hong_Kong": timedelta(hours=8),
                "Asia/Tokyo": timedelta(hours=9),
                "Asia/Seoul": timedelta(hours=9),
                "Asia/Shanghai": timedelta(hours=8),
                "Asia/Taipei": timedelta(hours=8),
                "Asia/Kolkata": timedelta(hours=5, minutes=30),
                "Asia/Jerusalem": timedelta(hours=3),
                "Asia/Dubai": timedelta(hours=4),
                "Asia/Riyadh": timedelta(hours=3),
                "Africa/Johannesburg": timedelta(hours=2),
                "UTC": timedelta(0),
            }
            offset = fallback_offsets.get(tz_name, timedelta(hours=-4))
            return timezone(offset)

    def detect_timezone(self, email: str, institution: Optional[str] = None) -> Dict[str, str]:
        """Detect country, location, and timezone from email and institution name."""
        clean_email = (email or "").strip().lower()
        domain = clean_email.split("@")[-1] if "@" in clean_email else clean_email
        full_text = f"{domain} {institution or ''}".lower()
        
        # 1. Direct university domain exact or suffix match
        for known_domain, (country, city, tz_name) in UNIVERSITY_DOMAINS.items():
            if domain == known_domain or domain.endswith("." + known_domain):
                return {
                    "country": country,
                    "city": city,
                    "timezone": tz_name,
                    "matched_by": f"Recognized institution domain ({known_domain})"
                }

        # 2. Check prominent geographic & institution keywords in domain or institution
        # New Zealand
        if any(k in full_text for k in ["auckland", "otago", "canterbury", "wellington", "waikato", "massey", "zealand"]):
            return {"country": "New Zealand", "city": "Auckland / Wellington", "timezone": "Pacific/Auckland", "matched_by": "New Zealand institution keyword"}

        # Australia
        if any(k in full_text for k in ["melbourne", "sydney", "queensland", "canberra", "monash", "adelaide", "australia"]):
            return {"country": "Australia", "city": "Sydney / Melbourne", "timezone": "Australia/Sydney", "matched_by": "Australia institution keyword"}

        # US Pacific / West
        if any(k in full_text for k in ["stanford", "berkeley", "california", "washington", "ucla", "usc", "caltech", "oregon", "ucsb", "ucsd"]):
            return {"country": "United States", "city": "US West Coast", "timezone": "America/Los_Angeles", "matched_by": "US West institution keyword"}

        # US Central
        if any(k in full_text for k in ["chicago", "northwestern", "illinois", "austin", "purdue", "wisconsin", "michigan", "minnesota", "texas"]):
            return {"country": "United States", "city": "US Central", "timezone": "America/Chicago", "matched_by": "US Central institution keyword"}

        # US East
        if any(k in full_text for k in ["harvard", "mit", "columbia", "princeton", "new york", "cmu", "cornell", "yale", "penn", "georgia tech", "gatech", "duke", "boston"]):
            return {"country": "United States", "city": "US East Coast", "timezone": "America/New_York", "matched_by": "US East institution keyword"}

        # UK
        if any(k in full_text for k in ["oxford", "cambridge", "imperial", "london", "edinburgh", "manchester", "brunel", "kcl", "warwick", "bristol", "glasgow"]):
            return {"country": "United Kingdom", "city": "United Kingdom", "timezone": "Europe/London", "matched_by": "UK institution keyword"}

        # Switzerland
        if any(k in full_text for k in ["eth", "zurich", "epfl", "lausanne", "switzerland", "geneva"]):
            return {"country": "Switzerland", "city": "Switzerland", "timezone": "Europe/Zurich", "matched_by": "Switzerland institution keyword"}

        # Germany
        if any(k in full_text for k in ["munich", "tum", "berlin", "heidelberg", "aachen", "germany", "fraunhofer", "max planck"]):
            return {"country": "Germany", "city": "Germany", "timezone": "Europe/Berlin", "matched_by": "Germany institution keyword"}

        # Canada
        if any(k in full_text for k in ["toronto", "mcgill", "waterloo", "vancouver", "canada", "alberta", "montreal"]):
            return {"country": "Canada", "city": "Canada", "timezone": "America/Toronto", "matched_by": "Canada institution keyword"}

        # Singapore
        if any(k in full_text for k in ["nus", "ntu", "singapore", "smu"]):
            return {"country": "Singapore", "city": "Singapore", "timezone": "Asia/Singapore", "matched_by": "Singapore institution keyword"}

        # Japan
        if any(k in full_text for k in ["tokyo", "kyoto", "japan", "osaka", "tohoku"]):
            return {"country": "Japan", "city": "Tokyo / Kyoto", "timezone": "Asia/Tokyo", "matched_by": "Japan institution keyword"}

        # Hong Kong
        if any(k in full_text for k in ["hong kong", "hku", "cuhk", "hkust"]):
            return {"country": "Hong Kong", "city": "Hong Kong", "timezone": "Asia/Hong_Kong", "matched_by": "Hong Kong institution keyword"}

        # 3. Match by TLD (.ac.nz, .edu.au, .ac.uk, .nz, .au, .de, etc.)
        parts = domain.split(".")
        if len(parts) >= 2:
            two_part_tld = ".".join(parts[-2:])
            if two_part_tld in TLD_DEFAULTS:
                country, city, tz_name = TLD_DEFAULTS[two_part_tld]
                return {"country": country, "city": city, "timezone": tz_name, "matched_by": f"Country TLD (.{two_part_tld})"}
            
            single_tld = parts[-1]
            if single_tld in TLD_DEFAULTS:
                country, city, tz_name = TLD_DEFAULTS[single_tld]
                return {"country": country, "city": city, "timezone": tz_name, "matched_by": f"Country TLD (.{single_tld})"}

        # 4. Fallback for .edu or unknown
        if domain.endswith(".edu"):
            return {
                "country": "United States",
                "city": "USA (Academic)",
                "timezone": "America/New_York",
                "matched_by": "Higher education TLD (.edu)"
            }

        return {
            "country": "International",
            "city": "Global",
            "timezone": "UTC",
            "matched_by": "Default international fallback"
        }

    def calculate_optimal_schedule(self, email: str, institution: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates the optimal sending time for a professor:
        - Target window: 08:30 AM - 09:30 AM in the professor's local time.
        - Preferred days: Tuesday, Wednesday, Thursday.
        - INVIOLABLE RULE: NEVER send on Friday (holiday mindset, 80%+ drop in faculty attention, weekend burying).
        - NEVER send on Saturday or Sunday.
        - Converts between Target Local Time and IST (India Standard Time).
        """
        location_info = self.detect_timezone(email, institution)
        tz_str = location_info["timezone"]
        target_tz = self._get_timezone_obj(tz_str)
        ist_tz = self._get_timezone_obj("Asia/Kolkata")

        utc_now = datetime.now(timezone.utc)
        target_now = utc_now.astimezone(target_tz)
        ist_now = utc_now.astimezone(ist_tz)

        # Calculate time difference in hours between Target and IST
        # (Target UTC offset - IST UTC offset)
        target_offset = target_now.utcoffset() or timedelta(0)
        ist_offset = ist_now.utcoffset() or timedelta(hours=5, minutes=30)
        offset_diff_seconds = (target_offset - ist_offset).total_seconds()
        diff_hours = offset_diff_seconds / 3600.0

        if diff_hours < 0:
            diff_str = f"{abs(diff_hours):.1f}h behind India"
        elif diff_hours > 0:
            diff_str = f"{diff_hours:.1f}h ahead of India"
        else:
            diff_str = "Same time as India"

        # Professor current activity state
        current_hour = target_now.hour
        if 0 <= current_hour < 7:
            activity_state = "🌙 Sleeping / Offline (Night)"
        elif 7 <= current_hour < 9:
            activity_state = "☕ Early Morning (Pre-Work Routine)"
        elif 9 <= current_hour < 12:
            activity_state = "💼 Peak Morning Desk & Inbox Time"
        elif 12 <= current_hour < 14:
            activity_state = "🥪 Lunch & Colloquium Window"
        elif 14 <= current_hour < 17:
            activity_state = "🔬 Afternoon Lab & Meetings"
        elif 17 <= current_hour < 21:
            activity_state = "🏡 Evening / Offline"
        else:
            activity_state = "🌙 Late Night / Resting"

        current_weekday = target_now.weekday() # Monday=0 ... Sunday=6

        reasoning = []
        reasoning.append(f"Destination: {location_info['country']} ({location_info['city']}) • Timezone: {tz_str}")
        reasoning.append(f"Professor is currently {diff_str} • Activity: {activity_state}")
        reasoning.append(f"Professor's local time: {target_now.strftime('%A, %I:%M %p')}")
        reasoning.append(f"Your local time in India: {ist_now.strftime('%A, %I:%M %p IST')}")

        target_date = target_now.date()
        target_hour = 8
        target_minute = 45

        # Decision tree for scheduling:
        # Mon (0), Tue (1), Wed (2) before 8:45 AM -> Today 8:45 AM
        # Mon (0), Tue (1), Wed (2) 8:45 AM - 11:30 AM -> Today 11:30 AM
        # Mon (0) or Tue (1) after 11:30 AM -> Tomorrow 8:45 AM
        # Wed (2) after 11:30 AM -> Thursday 8:45 AM
        # Thu (3) after 11:30 AM -> SKIP FRIDAY! Advance 5 days to next Tuesday 8:45 AM
        # Friday (4) anytime -> STRICT INVIOLABLE FRIDAY RULE! Advance 4 days to next Tuesday 8:45 AM
        # Saturday (5) -> Advance 3 days to next Tuesday 8:45 AM
        # Sunday (6) -> Advance 2 days to next Tuesday 8:45 AM

        if current_weekday in (0, 1, 2) and current_hour < 8:
            target_hour = 8
            target_minute = 45
            reasoning.append("Optimal slot is today morning at 08:45 AM before professor's morning lectures.")
        elif current_weekday in (0, 1, 2) and (current_hour == 8 and target_now.minute < 45):
            target_hour = 8
            target_minute = 45
            reasoning.append("Optimal slot is today morning at 08:45 AM.")
        elif current_weekday in (0, 1, 2) and current_hour < 11:
            target_hour = 11
            target_minute = 15
            reasoning.append("Morning desk review slot available today at 11:15 AM.")
        elif current_weekday in (0, 1):
            target_date = target_date + timedelta(days=1)
            target_hour = 8
            target_minute = 45
            reasoning.append("Today's morning window passed. Scheduled for tomorrow morning at 08:45 AM.")
        elif current_weekday == 2:
            target_date = target_date + timedelta(days=1)
            target_hour = 8
            target_minute = 45
            reasoning.append("Scheduled for Thursday morning at 08:45 AM.")
        elif current_weekday == 3:
            # Thursday afternoon -> Never schedule on Friday!
            target_date = target_date + timedelta(days=5)
            target_hour = 8
            target_minute = 45
            reasoning.append("🛡️ Friday Rule: Thursday afternoon/evening skipped past Friday and weekend directly to Tuesday 08:45 AM.")
        elif current_weekday == 4:
            # Friday -> STRICT RULE
            target_date = target_date + timedelta(days=4)
            target_hour = 8
            target_minute = 45
            reasoning.append("🛡️ Inviolable Friday Rule: Friday faculty inboxes are closing for the weekend. Scheduled for Tuesday 08:45 AM (Peak Open Rate).")
        elif current_weekday == 5:
            # Saturday
            target_date = target_date + timedelta(days=3)
            target_hour = 8
            target_minute = 45
            reasoning.append("🛡️ Weekend Avoidance: Scheduled for Tuesday 08:45 AM to avoid Monday morning rush.")
        elif current_weekday == 6:
            # Sunday
            target_date = target_date + timedelta(days=2)
            target_hour = 8
            target_minute = 45
            reasoning.append("🛡️ Weekend Avoidance: Scheduled for Tuesday 08:45 AM.")

        scheduled_local = datetime(
            target_date.year, target_date.month, target_date.day,
            target_hour, target_minute, 0, tzinfo=target_tz
        )
        
        scheduled_utc = scheduled_local.astimezone(timezone.utc)
        scheduled_ist = scheduled_local.astimezone(ist_tz)

        return {
            "country": location_info["country"],
            "city": location_info["city"],
            "timezone": tz_str,
            "matched_by": location_info["matched_by"],
            "diff_hours_str": diff_str,
            "activity_state": activity_state,
            "current_local_time": target_now.strftime("%a, %b %d • %I:%M %p"),
            "current_ist_time": ist_now.strftime("%a, %b %d • %I:%M %p IST"),
            "optimal_slot_local": scheduled_local.strftime("%A, %b %d at %I:%M %p"),
            "optimal_slot_ist": scheduled_ist.strftime("%A, %b %d at %I:%M %p IST"),
            "scheduled_iso": scheduled_utc.isoformat(),
            "scheduled_utc": scheduled_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "reasoning": reasoning,
            "friday_protected": True
        }

smart_scheduler = SmartScheduler()
