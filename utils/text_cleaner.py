import re

def clean_text(text):

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def split_text(text, chunk_size=2):

    # Split by lines first
    lines = text.splitlines()

    cleaned = []

    for line in lines:

        line = line.strip()

        if len(line) > 2:
            cleaned.append(line)

    # If very small report
    if len(cleaned) <= 5:
        return cleaned

    chunks = []

    for i in range(0, len(cleaned), chunk_size):

        chunk = " ".join(
            cleaned[i:i+chunk_size]
        )

        chunks.append(chunk)

    return chunks