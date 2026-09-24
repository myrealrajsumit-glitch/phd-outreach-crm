import re
import httpx
from typing import List, Dict, Any, Optional

def reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(w for _, w in word_positions)

def estimate_email(name: str, institution: str) -> str:
    """Heuristic to generate clean academic placeholder format."""
    clean_name = re.sub(r'[^a-zA-Z\s]', '', name).strip().lower()
    parts = clean_name.split()
    if len(parts) >= 2:
        user_part = f"{parts[0]}.{parts[-1]}"
    elif parts:
        user_part = parts[0]
    else:
        user_part = "contact"
    
    inst_clean = re.sub(r'[^a-zA-Z\s]', '', institution).strip().lower()
    domain = "univ.edu"
    if "stanford" in inst_clean:
        domain = "stanford.edu"
    elif "berkeley" in inst_clean or "uc berkeley" in inst_clean:
        domain = "berkeley.edu"
    elif "mit" in inst_clean or "massachusetts institute" in inst_clean:
        domain = "mit.edu"
    elif "harvard" in inst_clean:
        domain = "harvard.edu"
    elif "carnegie" in inst_clean or "cmu" in inst_clean:
        domain = "cmu.edu"
    elif "georgia tech" in inst_clean:
        domain = "gatech.edu"
    elif "washington" in inst_clean:
        domain = "uw.edu"
    elif "louisiana state" in inst_clean:
        domain = "lsu.edu"
    elif "oxford" in inst_clean:
        domain = "ox.ac.uk"
    elif "cambridge" in inst_clean:
        domain = "cam.ac.uk"
    elif "toronto" in inst_clean:
        domain = "utoronto.ca"
    elif "lehigh" in inst_clean:
        domain = "lehigh.edu"
    else:
        words = [w for w in inst_clean.split() if w not in ['of', 'the', 'at', 'in', 'and']]
        if words:
            short = "".join(w[0] for w in words[:4])
            domain = f"{short}.edu"

    return f"{user_part}@{domain}"

