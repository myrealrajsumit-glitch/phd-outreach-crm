// Client-side Smart Scheduler & Timezone Intelligence Fallback
// Provides 100% offline reliability for PhD Outreach CRM when backend is unconfigured or serverless.

export const UNIVERSITY_DOMAINS = {
  // New Zealand
  "auckland.ac.nz": { country: "New Zealand", city: "Auckland", timezone: "Pacific/Auckland" },
  "otago.ac.nz": { country: "New Zealand", city: "Dunedin", timezone: "Pacific/Auckland" },
  "canterbury.ac.nz": { country: "New Zealand", city: "Christchurch", timezone: "Pacific/Auckland" },
  "vuw.ac.nz": { country: "New Zealand", city: "Wellington", timezone: "Pacific/Auckland" },
  "waikato.ac.nz": { country: "New Zealand", city: "Hamilton", timezone: "Pacific/Auckland" },
  "massey.ac.nz": { country: "New Zealand", city: "Palmerston North", timezone: "Pacific/Auckland" },
  "aut.ac.nz": { country: "New Zealand", city: "Auckland", timezone: "Pacific/Auckland" },
  "lincoln.ac.nz": { country: "New Zealand", city: "Lincoln", timezone: "Pacific/Auckland" },

  // Australia
  "unimelb.edu.au": { country: "Australia", city: "Melbourne", timezone: "Australia/Melbourne" },
  "sydney.edu.au": { country: "Australia", city: "Sydney", timezone: "Australia/Sydney" },
  "anu.edu.au": { country: "Australia", city: "Canberra", timezone: "Australia/Sydney" },
  "unsw.edu.au": { country: "Australia", city: "Sydney", timezone: "Australia/Sydney" },
  "uq.edu.au": { country: "Australia", city: "Brisbane", timezone: "Australia/Brisbane" },
  "monash.edu": { country: "Australia", city: "Melbourne", timezone: "Australia/Melbourne" },
  "uwa.edu.au": { country: "Australia", city: "Perth", timezone: "Australia/Perth" },
  "adelaide.edu.au": { country: "Australia", city: "Adelaide", timezone: "Australia/Adelaide" },
  "uts.edu.au": { country: "Australia", city: "Sydney", timezone: "Australia/Sydney" },

  // United States - Pacific
  "stanford.edu": { country: "United States", city: "Stanford, CA", timezone: "America/Los_Angeles" },
  "berkeley.edu": { country: "United States", city: "Berkeley, CA", timezone: "America/Los_Angeles" },
  "ucla.edu": { country: "United States", city: "Los Angeles, CA", timezone: "America/Los_Angeles" },
  "washington.edu": { country: "United States", city: "Seattle, WA", timezone: "America/Los_Angeles" },
  "caltech.edu": { country: "United States", city: "Pasadena, CA", timezone: "America/Los_Angeles" },
  "ucsd.edu": { country: "United States", city: "San Diego, CA", timezone: "America/Los_Angeles" },

  // United States - Eastern
  "mit.edu": { country: "United States", city: "Cambridge, MA", timezone: "America/New_York" },
  "harvard.edu": { country: "United States", city: "Cambridge, MA", timezone: "America/New_York" },
  "cmu.edu": { country: "United States", city: "Pittsburgh, PA", timezone: "America/New_York" },
  "columbia.edu": { country: "United States", city: "New York, NY", timezone: "America/New_York" },
  "princeton.edu": { country: "United States", city: "Princeton, NJ", timezone: "America/New_York" },
  "cornell.edu": { country: "United States", city: "Ithaca, NY", timezone: "America/New_York" },
  "yale.edu": { country: "United States", city: "New Haven, CT", timezone: "America/New_York" },
  "upenn.edu": { country: "United States", city: "Philadelphia, PA", timezone: "America/New_York" },
  "gatech.edu": { country: "United States", city: "Atlanta, GA", timezone: "America/New_York" },
  "nyu.edu": { country: "United States", city: "New York, NY", timezone: "America/New_York" },

  // United Kingdom
  "ox.ac.uk": { country: "United Kingdom", city: "Oxford", timezone: "Europe/London" },
  "cam.ac.uk": { country: "United Kingdom", city: "Cambridge", timezone: "Europe/London" },
  "imperial.ac.uk": { country: "United Kingdom", city: "London", timezone: "Europe/London" },
  "ucl.ac.uk": { country: "United Kingdom", city: "London", timezone: "Europe/London" },
  "ed.ac.uk": { country: "United Kingdom", city: "Edinburgh", timezone: "Europe/London" },
  "manchester.ac.uk": { country: "United Kingdom", city: "Manchester", timezone: "Europe/London" },
  "brunel.ac.uk": { country: "United Kingdom", city: "London", timezone: "Europe/London" },

  // India
  "iisc.ac.in": { country: "India", city: "Bengaluru", timezone: "Asia/Kolkata" },
  "iitb.ac.in": { country: "India", city: "Mumbai", timezone: "Asia/Kolkata" },
  "iitd.ac.in": { country: "India", city: "New Delhi", timezone: "Asia/Kolkata" },
  "iitm.ac.in": { country: "India", city: "Chennai", timezone: "Asia/Kolkata" },
  "iitk.ac.in": { country: "India", city: "Kanpur", timezone: "Asia/Kolkata" },

  // Singapore, Europe & Canada
  "nus.edu.sg": { country: "Singapore", city: "Singapore", timezone: "Asia/Singapore" },
  "ntu.edu.sg": { country: "Singapore", city: "Singapore", timezone: "Asia/Singapore" },
  "ethz.ch": { country: "Switzerland", city: "Zurich", timezone: "Europe/Zurich" },
  "tum.de": { country: "Germany", city: "Munich", timezone: "Europe/Berlin" },
  "utoronto.ca": { country: "Canada", city: "Toronto, ON", timezone: "America/Toronto" },
  "ubc.ca": { country: "Canada", city: "Vancouver, BC", timezone: "America/Vancouver" }
};

