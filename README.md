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

## Configuration & Secrets
When deploying on Hugging Face Spaces, configure these in **Settings → Variables and Secrets**:
- `GEMINI_API_KEY_01` through `GEMINI_API_KEY_06`
- `SECRET_KEY`
- `ENVIRONMENT` (set to `production`)
