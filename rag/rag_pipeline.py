import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

def generate_medical_answer(
    query,
    context_chunks
):

    context = "\n\n".join(context_chunks)

    context = context[:1200]

    prompt = f"""
You are MedAssist AI, a healthcare assistant.

Rules:
- Answer ONLY using the provided medical context
- Keep responses simple and professional
- Do NOT diagnose diseases
- Recommend consulting doctors when necessary
- Mention emergency care for severe symptoms

Medical Context:
{context}

Question:
{query}

Response:
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json().get(
            "response",
            ""
        )

    except Exception as e:

        return f"AI Error: {str(e)}"