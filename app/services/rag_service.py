from app.ai.client import client
from app.core.config import settings
from app.services.retrieval import search

SYSTEM_PROMPT = (
    "Отвечай на вопрос, используя ТОЛЬКО приведённый ниже контекст. "
    "Если ответа в контексте нет — так и скажи, не выдумывай. "
    "Укажи источник (раздел/документ)."
)


def answer(question: str) -> dict:
    points = search(question, settings.TOP_K)

    if not points:
        return {"answer": "В документации нет информации по этому вопросу.", "sources": []}

    context = "\n\n".join(f"[{point.payload['source']}] {point.payload['text']}" for point in points)

    response = client.chat.completions.create(
        model=settings.CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Контекст:\n{context}\n\nВопрос: {question}"},
        ],
    )

    sources = [{"source": point.payload["source"], "doc_id": point.payload["doc_id"]} for point in points]
    return {"answer": response.choices[0].message.content.strip(), "sources": sources}
