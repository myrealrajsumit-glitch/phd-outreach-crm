# Project Memory & State Tracking
## PhD Professor Review & Intelligent Cold Outreach CRM

---

### 1. MEMORY

#### 1.1 Important Context & Architecture Decisions
- **Smart Timezone & Country Thinking Engine**: The CRM automatically parses the professor's email domain/institution, resolves the destination country and IANA timezone, and maps the offset relative to India Standard Time (IST, UTC+5:30).
- **Inviolable Friday & Weekend Outreach Protection**: Automated rule that strictly prohibits scheduling cold outreach on Friday or over the weekend. Faculty inboxes on Friday have poor attention spans (<12% response rate) and emails get buried by Monday morning. Any scheduling initiated on Thursday afternoon or Friday automatically rolls forward to **Tuesday 08:45 AM local destination time**.
- **PhD Anti-Spam & Deliverability Protocol**: Built-in backend heuristic analyzer (`spam_checker.py`) that checks outgoing subject lines and email bodies against university spam heuristics (detecting desperate buzzwords, generic salutations like "Respected Sir", suspicious URL shorteners, excessive length, or lack of grounded publication references).
- **Dual-Action Dispatch System**: Replaced obsolete "Open in Gmail" shortcuts with two first-class CRM options:
  1. **⚡ Send Instant Email**: Dispatches immediately via configured SMTP relay.
  2. **📅 Smart Schedule Email**: Automatically schedules delivery in the professor's optimal local morning slot.
- **Local-First & Rock-Solid Backend**: As requested by the user, deployment to Vercel is suspended. The priority is a robust, well-tested Python/FastAPI async backend with SQLite persistence, zero external broker bloat, and total privacy for applicant data.

#### 1.2 User Preferences & Project Settings
- **Candidate Timezone**: India Standard Time (IST, UTC+5:30).
- **Primary AI Model**: `gemini-2.0-flash` (multi-key pool with automatic rotation and retry).
- **Email Dispatch Guardrails**: Maximum velocity throttled to 25 emails/day; minimum staggering interval of 45–120s between queue dispatches.
- **Outreach Scope**: Global PhD & Research Fellowship positions across North America, UK, Europe, and Asia-Pacific.

---

### 2. WHAT HAPPENED

#### 2.1 Milestone Log
- **2026-09-23 (Reset & Foundation)**:
  - Scrapped legacy code and initialized structured 6-document architecture.
  - Backed up authorized Gemini API keys into root `.env`.
- **2026-09-23 (Full Stack Build & Validation - Phases 1 to 5)**:
  - Phase 1: Authentication & user workspace.
  - Phase 2: React 18 + Vite dashboard with responsive sidebar.
  - Phase 3: Professor & research paper catalog with detail dossier.
  - Phase 4: Gemini AI Co-Pilot & outreach center.
  - Phase 5: Initial unit tests and Vite client builds.
- **2026-09-25 (Intelligent Scheduling & Anti-Spam Deliverability Upgrade)**:
  - **Comprehensive PRD Upgrade (`prd.md`)**: Fully updated following the exact 3-section template (What to Build, Targeted User, Features) incorporating the timezone thinking system, anti-spam protocol, and dual-dispatch interface.
  - **Smart Scheduler & Timezone Engine (`smart_scheduler.py`)**: Built country and timezone detection across 100+ global university domains and ccTLDs. Implemented activity state detection (Sleeping vs Desk time) and strict Friday/weekend avoidance.
  - **Academic Anti-Spam Defense Service (`spam_checker.py`)**: Built deliverability analyzer detecting dangerous trigger phrases ("Respected Sir", "100% scholarship", "kindly revert"), shorteners (`bit.ly`), link limits, word counts, and proper salutations.
  - **REST API Endpoints (`email_routes.py`)**: Added `POST /api/emails/analyze-schedule` and `POST /api/emails/check-spam`.
  - **Frontend Outreach Composer (`GmailCompose.jsx`)**: Integrated real-time country intelligence banner, live anti-spam deliverability meter, and dual dispatch buttons (**⚡ Send Instant Email** vs **📅 Smart Schedule Email**). Completely eradicated all "Open in Gmail" buttons.
  - **Quality Assurance**: Executed pytest test suite (`backend/tests/test_scheduler_and_spam.py` + `backend/tests/test_api_flow.py`) with 5/5 passing (100%). Verified Vite production client build compiles cleanly in 2.40s.

---

### 3. CURRENTLY WORKING

- **Current Status**: Backend and frontend are synchronized, fully functional locally, and tested.
- **Next Steps When Resuming**:
  1. Run the local backend server via `backend\.venv\Scripts\python.exe backend/run_server.py`.
  2. Run the frontend development server via `npm run dev` in `frontend/`.
  3. Validate real professor email typing in the outreach composer and verify live deliverability score and scheduling slots.

---

### 4. UPDATES

- **Maintenance Protocol**:
  - Update this document after completing each major phase or architectural decision.
  - Keep test coverage at 100% for all scheduling and deliverability modules.

---

### 5. PURPOSE

- **Maintain Context Across Sessions**: Ensure that future agent and developer sessions immediately understand the project purpose, architecture, and current execution phase.
- **Improve Productivity & Consistency**: Prevent redundant work, accidental deletion of credentials, or deviation from approved design tokens.
- **Ensure Nothing Important Is Forgotten**: Retain critical parameters (rate limits, key rotation policies, delivery safeguards) across long development intervals.
