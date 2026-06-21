import google.genai as genai
import json, os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

SYSTEM_PROMPT = """You are a scientific document parser.
Extract structure from academic paper text and return ONLY valid JSON.
No explanation, no markdown, no code blocks. Raw JSON only."""

USER_PROMPT_TEMPLATE = """Extract the following from this academic paper and return as JSON:

{{
  "title": "full article title",
  "authors": [
    {{"first": "", "last": "", "affiliation": "", "corresponding": false}}
  ],
  "abstract": "full abstract text",
  "keywords": ["keyword1"],
  "journal": "journal name if found",
  "doi": "DOI if found",
  "pub_date": "publication date if found",
  "article_type": "research-article",
  "sections": [
    {{"heading": "Introduction", "content": "..."}}
  ],
  "references": [
    {{"id": "1", "authors": "Smith et al.", "title": "...", "journal": "...", "year": "2021", "doi": ""}}
  ]
}}

PAPER TEXT:
{text}"""

def parse_with_ai(full_text: str) -> dict:
    text = full_text[:12000]
    prompt = SYSTEM_PROMPT + "\n\n" + USER_PROMPT_TEMPLATE.format(text=text)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    raw = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)