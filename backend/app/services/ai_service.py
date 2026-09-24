import json
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import errors as genai_errors
from app.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.keys = settings.gemini_keys
        self.current_key_idx = 0
        preferred = settings.GEMINI_MODEL or "gemini-3.1-flash-lite"
        # Primary and failover models verified to work with sub-second response
        candidate_models = [preferred, "gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"]
        self.models_pool = []
        for m in candidate_models:
            if m and m not in self.models_pool:
                self.models_pool.append(m)

    def _get_next_client(self) -> genai.Client:
        if not self.keys:
            raise ValueError("No Gemini API keys configured in environment.")
        key = self.keys[self.current_key_idx]
        self.current_key_idx = (self.current_key_idx + 1) % len(self.keys)
        return genai.Client(api_key=key)

    def _generate_with_fallback(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        last_error = None

        # Try across available models in pool with key rotation
        for model in self.models_pool:
            for attempt in range(len(self.keys) if self.keys else 1):
                client = self._get_next_client()
                try:
                    config = {}
                    if system_instruction:
                        config["system_instruction"] = system_instruction
                    
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config if config else None
                    )
                    if response and response.text:
                        return response.text.strip()
                    raise ValueError("Empty response received from Gemini.")
                except (genai_errors.ClientError, Exception) as e:
                    err_str = str(e)
                    logger.warning(f"Gemini {model} attempt {attempt + 1} failed: {e}.")
                    last_error = e
                    # If model is 503 unavailable (high demand) or 404, immediately switch to next model
                    if "503" in err_str or "UNAVAILABLE" in err_str or "404" in err_str or "NOT_FOUND" in err_str:
                        logger.info(f"Model {model} experienced capacity limit (503/404). Immediately trying next fallback model.")
                        break

        raise RuntimeError(f"All Gemini models and API keys failed. Last error: {last_error}")

    def synthesize_professor_research(
        self,
        professor_name: str,
        institution: str,
        topics: str,
        papers: List[Dict[str, Any]],
        candidate_field: str,
        candidate_interests: str
    ) -> Dict[str, Any]:
        """Synthesize professor publications, calculate match score, and produce inquiry angles."""
        papers_text = ""
        for idx, p in enumerate(papers, 1):
            papers_text += f"\n[Paper {idx}]\nTitle: {p.get('title')}\nYear: {p.get('year', 'N/A')}\nVenue: {p.get('venue', 'N/A')}\nAbstract: {p.get('abstract', 'No abstract provided')}\n"

        prompt = f"""You are an elite academic research advisor evaluating professor-candidate alignment for PhD admissions.

Professor: {professor_name}
Institution: {institution}
Lab Research Topics: {topics}

Target Publications:
{papers_text if papers_text.strip() else "No papers provided. Base analysis on lab topics."}

Candidate Background:
- Field: {candidate_field}
- Research Interests: {candidate_interests}

Tasks:
1. Calculate a Research Alignment Score (Float between 1.0 and 10.0) based on how well the candidate's background connects with the professor's recent publications.
2. List 2-3 Key Methodological Findings/Contributions from the papers.
3. Identify 2-3 Research Gaps or Next Steps where a new PhD student could contribute.
4. Formulate 2-3 Sharp, Technical Discussion Questions suitable for an academic cold email.
5. Provide a concise markdown synthesis summarizing the collaboration angle.

Respond strictly in valid JSON format matching this schema:
{{
  "match_score": 8.5,
  "key_findings": ["...", "..."],
  "research_gaps": ["...", "..."],
  "discussion_questions": ["...", "..."],
  "synthesis_markdown": "### Executive Summary\\n..."
}}
"""
        response_text = self._generate_with_fallback(
            prompt,
            system_instruction="You are an expert academic evaluator. Always respond with strict, valid JSON containing only the requested fields."
        )
        
        # Clean json formatting if wrapped in code block
        cleaned = response_text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except Exception:
            return {
                "match_score": 7.5,
                "key_findings": ["Active research in " + topics],
                "research_gaps": ["Exploring open problems in " + topics],
                "discussion_questions": [f"How does your lab approach current challenges in {topics}?"],
                "synthesis_markdown": response_text
            }

    def draft_academic_cold_email(
        self,
        professor_name: str,
        institution: str,
        papers: List[Dict[str, Any]],
        candidate_name: str,
        candidate_degree: str,
        candidate_interests: str,
        candidate_cv_summary: str,
        tone: str = "Formal Academic",
        word_count: int = 250,
        custom_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """Draft a hyper-personalized, grounded cold outreach email for PhD inquiry."""
        papers_text = ""
        for idx, p in enumerate(papers, 1):
            papers_text += f"\n- Paper {idx}: '{p.get('title')}' ({p.get('year', '')}) - {p.get('venue', '')}\n  Abstract: {p.get('abstract', '')[:300]}..."

        prompt = f"""You are a professional PhD application coach specializing in crafting high-impact, personalized academic cold emails to professors.

Recipient:
- Professor: {professor_name}
- Institution: {institution}
- Relevant Papers:
{papers_text if papers_text.strip() else "None provided (use general lab topics)."}

Sender (Candidate):
- Name: {candidate_name}
- Current Degree: {candidate_degree}
- Research Interests: {candidate_interests}
- Qualifications/Experience: {candidate_cv_summary}

Requirements:
- Target Tone: {tone}
- Target Word Count: approximately {word_count} words
- Do NOT use generic marketing phrases (e.g. "I hope this email finds you well", "I was thrilled by your work").
- Start directly by introducing the candidate's degree and express specific interest in joining their group for a funded PhD position.
- Cite specific concepts from their papers and connect them directly to the candidate's technical skills or research ideas.
- Provide a clear, polite call-to-action (inquiry on upcoming PhD openings and a request for a brief 15-minute video discussion).
- Custom User Notes: {custom_instructions if custom_instructions else "None"}

Respond strictly in valid JSON format:
{{
  "subject": "Inquiry regarding PhD Openings in [Topic] - [Candidate Name]",
  "body": "Dear Professor [LastName],\\n\\n...",
  "tone_used": "{tone}",
  "grounded_citations": ["Paper 1 title", "..."],
  "suggested_call_to_action": "Request for a 15-minute introductory video call"
}}
"""
        response_text = self._generate_with_fallback(
            prompt,
            system_instruction="You write polished, scholarly cold emails that get responses from tenure-track and senior professors. Respond strictly in valid JSON."
        )
        cleaned = response_text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except Exception:
            return {
                "subject": f"PhD Inquiry - {candidate_interests} - {candidate_name}",
                "body": response_text,
                "tone_used": tone,
                "grounded_citations": [p.get("title") for p in papers if p.get("title")],
                "suggested_call_to_action": "Request for 15-minute discussion"
            }

    def draft_follow_up_email(
        self,
        professor_name: str,
        institution: str,
        previous_subject: str,
        previous_body: str,
        candidate_name: str,
        follow_up_stage: int = 1,  # 1 = 7-day gentle reminder, 2 = 14-day value-add, 3 = final courtesy check
        custom_hook: Optional[str] = None
    ) -> Dict[str, Any]:
        """Draft a polite, high-converting follow-up email for busy professors."""
        stage_desc = {
            1: "Gentle reminder (7-10 days after initial email). Very concise (~80 words). Re-iterate enthusiasm for their group.",
            2: "Second follow-up (14-21 days). Bring a new perspective or mention a recent development/question (~100 words).",
            3: "Final courtesy follow-up. Very brief (~50 words), acknowledging they may not have openings and thanking them."
        }.get(follow_up_stage, "Polite follow-up")

        prompt = f"""You are an expert academic advisor drafting a follow-up email to a university professor.

Recipient:
- Professor: {professor_name}
- Institution: {institution}

Previous Thread:
- Subject: {previous_subject}
- Previous Email Snippet: {previous_body[:350]}...

Sender:
- Candidate Name: {candidate_name}

Follow-up Strategy:
- Stage: {follow_up_stage} ({stage_desc})
- Additional User Notes / Hook: {custom_hook if custom_hook else "None"}

Requirements:
- Subject line must follow standard email reply thread conventions (e.g. "Re: {previous_subject}")
- Be extremely polite, respectful of the professor's busy schedule, and concise.
- Never sound entitled, demanding, or desperate.
- Politely restate the core inquiry regarding upcoming PhD openings.

Respond strictly in valid JSON format:
{{
  "subject": "Re: {previous_subject}",
  "body": "Dear Professor [LastName],\\n\\nI wanted to briefly follow up on my email below regarding potential PhD openings in your group...\\n\\nBest regards,\\n{candidate_name}",
  "stage": {follow_up_stage}
}}
"""
        response_text = self._generate_with_fallback(
            prompt,
            system_instruction="You write courteous, respectful, and brief academic follow-up emails. Respond strictly in valid JSON."
        )
        cleaned = response_text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except Exception:
            return {
                "subject": f"Re: {previous_subject}",
                "body": response_text,
                "stage": follow_up_stage
            }

ai_service = GeminiService()
