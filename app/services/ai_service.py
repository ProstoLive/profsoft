from app.ai.client import client
from app.core.config import settings

ALLOWED_LABELS = {"positive", "negative", "neutral"}


def classify(text: str) -> str:
    if settings.TEST_MODE:
        return "neutral"

    response = client.chat.completions.create(
        model=settings.MODEL,
        messages=[
            {"role": "system", "content": settings.PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    label = response.choices[0].message.content.strip().lower()

    if label not in ALLOWED_LABELS:
        return "neutral"
    return label
