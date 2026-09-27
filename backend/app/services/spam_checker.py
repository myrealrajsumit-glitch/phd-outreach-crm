"""
Academic Deliverability & Anti-Spam Defense Engine for PhD Outreach
Evaluates applicant cold emails against university mail filter heuristics
(Proofpoint, Barracuda, Microsoft 365 Defender, Google Workspace for Education)
to guarantee maximum inbox placement and faculty response rates.
"""

import re
from typing import Dict, Any, List, Optional

# High-risk spam triggers heavily penalized by university mail relays
CRITICAL_SPAM_TRIGGERS = [
    ("100% scholarship", "Guaranteeing or pleading for 100% scholarship triggers financial scam heuristics."),
    ("free funding", "Phrases like 'free funding' are common phishing/spam markers."),
    ("kindly revert", "'Kindly revert back' is recognized in academic Bayesian filters as generic bulk outreach."),
    ("revert back", "'Revert back' is outdated non-standard English flagged by university filters."),
    ("respected sir", "'Respected Sir' is a top tell of unresearched mass cold mailing from South Asia. Use 'Dear Professor [Last Name]'."),
    ("respected madam", "'Respected Madam' is a generic template marker. Address the professor specifically."),
    ("give me a chance", "Emotional pleading triggers spam filters and lowers academic credibility."),
    ("beg to state", "Archaic bureaucratic phrasing instantly triggers spam heuristics."),
    ("humble request", "Pleading language signals lack of confidence and generic mass mailing."),
    ("urgent reply", "Marking cold outreach as 'urgent' is a severe spam score trigger."),
    ("immediate response", "Demanding an immediate response from faculty triggers spam and deletion."),
    ("prestigious university", "Superficial flattery ('your prestigious university') signals zero paper reading."),
    ("world-renowned", "Vague flattery triggers academic spam heuristics."),
    ("dear sir/madam", "Generic 'Dear Sir/Madam' salutation guarantees 90%+ filter or bin rate."),
    ("to whom it may concern", "Never use 'To Whom It May Concern' for faculty outreach."),
    ("opportunity of a lifetime", "Sales/marketing buzzphrase flagged by spam classifiers."),
]

# Suspicious URL shorteners that trigger instant spam isolation
BLOCKED_SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "ow.ly", "goo.gl", "is.gd", "buff.ly", "cutt.ly"]

