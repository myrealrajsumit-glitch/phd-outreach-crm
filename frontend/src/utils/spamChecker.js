// Client-side Academic Spam Checker Fallback
// Ensures deliverability score and warning heuristics work even when backend is offline or on Vercel.

export const SPAM_TRIGGERS = [
  { trigger: "100% scholarship", reason: "Guaranteed/pleading scholarship phrasing triggers financial scam heuristics." },
  { trigger: "free funding", reason: "'Free funding' is flagged as a phishing marker by university filters." },
  { trigger: "kindly revert", reason: "'Kindly revert back' is recognized in academic spam filters as bulk mailing." },
  { trigger: "revert back", reason: "'Revert back' is outdated non-standard phrasing heavily flagged." },
  { trigger: "respected sir", reason: "'Respected Sir' triggers bulk mass-mail heuristics. Use 'Dear Professor [Last Name]'." },
  { trigger: "respected madam", reason: "'Respected Madam' is a generic template marker." },
  { trigger: "give me a chance", reason: "Emotional pleading lowers academic credibility and triggers filters." },
  { trigger: "beg to state", reason: "Bureaucratic begging phrasing triggers instant spam classification." },
  { trigger: "humble request", reason: "Pleading language signals mass outreach." },
  { trigger: "urgent reply", reason: "Marking inquiry as 'urgent' is a severe spam score trigger." },
  { trigger: "immediate response", reason: "Demanding immediate reply triggers deletion/filtering." },
  { trigger: "dear sir/madam", reason: "'Dear Sir/Madam' salutation guarantees 90%+ spam isolation." },
  { trigger: "to whom it may concern", reason: "Avoid generic recipient greetings." }
];

export function clientCheckSpam(subject = '', body = '', recipientName = '', recipientEmail = '') {
  let score = 100;
  const flags = [];
  const suggestions = [];
  const positive_signals = [];

  const sub = (subject || '').trim();
  const text = (body || '').trim();
  const lowerSub = sub.toLowerCase();
  const lowerText = text.toLowerCase();
  const words = text ? text.split(/\s+/) : [];
  const wordCount = words.length;

  // 1. Subject Line Checks
  if (!sub) {
    flags.push("Empty subject line (High spam drop rate).");
    score -= 30;
  } else {
    if (sub.length > 70) {
      flags.push(`Subject line too long (${sub.length} chars). Keep under 65 chars.`);
      score -= 8;
    }
    if (sub.length < 15 && wordCount > 0) {
      flags.push("Subject line is too brief or ambiguous (e.g. 'hi' or 'inquiry').");
      score -= 15;
    }
    if (sub.toUpperCase() === sub && /[A-Z]/.test(sub)) {
      flags.push("ALL-CAPS in subject line triggers severe spam filters.");
      score -= 30;
    }
    if (sub.includes("!")) {
      flags.push("Exclamation mark in subject line triggers marketing filters.");
      score -= 10;
    }
    if (lowerSub.includes("phd") || lowerSub.includes("prospective") || lowerSub.includes("inquiry") || lowerSub.includes("research")) {
      positive_signals.push("Subject line includes scholarly context keywords.");
    }
  }

  // 2. Body Spam Keywords Check
  SPAM_TRIGGERS.forEach(({ trigger, reason }) => {
    if (lowerText.includes(trigger) || lowerSub.includes(trigger)) {
      flags.push(`Flagged phrase detected: "${trigger}" — ${reason}`);
      score -= 12;
    }
  });

  // 3. Word Count Check
  if (wordCount > 0) {
    if (wordCount < 40) {
      flags.push(`Extremely brief body (${wordCount} words). Add scholarly substance.`);
      score -= 15;
    } else if (wordCount > 400) {
      flags.push(`Email is too long (${wordCount} words). Faculty skim emails; target 180–260 words.`);
      score -= 10;
    } else if (wordCount >= 140 && wordCount <= 280) {
      positive_signals.push(`Optimal academic length (${wordCount} words). High likelihood of reading.`);
    }
  }

  // 4. Positive Signals
  if (lowerText.includes("dr.") || lowerText.includes("prof") || (recipientName && lowerText.includes(recipientName.toLowerCase()))) {
    positive_signals.push("Personalized academic salutation present.");
  }
  if (lowerText.includes("paper") || lowerText.includes("publication") || lowerText.includes("research") || lowerText.includes("dissertation")) {
    positive_signals.push("Evidence-grounded scholarly references detected.");
  }

  score = Math.max(10, Math.min(100, score));

  let rating = "EXCELLENT";
  let is_safe_to_send = true;
  if (score < 45) {
    rating = "CRITICAL_SPAM";
    is_safe_to_send = false;
  } else if (score < 70) {
    rating = "MODERATE_RISK";
    is_safe_to_send = false;
  } else if (score < 85) {
    rating = "GOOD";
  }

  if (flags.length === 0) {
    suggestions.push("Clean draft! Ready for academic delivery.");
  }

  return {
    score,
    deliverability_score: score,
    rating,
    is_safe_to_send,
    word_count: wordCount,
    flags,
    suggestions,
    positive_signals
  };
}
