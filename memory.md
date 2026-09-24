# Project Memory & State Tracking
## PhD Professor Review & Cold Outreach Intelligence CRM

---

### 1. MEMORY

#### 1.1 Important Context & Architecture Decisions
- **Complete Legacy Reset**: The prior crawler/discovery and automated audit codebase was completely scrapped per user instruction to pivot to a focused, user-controlled **Professor Review & Cold Outreach CRM**.
- **Preserved API Credentials**: The multi-key Gemini pool (`GEMINI_API_KEY_01` through `GEMINI_API_KEY_06`) and `OPENROUTER_API_KEY` are safely preserved in the root `.env` file.
- **Architectural Tenet**: High-speed, lightweight, self-contained architecture utilizing FastAPI (Python 3.11+) + React 18 / Vite + SQLite (aiosqlite) with zero external message broker bloat.
- **Outreach Invariant**: Strict Human-in-the-Loop requirement. All emails must be reviewed by the candidate before queuing. No autonomous unverified bulk blasting.

#### 1.2 User Preferences & Project Settings
- **Primary AI Model**: `gemini-2.0-flash` (with automated multi-key rotation and exponential backoff).
- **Email Dispatch Guardrails**: Default daily sending velocity capped at 25 emails/day; minimum staggering interval of 45–120 seconds between outgoing emails to protect sender domain reputation.
- **Outreach Scope**: Global PhD applications (Computer Science, AI, Bioinformatics, Engineering).

---

### 2. WHAT HAPPENED

#### 2.1 Milestone Log
- **2026-09-23 (Reset & Foundation)**:
  - Scrapped legacy code, obsolete discovery scripts, and forensic audit reports.
  - Backed up all authorized Gemini API keys into root `.env`.
  - Authored the comprehensive 6-document project specification suite.
- **2026-09-23 (Full Stack Build & Validation - Phases 1 to 5)**:
  - **Phase 1 (Workspace & Auth)**: FastAPI JWT authentication, password hashing with passlib/bcrypt, and user models.
  - **Phase 2 (Dashboard & Architecture)**: Built React + Vite dashboard with responsive sidebar, stats overview, theme toggle, and pipeline breakdown.
  - **Phase 3 (CRUD & Detail Dossier)**: Created professor catalog, paper associations, filtering/sorting, and detailed professor dossier view.
  - **Phase 4 (AI Co-Pilot & Outreach Center)**: Built multi-key Gemini rotation pool, research alignment analyzer, cold email drafter, staggered background dispatch queue worker with rate limits, and template variable replacement.
  - **Phase 5 (Testing & Quality Assurance)**:
    - Executed end-to-end integration test (`backend/tests/test_api_flow.py`) with 100% pass rate.
    - Verified Vite client production build (`dist/`) successfully compiles in 2.45s with 0 errors.
    - Seeded initial professor and candidate records (`backend/seed_data.py`).

- **2026-09-24 (GitHub Push & Deployment Preparation)**:
  - Configured remote origin to `https://github.com/myrealrajsumit-glitch/phd-outreach-crm.git`.
  - Pushed all core branches and CRM components to GitHub `main`.
  - Updated `Dockerfile` to dynamically support cloud-provided `$PORT` (Render port 10000, Hugging Face port 7860).
  - Ready for 1-click free deployment on Render.com or manual hosting.

---

### 3. CURRENTLY WORKING

- **Current Status**: All code, configurations, and assets are safely committed and synced to GitHub (`main` branch).
- **GitHub Repository**: `https://github.com/myrealrajsumit-glitch/phd-outreach-crm`
- **Next Steps When Resuming**:
  1. Complete 100% free deployment on [dashboard.render.com](https://dashboard.render.com) (select GitHub repo -> Web Service -> Free tier).
  2. Add environment secrets (`SECRET_KEY`, `ENVIRONMENT=production`, Gemini API keys).
  3. Verify live URL access.

---

### 4. UPDATES

- **Maintenance Protocol**:
  - Update this document after completing each major phase or architectural decision.
  - Remove deprecated notes when new modules replace interim scaffolding.
  - Record any API quota limits or prompt adjustments discovered during live testing.

---

### 5. PURPOSE

- **Maintain Context Across Sessions**: Ensure that future agent and developer sessions immediately understand the project purpose, architecture, and current execution phase.
- **Improve Productivity & Consistency**: Prevent redundant work, accidental deletion of credentials, or deviation from approved design tokens.
- **Ensure Nothing Important Is Forgotten**: Retain critical parameters (rate limits, key rotation policies, delivery safeguards) across long development intervals.
