cat > jats_builder.py << 'EOF'
from lxml import etree

def build_jats(data: dict) -> str:
    root = etree.Element("article", attrib={
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "article-type": data.get("article_type", "research-article"),
        "dtd-version": "1.3"
    })

    front = etree.SubElement(root, "front")
    meta = etree.SubElement(front, "article-meta")

    if data.get("doi"):
        aid = etree.SubElement(meta, "article-id", attrib={"pub-id-type": "doi"})
        aid.text = data["doi"]

    tg = etree.SubElement(meta, "title-group")
    etree.SubElement(tg, "article-title").text = data.get("title", "")

    cg = etree.SubElement(meta, "contrib-group")
    for author in data.get("authors", []):
        attrs = {"contrib-type": "author"}
        if author.get("corresponding"):
            attrs["corresp"] = "yes"
        contrib = etree.SubElement(cg, "contrib", attrib=attrs)
        name = etree.SubElement(contrib, "name")
        etree.SubElement(name, "surname").text = author.get("last", "")
        etree.SubElement(name, "given-names").text = author.get("first", "")
        if author.get("affiliation"):
            etree.SubElement(contrib, "aff").text = author["affiliation"]

    if data.get("abstract"):
        ab = etree.SubElement(meta, "abstract")
        etree.SubElement(ab, "p").text = data["abstract"]

    if data.get("keywords"):
        kg = etree.SubElement(meta, "kwd-group")
        for kw in data["keywords"]:
            etree.SubElement(kg, "kwd").text = kw

    body = etree.SubElement(root, "body")
    for section in data.get("sections", []):
        sec = etree.SubElement(body, "sec")
        etree.SubElement(sec, "title").text = section.get("heading", "")
        etree.SubElement(sec, "p").text = section.get("content", "")

    if data.get("references"):
        back = etree.SubElement(root, "back")
        ref_list = etree.SubElement(back, "ref-list")
        for ref in data["references"]:
            ref_el = etree.SubElement(ref_list, "ref", attrib={"id": f"r{ref['id']}"})
            mc = etree.SubElement(ref_el, "mixed-citation")
            mc.text = f"{ref.get('authors','')}. {ref.get('title','')}. {ref.get('journal','')}. {ref.get('year','')}."

    return etree.tostring(root, pretty_print=True,
                          xml_declaration=True, encoding="UTF-8").decode()
EOF