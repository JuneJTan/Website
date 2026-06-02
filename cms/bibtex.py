import re


TYPE_MAP = {
    "article": "journal",
    "inproceedings": "conference",
    "conference": "conference",
    "proceedings": "conference",
    "book": "book",
    "inbook": "book",
    "incollection": "book",
    "phdthesis": "conference",
    "mastersthesis": "conference",
    "misc": "workshop",
    "unpublished": "workshop",
    "techreport": "workshop",
}


def parse_bibtex(text):
    entries = []
    index = 0
    while True:
        start = text.find("@", index)
        if start == -1:
            break
        open_pos = text.find("{", start)
        if open_pos == -1:
            break

        depth = 0
        end = None
        for pos in range(open_pos, len(text)):
            char = text[pos]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = pos
                    break
        if end is None:
            break

        raw_entry = text[start : end + 1]
        parsed = parse_entry(raw_entry)
        if parsed:
            entries.append(parsed)
        index = end + 1
    return entries


def parse_entry(raw_entry):
    match = re.match(r"@\s*(\w+)\s*\{\s*([^,]+)\s*,(.*)\}\s*$", raw_entry, re.S)
    if not match:
        return None

    entry_type = match.group(1).lower()
    key = match.group(2).strip()
    body = match.group(3)
    fields = parse_fields(body)
    fields["entry_type"] = entry_type
    fields["key"] = key
    return fields


def parse_fields(body):
    fields = {}
    index = 0
    while index < len(body):
        match = re.search(r"([A-Za-z][\w-]*)\s*=", body[index:])
        if not match:
            break
        name = match.group(1).lower()
        value_start = index + match.end()
        value, next_index = read_value(body, value_start)
        if value is not None:
            fields[name] = clean_value(value)
        index = next_index
    return fields


def read_value(body, index):
    while index < len(body) and body[index].isspace():
        index += 1
    if index >= len(body):
        return None, len(body)

    if body[index] == "{":
        depth = 0
        start = index + 1
        for pos in range(index, len(body)):
            if body[pos] == "{":
                depth += 1
            elif body[pos] == "}":
                depth -= 1
                if depth == 0:
                    return body[start:pos], skip_comma(body, pos + 1)
    elif body[index] == '"':
        start = index + 1
        escaped = False
        for pos in range(start, len(body)):
            if body[pos] == "\\" and not escaped:
                escaped = True
                continue
            if body[pos] == '"' and not escaped:
                return body[start:pos], skip_comma(body, pos + 1)
            escaped = False
    else:
        start = index
        pos = index
        while pos < len(body) and body[pos] not in ",\n":
            pos += 1
        return body[start:pos], skip_comma(body, pos)

    return None, len(body)


def skip_comma(body, index):
    while index < len(body) and body[index].isspace():
        index += 1
    if index < len(body) and body[index] == ",":
        index += 1
    return index


def clean_value(value):
    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value).strip()
    replacements = {
        r"\&": "&",
        r"\'{a}": "á",
        r"\'{e}": "é",
        r"\'{i}": "í",
        r"\'{o}": "ó",
        r"\'{u}": "ú",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    value = re.sub(r"[{}]", "", value)
    return value


def format_authors(author_field):
    if not author_field:
        return ""
    authors = [part.strip() for part in re.split(r"\s+and\s+", author_field) if part.strip()]
    normalized = []
    for author in authors:
        if "," in author:
            last, first = [part.strip() for part in author.split(",", 1)]
            author = f"{first} {last}".strip()
        normalized.append(author)
    if len(normalized) > 6:
        return ", ".join(normalized[:6]) + ", et al."
    return ", ".join(normalized)


def publication_type_for(entry):
    return TYPE_MAP.get(entry.get("entry_type", ""), "journal")


def format_raw_citation(entry):
    authors = format_authors(entry.get("author", ""))
    title = entry.get("title", "").rstrip(".")
    venue = entry.get("journal") or entry.get("booktitle") or entry.get("publisher") or entry.get("school") or entry.get("institution")
    year = entry.get("year", "")
    volume = entry.get("volume", "")
    number = entry.get("number", "")
    pages = entry.get("pages", "")

    parts = []
    if authors:
        parts.append(authors)
    if title:
        parts.append(f'"{title},"')
    if venue:
        parts.append(venue)
    if volume:
        parts.append(f"vol. {volume}")
    if number:
        parts.append(f"no. {number}")
    if pages:
        parts.append(f"pp. {pages}")
    if year:
        parts.append(str(year))

    citation = ", ".join(parts).strip()
    if citation and not citation.endswith("."):
        citation += "."
    return citation


def publication_defaults(entry):
    year = entry.get("year", "")
    return {
        "title": entry.get("title") or entry.get("key", "Untitled"),
        "authors": format_authors(entry.get("author", "")),
        "publication_type": publication_type_for(entry),
        "venue": entry.get("journal") or entry.get("booktitle") or entry.get("publisher") or "",
        "year": int(year) if str(year).isdigit() else None,
        "volume": entry.get("volume", ""),
        "issue": entry.get("number", ""),
        "pages": entry.get("pages", ""),
        "doi": entry.get("doi", ""),
        "external_url": entry.get("url", ""),
        "raw_citation": format_raw_citation(entry),
        "is_visible": True,
    }
