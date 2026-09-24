# Project Rules, Standards & Guidelines
## PhD Professor Review & Cold Outreach Intelligence CRM

---

### 1. WHAT TO USE

- **Architectural Pattern**: Clean Layered Architecture (`API Routes` ➔ `Service Layer` ➔ `Data Layer / ORM`).
- **Asynchronous Everywhere**: Use `async`/`await` for all I/O operations (database queries via `aiosqlite`, HTTP requests to Gemini API, SMTP email dispatches via `aiosmtplib`).
- **Data Validation & Typing**: Strict Pydantic v2 schemas for all API payloads and response bodies. Python type hints (`typing`) on all functions.
- **Component-Driven UI**: Modular, reusable React components with clean separation of presentation and business logic.
- **Design Tokens & Tailwind CSS**: Stick strictly to predefined design system tokens (colors, padding, font weights) for visual consistency.
- **Official Google GenAI SDK**: Use official Google SDK interfaces for Gemini API communication with multi-key pool rotation.
- **Human-in-the-Loop Email Flow**: Every email draft must be explicitly previewed and approved by the candidate before queuing.

---

### 2. WHAT TO AVOID

- **No Mass Blind Emailing**: Never allow arbitrary blast emailing without individual professor review and email customization.
- **No Hallucinated Citations**: Never allow the AI engine to generate paper citations without supplying the actual paper metadata in the prompt context.
- **No Synchronous Blocking in Async Routes**: Never use `time.sleep()`, synchronous `requests`, or synchronous DB calls inside FastAPI handlers.
- **No Hardcoded Secrets or Keys**: Never commit API keys, JWT secret keys, or email passwords in source code. All secrets must reside exclusively in `.env`.
- **No Monolithic 1000+ Line Files**: Break complex components into focused sub-components and modular services.
- **No Over-Engineering**: Avoid heavyweight message brokers (e.g., Celery, RabbitMQ) or enterprise databases for local candidate workflows. Use standard asyncio background workers and SQLite.

---

### 3. LIBRARIES & DEPENDENCIES

#### Approved Backend Dependencies (`backend/requirements.txt`)
- `fastapi >= 0.110.0`: Primary async REST API web framework.
- `uvicorn[standard] >= 0.28.0`: High-speed ASGI web server.
- `pydantic >= 2.6.0`: Data modeling, validation, and serialization.
- `pydantic-settings >= 2.2.0`: Typed environment variable configuration.
- `sqlalchemy >= 2.0.28`: Modern async SQL toolkit and ORM.
- `aiosqlite >= 0.20.0`: Async SQLite driver.
- `google-genai >= 0.1.0` or `google-generativeai >= 0.4.0`: Official Google Gemini AI SDK.
- `aiosmtplib >= 3.0.1`: Async SMTP client for non-blocking email delivery.
- `passlib[bcrypt] >= 1.7.4`: Password hashing with bcrypt.
- `python-jose[cryptography] >= 3.3.0` or `PyJWT >= 2.8.0`: JWT token encoding/decoding.
- `python-multipart >= 0.0.9`: File and form data parsing.
- `httpx >= 0.27.0`: Async HTTP client for external integrations.
- `pytest >= 8.0.0` & `pytest-asyncio >= 0.23.0`: Unit and integration testing.

#### Approved Frontend Dependencies (`frontend/package.json`)
- `react` & `react-dom` (`^18.2.0`): Core React library.
- `vite` (`^5.1.0`): Build tool and dev server.
- `react-router-dom` (`^6.22.0`): Client-side routing.
- `axios` (`^1.6.7`): HTTP client with request/response interceptors.
- `lucide-react` (`^0.350.0`): Consistent, lightweight UI vector icons.
- `tailwindcss` (`^3.4.1`) & `autoprefixer`: Utility styling engine.
- `react-hot-toast` (`^2.4.1`): Non-intrusive toast notifications.

---

### 4. ERROR HANDLING

- **Standardized API Error Response**: All backend exceptions must return a uniform JSON schema:
  ```json
  {
    "success": false,
    "error_code": "RESOURCE_NOT_FOUND",
    "message": "Professor with ID 42 does not exist.",
    "details": null
  }
  ```
- **Gemini API Rate Limiting & Failover**:
  - In the event of a `429 Too Many Requests` or quota exhaustion on a Gemini key, automatically rotate to the next key in the multi-key pool (`GEMINI_API_KEY_01` through `06`).
  - Implement exponential backoff with jitter (initial retry 2s, max retries 3).
- **SMTP Failure Isolation**:
  - SMTP connection errors must not crash background tasks.
  - Failed dispatches must mark the email record as `FAILED`, log the exact error reason (e.g., `AuthenticationFailed`, `InvalidRecipientDomain`), and notify the user via the UI.
- **Frontend Graceful Degradation**:
  - Display informative UI error states (empty states, retry buttons, toast alerts) instead of blank screens.
  - Form validation errors must be highlighted per-field with clear corrective instructions.

---

### 5. BOUNDARIES OF AI

- **What AI CAN Do**:
  - Summarize professor research papers and extract main contributions.
  - Suggest alignment angles between candidate background and professor lab focus.
  - Draft personalized initial email inquiries and follow-up templates.
  - Polish and critique user-written drafts for tone, grammar, and academic suitability.
  - Calculate research compatibility scores based on objective semantic overlap.
- **What AI CANNOT Do**:
  - **Cannot Autonomously Send Emails**: The AI can never trigger email dispatch without candidate review and explicit user confirmation.
  - **Cannot Fabricate Papers or Grants**: The AI is prohibited from inventing citations or publications. All citations must be referenced from supplied professor paper records.
  - **Cannot Impersonate Professors**: The AI must never simulate or auto-respond on behalf of professors.
  - **Cannot Alter Pipeline Records Unchecked**: The AI serves as an advisory co-pilot, not an autonomous agent that edits user CRM data without permission.

---

### 6. GENERAL RULES

- **Code Style & Formatting**:
  - Python: Adhere strictly to PEP 8 standards. Use `black` and `flake8` guidelines.
  - JavaScript/React: Clean functional components with React Hooks. Explicit prop handling.
- **Naming Conventions**:
  - Python: `snake_case` for variables, functions, and filenames; `PascalCase` for classes and models.
  - JavaScript/React: `camelCase` for variables and functions; `PascalCase` for components and JSX files; `SCREAMING_SNAKE_CASE` for constants.
- **Commit Message Guidelines**:
  - Use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.
  - Provide concise, imperative descriptions (e.g., `feat: implement gemini multi-key rotation pool`).
- **Security & Data Privacy**:
  - Never expose API keys or passwords in frontend code or client bundles.
  - Hash all stored passwords using bcrypt.
  - Ensure JWT tokens have explicit expiration times.
- **Performance & Scalability**:
  - Paginate large lists (e.g., professors, email history).
  - Use indexed fields in SQLite for fast lookup (`email`, `status`, `institution`).
  - Cache static user profile information in memory during active sessions.
- **Testing Rules**:
  - All critical business logic (Gemini rotation, email variable interpolation, status transitions) must have unit test coverage.
  - Test happy paths, edge cases, and network failure modes.
