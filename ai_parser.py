import google.genai as genai
import json
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

PROMPT = """You are a scientific document parser. Extract structured data from this academic paper and return ONLY valid JSON. No explanation, no markdown, no code blocks.

CRITICAL RULES:
1. For author names: capture the FULL given name (including middle names). The LAST WORD is the surname, everything before is given names. Example: "MD ASHFAN PASHA" splits as first="MD ASHFAN", last="PASHA".
2. Extract ALL references from the bibliography section.
3. Ignore garbled text like "(cid:6)" in content.

Return JSON with these exact keys: title, authors (list of objects with first, last, affiliation, corresponding), abstract, keywords (list), journal, doi, pub_date, article_type, sections (list of objects with heading, content), references (list of objects with id, authors, title, journal, year, doi).

PAPER TEXT:
"""

def parse_with_ai(full_text: str) -> dict:
    text = full_text[:20000]
    prompt = PROMPT + text
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    raw = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)