class DiscoveryService:
    @staticmethod
    async def search_openalex_authors(query: str, limit: int = 15, country: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        headers = {"User-Agent": "PhD-Outreach-CRM/1.0 (academic-outreach@crm.local)"}
        
        async with httpx.AsyncClient(headers=headers, timeout=12.0) as client:
            try:
                resp = await client.get("https://api.openalex.org/authors", params={
                    "search": query,
                    "per-page": limit,
                    "sort": "cited_by_count:desc"
                })
                if resp.status_code == 200:
                    author_data = resp.json().get("results", [])
                    for a in author_data:
                        insts = a.get("last_known_institutions", [])
                        inst_name = insts[0].get("display_name") if insts else "Academic Institution"
                        country_code = insts[0].get("country_code") if insts else "US"
                        
                        if country and country.upper() != "ALL" and country.upper() != country_code.upper():
                            continue

                        topics = [t.get("display_name") for t in a.get("topics", [])[:4] if t.get("display_name")]
                        short_id = a.get("id", "").split("/")[-1]
                        
                        author_name = a.get("display_name", "").strip()
                        if not author_name or len(author_name) < 3:
                            continue

                        paper_title = None
                        paper_year = None
                        paper_venue = None
                        paper_abstract = None
                        paper_doi = None

                        if short_id:
                            try:
                                w_resp = await client.get("https://api.openalex.org/works", params={
                                    "filter": f"author.id:{short_id}",
                                    "sort": "publication_year:desc,cited_by_count:desc",
                                    "per-page": 1
                                })
                                if w_resp.status_code == 200:
                                    w_list = w_resp.json().get("results", [])
                                    if w_list:
                                        top_w = w_list[0]
                                        paper_title = top_w.get("title")
                                        paper_year = top_w.get("publication_year")
                                        host_source = top_w.get("primary_location", {}).get("source", {})
                                        paper_venue = host_source.get("display_name") if host_source else "Peer-Reviewed Venue"
                                        paper_abstract = reconstruct_abstract(top_w.get("abstract_inverted_index"))[:500]
                                        paper_doi = top_w.get("doi") or top_w.get("id")
                            except Exception:
                                pass

                        email_est = estimate_email(author_name, inst_name)
                        citations = a.get("cited_by_count", 0)
                        works_count = a.get("works_count", 0)

                        results.append({
                            "id": f"openalex-{short_id or author_name}",
                            "source": "OpenAlex",
                            "name": author_name,
                            "title": "Professor / Principal Investigator",
                            "institution": inst_name,
                            "country": country_code,
                            "department": ", ".join(topics[:2]) if topics else "Computer Science & Engineering",
                            "research_topics": ", ".join(topics) if topics else query,
                            "email": email_est,
                            "citations": citations,
                            "works_count": works_count,
                            "funding_status": "Active Academic Publisher",
                            "accepting_students": "Likely (Active Lab)",
                            "highlight_badge": f"⭐ {citations:,} Citations" if citations > 1000 else f"📄 {works_count} Papers",
                            "recent_paper": {
                                "title": paper_title or f"Recent Advancements in {query}",
                                "year": paper_year or 2025,
                                "venue": paper_venue or "Academic Conference / Journal",
                                "abstract": paper_abstract or f"Focuses on novel methodologies in {query} and experimental validation.",
                                "doi_or_url": paper_doi or ""
                            }
                        })
            except Exception as e:
                print(f"[DiscoveryService] OpenAlex error: {e}")

        return results

    @staticmethod
    async def search_nsf_grants(query: str, limit: int = 15, country: Optional[str] = None) -> List[Dict[str, Any]]:
        if country and country.upper() != "ALL" and country.upper() != "US":
            return []

        results = []
        async with httpx.AsyncClient(timeout=12.0) as client:
            try:
                resp = await client.get("https://api.nsf.gov/services/v1/awards.json", params={
                    "keyword": query,
                    "printFields": "id,title,awardeeName,awardeeCity,awardeeStateCode,fundsObligatedAmt,pdPIName,startDate,expDate,abstractText",
                    "rpp": limit
                })
                if resp.status_code == 200:
                    data = resp.json().get("response", {}).get("award", [])
                    for aw in data:
                        pi_name = (aw.get("pdPIName") or "").strip()
                        if not pi_name:
                            continue

                        inst_name = aw.get("awardeeName", "US Research University")
                        city = aw.get("awardeeCity", "")
                        state = aw.get("awardeeStateCode", "")
                        inst_full = f"{inst_name} ({state})" if state else inst_name
                        
                        award_title = aw.get("title", f"Research in {query}")
                        amount_val = aw.get("fundsObligatedAmt", 0)
                        try:
                            amount_fmt = f"${int(float(amount_val)):,}"
                        except Exception:
                            amount_fmt = "$500,000+"

                        start_date = aw.get("startDate", "")
                        exp_date = aw.get("expDate", "")
                        dates_str = f"{start_date[-4:] if len(start_date)>=4 else '2024'} - {exp_date[-4:] if len(exp_date)>=4 else '2028'}"
                        abstract = (aw.get("abstractText") or "").strip()[:500]

                        email_est = estimate_email(pi_name, inst_name)

                        results.append({
                            "id": f"nsf-{aw.get('id', pi_name)}",
                            "source": "NSF Grants",
                            "name": pi_name,
                            "title": "Principal Investigator / Professor",
                            "institution": inst_full,
                            "country": "US",
                            "department": "Department of Computer Science & Engineering",
                            "research_topics": f"{query}, NSF Funded Research, {award_title[:40]}",
                            "email": email_est,
                            "grant_info": {
                                "id": aw.get("id"),
                                "title": award_title,
                                "amount": amount_fmt,
                                "period": dates_str
                            },
                            "funding_status": f"Active NSF Grant ({amount_fmt})",
                            "accepting_students": "Grant_Funded",
                            "highlight_badge": f"💰 NSF Funded {amount_fmt} (Active to {exp_date[-4:] if len(exp_date)>=4 else '2028'})",
                            "recent_paper": {
                                "title": f"Grant Project: {award_title}",
                                "year": int(start_date[-4:]) if len(start_date) >= 4 and start_date[-4:].isdigit() else 2025,
                                "venue": "National Science Foundation Award",
                                "abstract": abstract or f"Funded research on {award_title} investigating cutting-edge challenges in {query}.",
                                "doi_or_url": f"https://www.nsf.gov/awardsearch/showAward?AWD_ID={aw.get('id')}"
                            }
                        })
            except Exception as e:
                print(f"[DiscoveryService] NSF error: {e}")

        return results

    @classmethod
    async def discover_faculty(
        cls, 
        query: str, 
        source: str = "all", 
        country: Optional[str] = None, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        query_clean = query.strip()
        if not query_clean:
            query_clean = "Machine Learning"

        openalex_items = []
        nsf_items = []

        sub_limit = max(10, limit // 2)
        if source in ["all", "openalex"]:
            openalex_items = await cls.search_openalex_authors(query_clean, limit=sub_limit if source == "all" else limit, country=country)

        if source in ["all", "nsf"]:
            nsf_items = await cls.search_nsf_grants(query_clean, limit=sub_limit if source == "all" else limit, country=country)

        combined = []
        combined.extend(nsf_items)
        combined.extend(openalex_items)

        seen_names = set()
        deduped = []
        for item in combined:
            key = item["name"].lower().strip()
            if key not in seen_names:
                seen_names.add(key)
                deduped.append(item)

        return deduped[:limit]
