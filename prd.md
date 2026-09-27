# Product Requirements Document (PRD)
## PhD Professor Review & Intelligent Cold Outreach CRM

---

### 1. WHAT TO BUILD

#### 1.1 Product Definition
The **PhD Professor Review & Intelligent Cold Outreach CRM** is an academic-grade relationship management and communication intelligence platform engineered specifically for prospective PhD applicants and research fellowship seekers. It bridges research discovery, faculty publication analysis, timezone-intelligent outreach scheduling, and email deliverability engineering into a unified, high-performance workspace.

#### 1.2 Core Purpose
Securing fully funded doctoral positions, research assistantships (RA), and faculty advisor sponsorship requires establishing credible scholarly connections with faculty. Prospective applicants face four critical failure points:
1. **Timezone Disconnect (The "India-to-Global" Gap)**: Applicants (particularly in South Asia / India) operate in opposite circadian cycles to institutions in North America and Western Europe. Cold emails sent during Indian daytime arrive in professors' inboxes at 2:00 AM or 3:00 AM local time, getting pushed down into oblivion by morning spam and department memos.
2. **The University Spam Shield Trap**: University mail relays (Proofpoint, Barracuda, Microsoft Defender for Office 365, Google Workspace for Education) employ aggressive spam filtering heuristics. Cold emails featuring generic greetings ("Respected Sir/Madam"), spam buzzwords ("urgent", "100% scholarship", "free funding"), tracking pixels, or high-pressure phrasing are immediately routed to Spam or Quarantine folders, never reaching faculty eyes.
3. **The Friday Outreach Mistake**: Faculty inboxes on Friday are dominated by end-of-week deadlines, grading, and weekend prep. Emails sent on Friday afternoon or evening have a dismal open rate (<12%) and remain buried under Monday morning departmental backlogs.
4. **Research Alignment Overhead**: Evaluating whether a professor's current lab trajectory matches the applicant's background requires deciphering dozens of recent papers, leading to generic emails that faculty immediately discard.

This platform resolves these challenges through a **Smart Timezone & Country Intelligence Engine**, an **Academic Anti-Spam Protocol & Deliverability Validator**, and a **Gemini AI-Powered Research Co-Pilot**.

#### 1.3 Key Product Goals
- **Smart Timezone & Country Detection**: Automatically resolve target country, city, and institution timezone directly from the professor's email domain (e.g., `ox.ac.uk` ➔ UK, `stanford.edu` ➔ US Pacific, `tum.de` ➔ Germany).
- **Dual-Action Outreach Interface**: Provide two explicit, unmistakable dispatch pathways:
  1. **Send Instant Email**: Dispatches immediately via configured secure SMTP credentials.
  2. **Smart Schedule Email**: Automatically schedules delivery in the professor's peak inbox-review window (08:30 AM – 09:30 AM local destination time) while converting transparently to India Standard Time (IST).
- **Strict Inviolable Scheduling Rules**: Absolutely zero outreach scheduling on Fridays or weekends. If an outreach is planned on Thursday afternoon or Friday, the system automatically advances to Tuesday morning (the statistically highest response window in academia).
- **Anti-Spam & Deliverability Defense**: A built-in heuristic deliverability analyzer that calculates a Spam Risk Score (0-100%), flags dangerous trigger words, enforces academic salutation standards, and guarantees clean deliverability without tracking pixels or suspicious attachments.
- **Deep Professor Dossier**: Catalog professors with laboratory focus, research keywords, recent publications, and candidate compatibility notes.
- **Removal of Disconnected "Open in Gmail" Workarounds**: Eliminate external browser hops and keep full tracking and sending reliability native to the CRM.
- **Robust Local-First Backend**: High-performance async FastAPI backend with SQLite persistence, zero cloud deployment bloat, and total privacy for applicant research data.

---

### 2. TARGETED USER

