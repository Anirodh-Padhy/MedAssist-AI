import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "phi3"

# =========================================================
# GENERAL MEDICAL AI
# =========================================================

def medical_response(
    user_input,
    patient_memory=""
):

    prompt = f"""
You are MedAssist AI,
an intelligent healthcare assistant.

Patient Previous History:
{patient_memory}

Current Patient Input:
{user_input}

Rules:
- Provide safe healthcare guidance
- Keep responses simple
- Mention doctor consultation when necessary
- Personalize responses using patient history
- Do NOT provide final diagnosis

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

# =========================================================
# REPORT EXPLANATION AI
# =========================================================

def explain_medical_report(analysis):

    findings = "\n".join(analysis)

    prompt = f"""
You are a medical AI assistant.

Analyze these medical findings.

Findings:
{findings}

Explain:
1. Possible causes
2. Health concerns
3. Lifestyle guidance
4. Doctor consultation recommendations

Keep response simple and professional.

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