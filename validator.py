import re
from templates import TEMPLATES

def validate_document(text, doc_name):
    template = TEMPLATES.get(doc_name)

    if not template:
        return {}, 0

    text = text.upper()

    matches = 0
    total_checks = len(template["patterns"]) + len(template["keywords"])
    results = {}

    # Keyword check
    for keyword in template["keywords"]:
        if keyword.upper() in text:
            matches += 1

    # Pattern check
    for field, pattern in template["patterns"].items():
        match = re.search(pattern, text)
        if match:
            results[field] = match.group()
            matches += 1
        else:
            results[field] = "Not Found"

    confidence = round((matches / total_checks) * 100, 2)

    return results, confidence