#### 2.1 Primary Audience
- **Prospective PhD Candidates**: Master's students, postgraduates, and undergraduate seniors seeking funded PhD positions and research assistantships globally (especially applicants applying from India and international timezones to North America, UK, Europe, and Asia-Pacific).
- **Postdoctoral & Research Fellowship Seekers**: PhD graduates reaching out to Principal Investigators (PIs) for specialized post-doc lab appointments.
- **Academic Mentors & Guidance Counselors**: Academic advisors managing candidate cohorts through doctoral admissions outreach.

#### 2.2 User Personas

##### Persona A: The International PhD Aspirant ("Arjun")
- **Profile**: Final-year Master's in Computer Science student based in Bengaluru, India (IST timezone). Target: 40 AI/ML faculty across US and European universities.
- **Pain Points**:
  - Struggles with time difference: Sends emails at 2:00 PM IST (which is 4:30 AM in Boston or 1:30 AM in Stanford), causing emails to be buried before professors wake up.
  - Emails constantly end up in Spam because of unvetted phrasing ("Respected Sir", "Kindly revert back", "Need urgent consideration").
  - Anxious about sending emails on Friday that get ignored over the weekend.
- **How This CRM Solves It**:
  - Arjun simply enters `prof@cs.cmu.edu`. The system detects **United States (US Eastern / America/New_York)**, compares it with IST (+9.5 hours), and automatically schedules the email for **Tuesday at 8:45 AM EDT (6:15 PM IST)**.
  - The Anti-Spam Meter scores his draft in real-time, alerts him to remove "Respected Sir", and suggests "Dear Professor CMU_Name".

##### Persona B: The Specialized Systems Scholar ("Priya")
- **Profile**: Research engineer targeting specialized European labs in Switzerland (ETH Zurich), Germany (TUM), and the UK (Oxford).
- **Pain Points**:
  - Fragmented records across spreadsheets; loses track of who replied and who needs a 10-day follow-up.
  - Does not know whether to send immediately or schedule according to European working hours.
- **How This CRM Solves It**:
  - Visual Kanban pipeline tracks each professor from `Identified` ➔ `Reviewing` ➔ `Draft_Ready` ➔ `Scheduled` ➔ `Sent` ➔ `Replied`.
  - Smart scheduler detects `.ch` and `.de` domains and provides one-click instant send or automated morning European dispatch.

---

### 3. FEATURES

#### 3.1 Smart Country, Timezone & Scheduling System ("Thinking Engine")
- **Automatic Email Domain Resolution**:
  - Inspects the recipient email address (e.g., `smith@berkeley.edu`, `johnson@cam.ac.uk`, `weber@tum.de`, `tan@nus.edu.sg`).
  - Matches against an embedded database of over 100 top global academic institutions and ccTLDs (`.edu`, `.ac.uk`, `.de`, `.ch`, `.ca`, `.fr`, `.nl`, `.se`, `.au`, `.sg`, `.jp`, etc.).
  - Extracts target Country, City/Campus, and canonical IANA Timezone.
- **Circadian Clock Bridge (India Standard Time ➔ Local University Time)**:
  - Continuously calculates the real-time offset between candidate's local time (IST, UTC+5:30) and the professor's local time.
  - Displays a visual badge: e.g., *"Detected: United States (US Pacific) • Professor's time: 11:45 PM (Sleeping) • Candidate time: 3:15 PM IST"*.
- **Optimal Academic Delivery Windows**:
  - Target sending window: **08:30 AM – 09:30 AM** local time on working weekdays.
  - Prime delivery slot: 08:45 AM local time, ensuring the message arrives right as faculty unlock their laptops before morning classes or lab meetings.
- **Inviolable Friday & Weekend Protection**:
  - **Rule**: NEVER schedule or dispatch outreach on Friday.
  - If a schedule is triggered on Thursday afternoon, Friday, or over the weekend, the engine automatically rolls forward to **Tuesday 08:45 AM** local time.
  - Tuesday is proven across academic communication studies to yield the highest faculty response rate.
- **Dual-Action Dispatch Interface**:
  - **Option 1: ⚡ Send Instant Email**: Dispatches immediately via configured SMTP credentials.
  - **Option 2: 📅 Smart Schedule Email**: Automatically commits the draft to the background queue with the exact computed optimal timestamp.
  - **Clean UI**: 100% removal of obsolete "Open in Gmail" buttons.