class PhDSpamDeliverabilityChecker:
    def analyze(
        self,
        subject: str,
        body: str,
        recipient_name: Optional[str] = None,
        recipient_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deeply inspects an outreach email subject and body for spam probability,
        academic etiquette, and deliverability risk.
        Returns a score from 0 to 100, risk classification, and actionable suggestions.
        """
        score = 100
        flags = []
        suggestions = []
        positive_signals = []

        sub = (subject or "").strip()
        text = (body or "").strip()
        lower_sub = sub.lower()
        lower_text = text.lower()
        words = text.split()
        word_count = len(words)

        # ----------------------------------------------------
        # 1. Subject Line Heuristics
        # ----------------------------------------------------
        if not sub:
            score -= 35
            flags.append("Missing subject line: Critical deliverability penalty.")
            suggestions.append("Add a structured subject line: 'Prospective PhD Inquiry - [Specific Topic] - [Your Name]'.")
        else:
            # Check all-caps in subject
            sub_caps_count = sum(1 for w in sub.split() if w.isupper() and len(w) > 2)
            if sub_caps_count > 1:
                score -= 20
                flags.append("ALL-CAPS words in subject line trigger spam filters.")
                suggestions.append("Use standard title casing in your subject line without all-caps words.")

            # Excessive exclamation marks or question marks
            if "!" in sub or "??" in sub:
                score -= 15
                flags.append("Punctuation ('!' or '??') in subject line heavily penalized by university firewalls.")
                suggestions.append("Remove exclamation marks from your subject line.")

            # Subject line spam keywords
            for trigger, reason in [("urgent", "Urgent in subject line"), ("please help", "Plea in subject line"), ("request for admission", "Generic admission plea")]:
                if trigger in lower_sub:
                    score -= 15
                    flags.append(f"Subject contains spam flag: '{trigger}'.")
                    suggestions.append(f"Remove '{trigger}' from subject line.")

            # Recommended subject format check
            if any(k in lower_sub for k in ["phd inquiry", "prospective phd", "research inquiry", "doctoral inquiry"]):
                positive_signals.append("Subject uses clear academic inquiry convention.")
            else:
                score -= 5
                suggestions.append("Clarify subject with: 'Prospective PhD Inquiry - [Research Area] - [Your Name]'.")

        # ----------------------------------------------------
        # 2. Critical Spam & Desperation Phrase Detection
        # ----------------------------------------------------
        found_triggers = []
        for phrase, reason in CRITICAL_SPAM_TRIGGERS:
            if phrase in lower_text or phrase in lower_sub:
                score -= 12
                found_triggers.append((phrase, reason))

        if found_triggers:
            for phrase, reason in found_triggers[:4]:  # Show top 4
                flags.append(f"Spam trigger detected: '{phrase}' - {reason}")
                suggestions.append(f"Remove '{phrase}' and replace with objective scholarly phrasing.")

        # ----------------------------------------------------
        # 3. Salutation & Professor Personalization
        # ----------------------------------------------------
        salutation_found = False
        has_generic_salutation = False

        if any(g in lower_text[:120] for g in ["respected sir", "respected madam", "dear sir", "dear madam", "to whom it may concern"]):
            score -= 25
            has_generic_salutation = True
            flags.append("Generic or deferential greeting ('Respected Sir/Madam') detected. This is a primary spam marker.")
            suggestions.append("Always greet faculty by name: 'Dear Professor [Last Name],' or 'Dear Dr. [Last Name],'.")
        elif any(g in lower_text[:100] for g in ["dear professor", "dear prof.", "dear dr.", "dr."]):
            salutation_found = True
            positive_signals.append("Professional academic salutation ('Dear Professor / Dr.') detected.")
        else:
            score -= 10
            suggestions.append("Start your email with: 'Dear Professor [Last Name],'")

        # Check if recipient's last name appears if known
        if recipient_name and not has_generic_salutation:
            name_parts = recipient_name.replace("Prof.", "").replace("Dr.", "").strip().split()
            last_name = name_parts[-1] if name_parts else ""
            if last_name and len(last_name) > 2 and last_name.lower() in lower_text[:120]:
                positive_signals.append(f"Personalized to Professor {last_name}.")
            elif last_name and len(last_name) > 2:
                suggestions.append(f"Verify you address the recipient as 'Dear Professor {last_name},'.")

        # ----------------------------------------------------
        # 4. Word Count & Cognitive Load
        # ----------------------------------------------------
        if word_count < 60:
            score -= 20
            flags.append(f"Email too brief ({word_count} words). Minimal emails often look like automated ping tests.")
            suggestions.append("Expand to 150-250 words, detailing your research background and alignment with the professor's lab.")
        elif word_count > 380:
            score -= 15
            flags.append(f"Email is too long ({word_count} words). Faculty skim emails; long drafts suffer high abandonment.")
            suggestions.append("Condense to 180-250 words. Focus on 1 paper reference, your key skills, and a brief call-to-action.")
        else:
            positive_signals.append(f"Optimal academic length ({word_count} words; ideal window is 150-280 words).")

        # ----------------------------------------------------
        # 5. Link Hygiene & URL Shorteners
        # ----------------------------------------------------
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)
        for u in urls:
            for blocked in BLOCKED_SHORTENERS:
                if blocked in u.lower():
                    score -= 30
                    flags.append(f"Dangerous URL shortener detected: '{blocked}'. University firewalls quarantine shortened links.")
                    suggestions.append(f"Remove shortened link '{u}' and provide clean direct links to your GitHub or Google Scholar.")

        if len(urls) > 3:
            score -= 15
            flags.append(f"Excessive link count ({len(urls)} links). High link density triggers promotional spam filters.")
            suggestions.append("Limit links to maximum 1-2 (e.g., your CV link or portfolio).")
        elif len(urls) <= 2:
            positive_signals.append("Clean link profile (0-2 direct links).")

        # ----------------------------------------------------
        # 6. Scholarly Evidence & Grounding Signals
        # ----------------------------------------------------
        scholarly_keywords = [
            "paper", "publication", "methodology", "algorithm", "dataset", "framework",
            "laboratory", "phd", "research", "thesis", "experiment", "model", "architecture"
        ]
        found_scholarly = [k for k in scholarly_keywords if k in lower_text]
        if len(found_scholarly) >= 3:
            positive_signals.append(f"Strong research vocabulary present ({', '.join(found_scholarly[:4])}).")
        else:
            score -= 10
            suggestions.append("Ground your email by referencing a specific publication, dataset, or methodology from the professor's recent work.")

        # ----------------------------------------------------
        # Final Score Normalization & Categorization
        # ----------------------------------------------------
        score = max(5, min(100, score))

        if score >= 90:
            rating = "EXCELLENT"
            color = "emerald"
            badge = "🛡️ Excellent Deliverability (Inbox Assured)"
        elif score >= 75:
            rating = "GOOD"
            color = "blue"
            badge = "✅ Good Academic Etiquette (Low Spam Risk)"
        elif score >= 55:
            rating = "MODERATE_RISK"
            color = "amber"
            badge = "⚠️ Moderate Risk (Spam Warning)"
        else:
            rating = "CRITICAL_SPAM_RISK"
            color = "rose"
            badge = "🚨 High Spam Risk (Filter Block Imminent)"

        return {
            "deliverability_score": score,
            "rating": rating,
            "badge": badge,
            "color": color,
            "word_count": word_count,
            "flags": flags,
            "suggestions": suggestions,
            "positive_signals": positive_signals,
            "is_safe_to_send": score >= 70
        }

spam_checker = PhDSpamDeliverabilityChecker()
