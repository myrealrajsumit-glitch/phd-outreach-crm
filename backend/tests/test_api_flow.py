import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import init_db

@pytest.mark.asyncio
async def test_full_system_flow():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Health check
        res = await ac.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["active_gemini_keys"] >= 1
        print("[PASS] Health check verified, active keys:", data["active_gemini_keys"])

        # 2. Register candidate user
        import uuid
        test_email = f"candidate.test.{uuid.uuid4().hex[:6]}@stanford.edu"
        reg_res = await ac.post("/api/auth/register", json={
            "email": test_email,
            "password": "SecurePassword123!",
            "full_name": "Sumit Raj",
            "target_field": "Computer Science & Artificial Intelligence",
            "current_degree": "M.S. in Computer Science",
            "research_interests": "Large Language Models, Distributed Systems, Multi-Agent Systems",
            "cv_summary": "First-author paper at NeurIPS workshop. Extensive research in LLM agent orchestration and RLHF."
        })
        assert reg_res.status_code == 200
        token_data = reg_res.json()
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("[PASS] Registration successful for:", token_data["user"]["full_name"])

        # 3. Create Professor with Paper
        prof_res = await ac.post("/api/professors", headers=headers, json={
            "name": "Dr. Andrew Ng",
            "email": "ang@cs.stanford.edu",
            "institution": "Stanford University",
            "department": "Computer Science",
            "title": "Adjunct Professor",
            "homepage_url": "https://www.andrewng.org",
            "country": "USA",
            "research_topics": "Deep Learning, Autonomous Agents, Data-Centric AI",
            "accepting_students": "Yes",
            "papers": [
                {
                    "title": "Agentic Design Patterns for LLMs",
                    "year": 2024,
                    "venue": "DeepLearning.AI Tech Report",
                    "abstract": "Analysis of reflection, tool use, planning, and multi-agent collaboration patterns that significantly enhance LLM problem-solving accuracy."
                }
            ]
        })
        assert prof_res.status_code == 200
        prof = prof_res.json()
        prof_id = prof["id"]
        print("[PASS] Professor added:", prof["name"], "at", prof["institution"])

        # 4. AI Research Review
        print("Testing Gemini AI Research Review...")
        ai_review_res = await ac.post("/api/ai/review", headers=headers, json={
            "professor_id": prof_id
        })
        assert ai_review_res.status_code == 200
        review = ai_review_res.json()
        assert review["match_score"] > 0
        assert len(review["discussion_questions"]) > 0
        print(f"[PASS] AI Research Review generated. Match Score: {review['match_score']}/10. Questions: {len(review['discussion_questions'])}")

        # 5. AI Cold Email Draft
        print("Testing Gemini AI Cold Email Drafting...")
        ai_draft_res = await ac.post("/api/ai/draft-email", headers=headers, json={
            "professor_id": prof_id,
            "tone": "Formal Academic",
            "word_count": 200
        })
        assert ai_draft_res.status_code == 200
        draft_content = ai_draft_res.json()
        assert len(draft_content["subject"]) > 5
        assert len(draft_content["body"]) > 50
        print("[PASS] AI Draft generated. Subject:", draft_content["subject"])

        # 6. Save email draft
        save_draft_res = await ac.post("/api/emails", headers=headers, json={
            "professor_id": prof_id,
            "subject": draft_content["subject"],
            "body": draft_content["body"]
        })
        assert save_draft_res.status_code == 200
        draft_obj = save_draft_res.json()
        draft_id = draft_obj["id"]
        print("[PASS] Email draft saved to CRM with ID:", draft_id)

        # 7. Dashboard Stats
        stats_res = await ac.get("/api/stats/dashboard", headers=headers)
        assert stats_res.status_code == 200
        stats = stats_res.json()
        assert stats["overview"]["total_professors"] >= 1
        print("[PASS] Dashboard statistics verified:", stats["overview"])

if __name__ == "__main__":
    asyncio.run(test_full_system_flow())
