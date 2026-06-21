USER_PROMPT_TEMPLATE = """Extract structured data from this academic paper and return ONLY valid JSON.

CRITICAL RULES:
1. For author names: capture the FULL given name (including middle names). 
   "MD ASHFAN PASHA" → first="MD ASHFAN", last="PASHA"
   "MD KHIMRAN UDDIN" → first="MD KHIMRAN", last="UDDIN"
   The LAST WORD is the surname, everything before is given names.
2. Extract ALL references from the bibliography/references section, even if numbered list.
3. Ignore garbled text like "(cid:6)" — these are PDF encoding artifacts, skip them in section content.
4. Look for references at the end of the paper under headings like "REFERENCES", "Bibliography", "Works Cited".

Return JSON in this exact format:

{{
  "title": "full article title",
  "authors": [
    {{"first": "FULL given names including middle", "last": "ONLY surname (last word)", "affiliation": "", "corresponding": false}}
  ],
  "abstract": "full abstract text",
  "keywords": ["keyword1"],
  "journal": "journal name if found",
  "doi": "DOI if found",
  "pub_date": "publication date if found",
  "article_type": "research-article",
  "sections": [
    {{"heading": "Introduction", "content": "clean text without garbled characters"}}
  ],
  "references": [
    {{"id": "1", "authors": "Smith et al.", "title": "...", "journal": "...", "year": "2021", "doi": ""}}
  ]
}}

PAPER TEXT:
{text}"""