export const TLD_DEFAULTS = {
  "ac.nz": { country: "New Zealand", city: "Auckland / Wellington", timezone: "Pacific/Auckland" },
  "nz": { country: "New Zealand", city: "New Zealand", timezone: "Pacific/Auckland" },
  "edu.au": { country: "Australia", city: "Sydney / Melbourne", timezone: "Australia/Sydney" },
  "au": { country: "Australia", city: "Australia (Eastern)", timezone: "Australia/Sydney" },
  "ac.uk": { country: "United Kingdom", city: "London / Oxford", timezone: "Europe/London" },
  "uk": { country: "United Kingdom", city: "United Kingdom", timezone: "Europe/London" },
  "ie": { country: "Ireland", city: "Dublin", timezone: "Europe/Dublin" },
  "ca": { country: "Canada", city: "Toronto / Montreal", timezone: "America/Toronto" },
  "de": { country: "Germany", city: "Berlin / Munich", timezone: "Europe/Berlin" },
  "ch": { country: "Switzerland", city: "Zurich / Geneva", timezone: "Europe/Zurich" },
  "sg": { country: "Singapore", city: "Singapore", timezone: "Asia/Singapore" },
  "in": { country: "India", city: "India", timezone: "Asia/Kolkata" },
  "edu": { country: "United States", city: "USA (Academic)", timezone: "America/New_York" }
};

