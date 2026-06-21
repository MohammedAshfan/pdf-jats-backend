from lxml import etree

def build_jats(data: dict) -> str:
    XLINK = "http://www.w3.org/1999/xlink"
    root = etree.Element("article",
        attrib={
            "article-type": data.get("article_type") or "research-article",
            "dtd-version": "1.3"
        },
        nsmap={"xlink": XLINK}
    )

    front = etree.SubElement(root, "front")
    meta = etree.SubElement(front, "article-meta")

    if data.get("doi"):
        aid = etree.SubElement(meta, "article-id", attrib={"pub-id-type": "doi"})
        aid.text = str(data["doi"])

    tg = etree.SubElement(meta, "title-group")
    etree.SubElement(tg, "article-title").text = str(data.get("title") or "")

    authors = data.get("authors") or []
    if authors:
        cg = etree.SubElement(meta, "contrib-group")
        for author in authors:
            if not isinstance(author, dict):
                continue
            attrs = {"contrib-type": "author"}
            if author.get("corresponding"):
                attrs["corresp"] = "yes"
            contrib = etree.SubElement(cg, "contrib", attrib=attrs)
            name = etree.SubElement(contrib, "name")
            etree.SubElement(name, "surname").text = str(author.get("last") or "")
            etree.SubElement(name, "given-names").text = str(author.get("first") or "")
            if author.get("affiliation"):
                etree.SubElement(contrib, "aff").text = str(author["affiliation"])

    if data.get("abstract"):
        ab = etree.SubElement(meta, "abstract")
        etree.SubElement(ab, "p").text = str(data["abstract"])

    keywords = data.get("keywords") or []
    if keywords:
        kg = etree.SubElement(meta, "kwd-group")
        for kw in keywords:
            if kw:
                etree.SubElement(kg, "kwd").text = str(kw)

    body = etree.SubElement(root, "body")
    sections = data.get("sections") or []
    for section in sections:
        if not isinstance(section, dict):
            continue
        sec = etree.SubElement(body, "sec")
        etree.SubElement(sec, "title").text = str(section.get("heading") or "")
        etree.SubElement(sec, "p").text = str(section.get("content") or "")

    references = data.get("references") or []
    if references:
        back = etree.SubElement(root, "back")
        ref_list = etree.SubElement(back, "ref-list")
        for i, ref in enumerate(references, 1):
            if not isinstance(ref, dict):
                continue
            ref_id = str(ref.get("id") or i)
            ref_el = etree.SubElement(ref_list, "ref", attrib={"id": f"r{ref_id}"})
            mc = etree.SubElement(ref_el, "mixed-citation")
            mc.text = f"{ref.get('authors','')}. {ref.get('title','')}. {ref.get('journal','')}. {ref.get('year','')}."

    return etree.tostring(root, pretty_print=True,
                          xml_declaration=True, encoding="UTF-8").decode()