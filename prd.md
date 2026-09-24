# Product Requirements Document (PRD)
## PhD Professor Review & Cold Outreach Intelligence CRM

---

### 1. WHAT TO BUILD

#### 1.1 Product Definition
The **PhD Professor Review & Cold Outreach Intelligence CRM** is a purpose-built, academic-grade relationship management and communication intelligence platform for prospective PhD applicants. It empowers scholars to research professors, systematically analyze faculty publications and research alignment, draft hyper-personalized academic cold emails powered by Google Gemini AI, track multi-stage email interactions, and execute scheduled or timed batch sending with strict deliverability and academic etiquette safeguards.

#### 1.2 Core Purpose
Securing fully funded doctoral positions, research assistantships, and advisor sponsorship requires establishing meaningful scholarly connections with faculty. Applicants face two fatal bottlenecks:
1. **Research & Review Overhead**: Spending countless hours reading papers, deciphering lab directions, and manually assessing whether a professor's current research agenda aligns with the candidate's background.
2. **Outreach & Pipeline Chaos**: Managing cold emails across disparate spreadsheets, forgetting follow-ups, risking generic spam that gets immediately discarded, or sending emails at inappropriate times without tracking responses.

This platform bridges that gap by merging an **Academic Research Review Engine** with an **Intelligent Cold Outreach CRM**, leveraging Gemini models to synthesize papers, pinpoint collaboration angles, generate high-impact scholarly emails, and manage the full outreach lifecycle in one centralized, high-density interface.

#### 1.3 Key Product Goals
- **Deep Professor Review**: Provide structured dossier cards for each professor containing university, department, lab focus, recent papers (titles, abstracts, DOIs), funding indicators, and match rating.
- **Gemini AI Research & Outreach Co-Pilot**: Utilize Google Gemini (using the multi-key pool) to analyze faculty papers against the candidate's CV/statement, generate bespoke academic inquiry emails, and suggest precise research discussion questions.
- **Full-Funnel CRM Pipeline**: Track every professor through progressive stages: `Identified` ➔ `Reviewing` ➔ `Draft Prepared` ➔ `Scheduled` ➔ `Sent` ➔ `Opened/Replied` ➔ `Interview Scheduled` ➔ `Offer/Accepted` / `Archived`.
- **Intelligent Timed & Batch Sending**: Enable sending personalized emails individually or queued in timed batches (with automated spacing and timezone awareness) to prevent spam flags and honor academic sending etiquette.
- **Interaction History & Follow-Up System**: Log all email dispatches, replies, follow-up dates, notes, and professor feedback.
- **Zero-Hallucination & Human-in-the-Loop Guarantee**: Ensure that every AI-generated citation and statement is grounded in real provided papers, with mandatory candidate review and approval before any email can be dispatched.

---

### 2. TARGETED USER

#### 2.1 Primary Audience
- **Prospective PhD Candidates**: Master's students, postgraduates, and undergraduate seniors seeking funded PhD positions, research assistantships (RA), and faculty advisor mentorship globally.
- **Postdoctoral & Research Fellowship Applicants**: Early-career researchers reaching out to principal investigators (PIs) for lab positions.
- **Academic Mentors & Counselors**: Advisors assisting cohorts of students in managing their graduate school application pipelines.

#### 2.2 User Personas

##### Persona A: The Dedicated PhD Aspirant ("Arjun")
- **Background**: Master of Science graduate in Computer Science / AI seeking a funded PhD in Europe or North America.
- **Needs**:
  - A single dashboard to catalog 40+ target professors across 15 institutions.
  - Quick summary and critical analysis of each professor's 2-3 most recent publications.
  - AI assistance in crafting emails that reference specific methodology details rather than generic flattery.
  - Automated tracking of when emails were sent and automated alerts when follow-ups are due.
- **Frustrations**:
  - Lost tracking across messy spreadsheets.
  - Writer's block when drafting tailored emails.
  - Uncertainty about whether emails were delivered, opened, or ignored.

##### Persona B: The Cross-Discipline Scholar ("Elena")
- **Background**: Computational Biology researcher applying to both Computer Science and Bioengineering departments.
- **Needs**:
  - Tagging and categorizing professors by research cluster (e.g., "Genomics", "Structural Bio", "Diff Models").
  - Tailoring email tone and CV emphasis depending on the department's disciplinary lean.
  - Managing multiple resume versions and targeted email templates.

---

### 3. FEATURES

