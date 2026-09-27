---
title: PhD Professor Outreach CRM
emoji: 🎓
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# PhD Professor Review & Cold Outreach Intelligence CRM

An academic relationship management platform and AI-powered cold outreach intelligence CRM for PhD applicants.

## Features
- **Professor Review & Dossier**: Deep dive into research focus, recent papers, and alignment metrics.
- **AI Cold Outreach Co-Pilot**: Multi-key Google Gemini rotation pool for generating tailored cold emails.
- **Safe Staggered Queue**: Automated rate limits and randomized delay to maintain sender reputation.
- **FastAPI + React 18**: High performance asynchronous Python backend serving a modern Tailwind-styled Single Page Application.

---

## 🚀 Deployment (Vercel)

> **Deployment = Vercel.** The React frontend is deployed on Vercel. The FastAPI backend runs separately (locally or on Hugging Face Spaces).

### Step 1 — Import Repository into Vercel
1. Go to [vercel.com](https://vercel.com) → **Add New Project** → Import your GitHub repository.
2. Vercel auto-detects `vercel.json` automatically:
   - **Framework**: Vite
   - **Build Command**: `npm --prefix frontend run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `npm --prefix frontend install`

### Step 2 — Set All Environment Variables in Vercel

In your Vercel Project → **Settings → Environment Variables**, add **all** of the following:

#### 🔵 Frontend Config (required for the UI to reach your backend)
| Variable | Value | Notes |
|---|---|---|
| `VITE_API_BASE_URL` | `https://your-backend.hf.space/api` | **Critical** — URL of your live FastAPI backend + `/api` |

#### 🟢 App & Server Config
| Variable | Value |
|---|---|
| `ENVIRONMENT` | `production` |
| `LOG_LEVEL` | `INFO` |
| `HOST` | `0.0.0.0` |
| `PORT` | `5555` |
| `BACKEND_PORT` | `5555` |
| `FRONTEND_PORT` | `5566` |
| `LOCAL_BACKEND_URL` | `https://your-backend.hf.space` |
| `LOCAL_FRONTEND_URL` | `https://your-app.vercel.app` |

#### 🔐 Security
| Variable | Value |
|---|---|
| `SECRET_KEY` | A long random secret string (never share) |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |

#### 🤖 Gemini AI Keys (from [Google AI Studio](https://aistudio.google.com))
| Variable | Value |
|---|---|
| `GEMINI_API_KEY_01` | Your Gemini API key #1 |
| `GEMINI_API_KEY_02` | Your Gemini API key #2 |
| `GEMINI_API_KEY_03` | Your Gemini API key #3 |
| `GEMINI_MODEL` | `gemini-2.0-flash` |

#### 🔀 OpenRouter (optional fallback AI)
| Variable | Value |
|---|---|
| `OPENROUTER_API_KEY` | Your OpenRouter API key |

#### 📧 Gmail SMTP (for email dispatch)
| Variable | Value |
|---|---|
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | `your_email@gmail.com` |
| `SMTP_PASSWORD` | Your Gmail App Password (16-char) |
| `SMTP_FROM_EMAIL` | `your_email@gmail.com` |
| `SMTP_FROM_NAME` | `Your Name` |
| `SMTP_USE_TLS` | `true` |

### Step 3 — Deploy
Click **Deploy**. Vercel builds and publishes your frontend. Every `git push` to `main` triggers an automatic re-deployment.

---

## 🖥️ Local Development

```bash
# Backend
backend\.venv\Scripts\python.exe backend/run_server.py

# Frontend (in a separate terminal)
cd frontend && npm run dev
```

Copy `.env.example` → `.env` and fill in your credentials for local use.

---

## ⚙️ Architecture

| Layer | Technology | Hosted On |
|---|---|---|
| Frontend | React 18 + Vite + Tailwind | **Vercel** |
| Backend API | FastAPI + Python | Hugging Face Spaces / Local |
| Database | SQLite (aiosqlite) | Co-located with backend |
| AI | Gemini multi-key pool | Google AI Studio |

