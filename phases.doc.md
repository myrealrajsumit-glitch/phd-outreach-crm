# Project Implementation Phases
## PhD Professor Review & Cold Outreach Intelligence CRM

---

### PHASE 1: PERSONAL WORKSPACE & PROFILE INITIALIZATION
- **Single-User Personal Workspace**:
  - Direct, friction-free access to personal PhD CRM workspace without login/password barriers.
  - Automatic candidate session configuration (Sumit Raj, M.S. in Computer Science).
- **Candidate Profile Setup**:
  - Target field specification (Computer Science & AI, Distributed Systems, Multi-Agent Systems).
  - Background credentials, CV summary, and technical specialization.
- **Outreach & Security Credentials**:
  - Local environment-level credential protection via `.env`.
  - Personal SMTP email configuration (Gmail App Password, university email).
  - Multi-key Google Gemini API pool integration (`gemini-3.6-flash`).

---

### PHASE 2: DASHBOARD
- **Create Dashboard Layout**:
  - Sleek modern layout with responsive collapsible sidebar, top navbar, and main content area.
  - Clean breadcrumbs and user profile status badge.
- **Overview Cards / Stats**:
  - Total Target Professors cataloged.
  - Outreach Funnel distribution (Drafts, Queued, Sent, Replied, Interviews).
  - Overall Response Rate (%) and Positive Engagement Rate.
  - Today's Email Dispatch Velocity (e.g., "7 of 25 sent today").
- **Navigation Setup**:
  - Fluid routing across: Dashboard, Professors Directory, Outreach Kanban Pipeline, Email Center & Queue, Candidate Profile, Settings.
- **Basic Data Visualization**:
  - Visual funnel breakdown chart (Identified ➔ Contacted ➔ Responded ➔ Interview).
  - Activity timeline showing recent actions (email sent, review completed, reply logged).

---

### PHASE 3: CRUD OPERATIONS
- **Create, Read, Update, Delete for Main Entities**:
  - **Professors**: Add new faculty, edit lab details, update research topics, archive/delete.
  - **Research Papers**: Attach recent publications to professors with venue, year, abstract, and DOI.
  - **Outreach Emails**: Create email drafts, update content, delete obsolete drafts.
  - **Email Templates**: Create reusable inquiry frameworks with customizable variables.
- **Form Validation**:
  - Strict client-side and server-side schema validation (valid emails, required names, valid URLs).
  - Informative inline field error messages.
- **List & Detail Views**:
  - **List View**: High-density table of professors with quick status badges, institution tags, and action buttons.
  - **Detail View**: Comprehensive professor dossier showing research history, papers, AI synthesis, past correspondence, and notes.
- **Search, Filter & Sort**:
  - Full-text search by professor name, institution, or keyword.
  - Multi-criteria filtering by Pipeline Stage (`Reviewing`, `Sent`, `Replied`), Department, and Country.
  - Sorting by compatibility score, last activity, or follow-up due date.

---

### PHASE 4: ADDITIONAL FEATURES
- **Business Logic & Rules**:
  - **Gemini AI Research & Outreach Co-Pilot**:
    - Multi-key rotation pool for Google Gemini 2.0 Flash.
    - AI paper abstract synthesis and research alignment scoring.
    - Context-aware academic email drafter with customizable tones and word counts.
  - **Intelligent Timed & Batch Sending**:
    - Staggered dispatch queue with 45–120s humanized intervals.
    - Daily velocity throttles to safeguard deliverability.
    - Scheduled send dates and timezone matching.
  - **Automated Follow-Up Reminder Engine**:
    - Auto-flags contacts awaiting response after 7–10 business days.
- **File Upload / Download**:
  - Upload candidate Resume / CV (PDF) and academic transcripts.
  - Automatic CV attachment support during email dispatch.
  - Export CRM records to CSV/JSON format.
- **Notifications / Alerts**:
  - Real-time toast notifications for successful dispatches, AI generation events, and errors.
  - Actionable dashboard alerts for overdue follow-ups.
- **Settings / Preferences**:
  - SMTP / Email configuration (Host, Port, User, App Password, TLS).
  - Gemini API key management (viewing pool status, active model selection).
  - Personal default email signature and variable defaults.

---

### PHASE 5: TESTING & QUALITY ASSURANCE
- **Unit Testing**:
  - Pytest suites for authentication, password hashing, and token validation.
  - Tests for Gemini multi-key rotation and rate-limit retry logic.
  - Tests for email template variable substitution (`{{professor_name}}`, etc.).
- **Integration Testing**:
  - End-to-end API test covering: User registration ➔ Add Professor ➔ Generate AI Draft ➔ Queue Email ➔ Status Update.
  - Mocked SMTP delivery integration tests.
- **Bug Fixing**:
  - Edge-case resolution (special characters in names, missing paper abstracts, invalid emails).
- **Performance Testing**:
  - Fast response times (< 100ms for CRUD endpoints).
  - Smooth UI rendering on lists with 100+ professor records.

---

### PHASE 6: DEPLOYMENT & MAINTENANCE
- **Deployment to Staging & Production**:
  - Clean local runner scripts (`run_server.py`, `npm run dev`) and production build bundling.
  - SQLite database backup and automated migration scripts.
- **User Feedback & Monitoring**:
  - Execution logging with timestamped file logs (`logs/app.log`).
  - Error rate tracking and delivery failure diagnostics.
- **Bug Fixes & Improvements**:
  - Ongoing optimization of Gemini prompt engineering for higher reply rates.
- **Future Enhancements**:
  - Automatic publication fetch via OpenAlex / Google Scholar API.
  - Direct IMAP reply detection to automatically move status to `Replied`.
