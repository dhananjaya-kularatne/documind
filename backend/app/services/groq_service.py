import os
from groq import Groq

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions using ONLY the provided context. "
    "If the context doesn't contain the answer, say you don't know based on the document. "
    "Be concise and accurate. Do not make up information."
)

def generate_answer(question: str, chunks: list[dict]) -> str:
    """
    Generate a grounded answer using retrieved chunks as context
    chunks: list of {"text":..., "page":...}
    """

    context = "\n\n".join(
        f"[Page {c['page']}]: {c['text']}" for c in chunks
    )

    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

