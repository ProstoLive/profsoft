import re


def _tail_words(text: str, overlap: int) -> str:
    if overlap <= 0 or not text:
        return ""

    tail = text[-overlap:]
    space_idx = tail.find(" ")
    if space_idx != -1:
        tail = tail[space_idx + 1:]
    return tail.strip()


def split_text(text: str, size: int, overlap: int) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    sentences = []
    for paragraph in paragraphs:
        sentences.extend(re.split(r"(?<=[.!?])\s+", paragraph))
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    current = ""
    for sentence in sentences:
        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) > size and current:
            chunks.append(current)
            tail = _tail_words(current, overlap)
            current = f"{tail} {sentence}".strip() if tail else sentence
        else:
            current = candidate

    if current:
        chunks.append(current)

    return chunks
