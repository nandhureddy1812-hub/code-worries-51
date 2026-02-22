import re

def clean_text(text):
    text = text.upper()
    text = re.sub(r"\s+", " ", text)
    return text