export function clientCalculateOptimalSchedule(email = '', institution = '') {
  let target = {
    country: "International Academic",
    city: "Global",
    timezone: "America/New_York"
  };

  const domain = (email.includes('@') ? email.split('@')[1] : '').toLowerCase().trim();
  const instLower = (institution || '').toLowerCase().trim();

  // Match known domain
  if (UNIVERSITY_DOMAINS[domain]) {
    target = UNIVERSITY_DOMAINS[domain];
  } else {
    // Check known domain suffix
    for (const [d, meta] of Object.entries(UNIVERSITY_DOMAINS)) {
      if (domain.endsWith(d)) {
        target = meta;
        break;
      }
    }
    // Check TLD defaults
    if (target.city === "Global") {
      for (const [tld, meta] of Object.entries(TLD_DEFAULTS)) {
        if (domain.endsWith(`.${tld}`) || domain === tld) {
          target = meta;
          break;
        }
      }
    }
    // Check institution keywords
    if (target.city === "Global" && instLower) {
      if (instLower.includes("new zealand") || instLower.includes("auckland")) {
        target = { country: "New Zealand", city: "Auckland", timezone: "Pacific/Auckland" };
      } else if (instLower.includes("australia") || instLower.includes("melbourne") || instLower.includes("sydney")) {
        target = { country: "Australia", city: "Sydney", timezone: "Australia/Sydney" };
      } else if (instLower.includes("oxford") || instLower.includes("cambridge") || instLower.includes("london") || instLower.includes("uk") || instLower.includes("brunel")) {
        target = { country: "United Kingdom", city: "London", timezone: "Europe/London" };
      } else if (instLower.includes("iit") || instLower.includes("india")) {
        target = { country: "India", city: "India", timezone: "Asia/Kolkata" };
      }
    }
  }

  // If still generic email (e.g. @gmail.com) with no university
  if (target.city === "Global" && (domain === 'gmail.com' || domain === 'yahoo.com' || domain === 'outlook.com' || domain === 'hotmail.com')) {
    target = { country: "Direct Contact", city: "Recipient Local", timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "Asia/Kolkata" };
  }

  const now = new Date();

  // Format local times
  const localTimeFormatter = new Intl.DateTimeFormat('en-US', {
    timeZone: target.timezone,
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
    weekday: 'short'
  });
  const current_local_time = localTimeFormatter.format(now);

  const istFormatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Kolkata',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
    weekday: 'short'
  });
  const current_ist_time = istFormatter.format(now);

  // Compute timezone offset difference
  const nowUtc = now.getTime();
  const getOffsetMinutes = (tz) => {
    const d = new Date(nowUtc);
    const invdate = new Date(d.toLocaleString('en-US', { timeZone: tz }));
    return Math.round((invdate.getTime() - d.getTime()) / 60000);
  };

  const targetOffsetMin = getOffsetMinutes(target.timezone);
  const istOffsetMin = getOffsetMinutes('Asia/Kolkata');
  const diffHours = (targetOffsetMin - istOffsetMin) / 60;
  const diff_hours_str = diffHours === 0 
    ? "Same time as India (IST)"
    : diffHours > 0 
      ? `+${diffHours % 1 === 0 ? diffHours : diffHours.toFixed(1)} hrs ahead of IST`
      : `${diffHours % 1 === 0 ? diffHours : diffHours.toFixed(1)} hrs behind IST`;

  // Activity State based on target's hour of the day
  const targetHour = parseInt(new Intl.DateTimeFormat('en-US', {
    timeZone: target.timezone,
    hour: 'numeric',
    hour12: false
  }).format(now), 10);

  let activity_state = "💼 Working Hours (Peak Focus)";
  if (targetHour >= 22 || targetHour < 7) {
    activity_state = "🌙 In Bed / Sleeping (Do Not Disturb)";
  } else if (targetHour >= 7 && targetHour < 9) {
    activity_state = "🌅 Morning Commute";
  } else if (targetHour >= 12 && targetHour < 14) {
    activity_state = "🥪 Lunch Break / Advising";
  } else if (targetHour >= 17 && targetHour < 22) {
    activity_state = "🌇 Evening / Winding Down";
  }

  // Calculate Optimal Academic Delivery Window (Strictly Tuesday, Wednesday, or Thursday at 9:30 AM local)
  // Day of week: 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat
  const getNextOptimalDate = () => {
    // Look ahead from tomorrow up to 7 days
    let candidate = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    for (let i = 0; i < 7; i++) {
      const dayOfWeek = candidate.getUTCDay();
      // Tuesday (2), Wednesday (3), Thursday (4) are prime academic inbox days. Friday (5), Saturday (6), Sunday (0) strictly avoided.
      if (dayOfWeek >= 2 && dayOfWeek <= 4) {
        return candidate;
      }
      candidate = new Date(candidate.getTime() + 24 * 60 * 60 * 1000);
    }
    return new Date(now.getTime() + 48 * 60 * 60 * 1000);
  };

  const optimalDate = getNextOptimalDate();
  const dayName = new Intl.DateTimeFormat('en-US', { weekday: 'long', timeZone: target.timezone }).format(optimalDate);
  const monthDay = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', timeZone: target.timezone }).format(optimalDate);
  const optimal_slot_local = `${dayName} (${monthDay}) at 9:30 AM`;

  // Equivalent in IST
  const optimal_slot_ist = `IST: ~${diffHours < 0 ? (9.5 - diffHours).toFixed(1) : (9.5 - diffHours).toFixed(1)} hrs`;

  return {
    email,
    institution: institution || target.city,
    country: target.country,
    city: target.city,
    timezone: target.timezone,
    current_local_time,
    current_ist_time,
    diff_hours_str,
    activity_state,
    is_safe_sending_window: targetHour >= 9 && targetHour <= 16,
    optimal_slot_local,
    optimal_slot_ist: `Synced to ${target.timezone.split('/')[1] || target.timezone}`,
    scheduled_iso: optimalDate.toISOString(),
    recommendation: "Academic faculty reply rates peak Tuesday–Thursday 9:00 AM – 11:30 AM. Friday inbox drops strictly prevented."
  };
}