#### 3.1 Professor Review & Dossier Management
- **Professor Database (CRUD)**: Create, view, update, and manage professor profiles with:
  - Full Name, Title, Institution, Department, Official Webpage URL, Lab Website URL.
  - Verified Email Address, Secondary Contact/Lab Coordinator.
  - Research Keywords / Topic Tags (e.g., "Reinforcement Learning", "Cryo-EM", "NLP").
  - Current Accepting Students Status (`Yes`, `No`, `Unknown`, `Grant Funded`).
- **Research Paper Review Deck**:
  - Add recent publication metadata (Title, Year, Venue, Abstract, DOI/Link, Key Findings).
  - Review notes area: Candidate's reflections, strengths, potential research proposals.
  - Compatibility & Alignment Score (1 to 10 rating based on candidate interest & background overlap).

#### 3.2 Gemini AI Research & Outreach Co-Pilot
- **Multi-Key Gemini Engine**: Connects to the user's Gemini API key pool (`gemini-2.0-flash`, `gemini-1.5-pro`) with automated round-robin and rate-limit fallbacks.
- **AI Paper Alignment Analysis**: Analyzes the professor's paper abstracts and highlights:
  - Core methodology and problem statement.
  - Potential research gaps where the candidate's skills fit.
  - 2-3 specific technical discussion questions for cold emails.
- **Context-Aware Email Drafter**:
  - Generates bespoke, scholarly cold emails incorporating:
    - Candidate's background (education, thesis, tech stack, publications).
    - Professor's exact paper contribution and relevance.
    - Tailored subject line (high open-rate academic conventions).
    - Call-to-action (brief 15-minute video call or inquiry on PhD openings for upcoming intake).
- **Tone & Length Customizer**: Toggle email styles (Formal Academic, Concise/Direct, Technical Focus) and length (150 words, 250 words, 350 words).
- **AI Email Polish & Critique**: Critiques user drafts for tone, clarity, academic etiquette, and spam-trigger words.

#### 3.3 Email CRM & Pipeline Tracking
- **Visual Funnel / Kanban & Table Views**:
  - `Identified`: Initial discovery, profile created.
  - `Reviewing`: Reading papers and taking notes.
  - `Drafting`: Email draft generated or in preparation.
  - `Scheduled`: In outgoing queue for timed dispatch.
  - `Sent`: Successfully sent to professor.
  - `Replied`: Professor responded (sub-states: Interested, Meeting Scheduled, Not Accepting Students, Forwarded to Colleague).
  - `Follow-Up Needed`: Triggered after $N$ business days without reply.
  - `Closed/Archived`: Outcome recorded.
- **Interaction History Timeline**: Timestamped audit trail of every status change, email draft version, sent message, note, and reply.

#### 3.4 Email Creation, Batch Dispatch & Scheduling
- **Rich-Text Email Editor**: In-app compose window with variable placeholders (`{{professor_name}}`, `{{paper_title}}`, `{{institution}}`, `{{candidate_degree}}`).
- **SMTP / Direct Email Integration**:
  - Configure personal or institutional email via SMTP/IMAP (Gmail App Password, Outlook, Custom Academic SMTP).
  - Test connection and verify sender identity.
- **Batch Sending Queue**:
  - Select multiple reviewed professors and queue customized drafts.
  - **Timed Staggering**: Configurable dispatch intervals (e.g., 60-120 seconds between emails) to mimic natural human sending and safeguard mailbox deliverability.
  - **Daily Velocity Caps**: Hard limits (e.g., max 25 emails/day) to prevent domain burn.
  - **Timezone Scheduling**: Schedule dispatches to match the professor's local institution business hours (e.g., Tuesday at 9:15 AM EST).

#### 3.5 Templates & Candidate Profile Management
- **Candidate Profile Vault**: Store candidate's bio, CV, research interests, GPA/honors, portfolio/GitHub link, and PDF CV attachments.
- **Template Library**: Pre-built and customizable academic email templates:
  - First Inquiry (Direct Advisor Sponsorship).
  - Inquiry with Pre-Proposal / Ideas.
  - Polite 10-Day Follow-Up.
  - Acknowledgment of Rejection / Forwarding Request.

#### 3.6 Analytics & Oversight
- **Real-Time Funnel Metrics**: Total professors reviewed, emails sent, reply rate (%), positive response rate, average response latency.
- **Export & Backup**: Export CRM records to CSV/JSON; complete database backup and restore capabilities.