#### 3.2 Academic Anti-Spam Protocol & Deliverability Defense Engine
- **Academic Deliverability Analyzer**:
  - Evaluates outgoing email drafts against institutional spam heuristics before sending or scheduling.
  - Generates an **Inbox Deliverability Score (0 – 100%)** and categorical rating (`Excellent`, `Good`, `Needs Revision`, `High Spam Risk`).
- **Spam Trigger Word & Desperation Phrase Detection**:
  - Flags high-risk vocabulary commonly found in spam student cold emails: *"100% scholarship"*, *"free funding"*, *"urgent response needed"*, *"kindly revert back"*, *"respected sir"*, *"sir/madam"*, *"give me a chance"*, *"beg to state"*.
- **Academic Etiquette & Salutation Verification**:
  - Enforces proper academic honorifics (`Dear Professor [Last Name]` or `Dear Dr. [Last Name]`).
  - Flags generic greetings (`Dear Sir`, `Respected Professor`, `To Whom It May Concern`) that trigger spam heuristics and immediate cognitive dismissal.
- **Formatting & Technical Deliverability Standards**:
  - Plain-text optimized: Zero hidden tracking pixels, zero tracking redirects that trigger institutional firewall blocks.
  - Link hygiene: Recommends maximum 1-2 clean academic URLs (e.g., candidate's Google Scholar, GitHub, or institutional lab page). Prohibits URL shorteners (`bit.ly`, `tinyurl`).
  - Word count validator: Optimal range of 150 – 250 words. Alerts the user if text is too short (<80 words, flags low effort) or too long (>350 words, causes skim-and-delete behavior).
- **Subject Line Recommendation Protocol**:
  - Validates subject line against established academic high-open-rate formulas:
    - `Prospective PhD Inquiry - [Specific Research Subfield] - [Candidate Name]`
    - `PhD Applicant (Fall 2026): [Candidate Research Focus] - Inquiry for Prof. [Last Name]`
  - Rejects spammy subjects with exclamation marks, all-caps words, or desperate language (`URGENT Inquiry`, `PhD Admission request please help`).

#### 3.3 Professor Dossier & Research Review Hub
- **Professor Catalog (CRUD)**:
  - Store full profile: Name, Title, Institution, Department, Lab Website, Verified Email Address.
  - Research Keywords & Domain Tags (e.g., `Reinforcement Learning`, `Distributed Systems`, `Genomics`).
  - Student intake status: `Accepting Students`, `Funding Uncertain`, `Sabbatical`, `Unknown`.
- **Publication Deck**:
  - Catalog recent papers (Title, Venue, Year, Abstract, DOI link).
  - Add personal reading notes, research gap hypotheses, and candidate synergy notes.
  - Compatibility rating (1 to 10 scale).

#### 3.4 Gemini AI Research & Outreach Co-Pilot
- **Multi-Key Pool Engine**:
  - Connects to user's Google Gemini API key pool (`gemini-2.0-flash`) with automatic failover and exponential backoff.
- **Grounded Research Hook Drafter**:
  - Synthesizes candidate's background with the professor's real published paper.
  - Produces tailored inquiry drafts that reference exact methodological contributions rather than superficial praise.
- **AI Deliverability & Polish Co-Pilot**:
  - Reviews candidate-typed emails and suggests edits to maximize deliverability and scholarly tone.

#### 3.5 Pipeline CRM & Email Dispatch Center
- **Funnel Progression**:
  - `Identified` ➔ `Reviewing` ➔ `Draft_Ready` ➔ `Scheduled` ➔ `Sent` ➔ `Replied` ➔ `Interview Scheduled` ➔ `Closed`.
- **Staggered Queue Dispatcher**:
  - Automated background worker handles scheduled dispatches with humanized intervals (45–120 seconds) to prevent SMTP relay rate limits.
- **Audit History**:
  - Timestamped logs of every interaction, status update, and scheduled delivery.
