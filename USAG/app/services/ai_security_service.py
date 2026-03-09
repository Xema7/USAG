import google.generativeai as genai
from typing import Any, Dict

from app.core import settings


async def analyze_security(payload: Any) -> Dict[str, Any]:

    if not settings.AI_API_KEY:
        return {"error": "Gemini API key not configured"}

    try:
        genai.configure(api_key=settings.AI_API_KEY)

        model = genai.GenerativeModel(settings.AI_MODEL_NAME)

        prompt = f"""
            You are a senior API security auditor analyzing traffic from an Enterprise Secure API Gateway.

            Your task:
            Analyze the provided API audit logs and detect potential security risks, anomalies, and policy violations.

            Context:
            - The system enforces authentication, role-based access control, rate limiting, and compliance tagging.
            - Logs may include: user_id, role, endpoint, method, status_code, ip_address, compliance_tag, timestamp.

            Security Evaluation Criteria:
            1. Suspicious access patterns (frequent access, unusual endpoints)
            2. Role misuse (admin accessing unexpected routes, user accessing restricted routes)
            3. Excessive 4xx or 5xx responses
            4. Rate-limit abuse patterns
            5. Access to sensitive/restricted compliance endpoints
            6. Repeated failed authentication attempts
            7. Abnormal request timing or bursts
            8. Indicators of injection or malicious payloads (if present)
            9. Unusual IP behavior

            Important:
            - Do NOT assume data not present in logs.
            - Base your analysis strictly on provided information.
            - If insufficient data, state that clearly.

            Logs:
            {payload}

            Return STRICT JSON in this exact structure:

            {{
            "risk_level": "Low | Medium | High",
            "risk_score": 0-100,
            "summary": "Short 2-3 sentence executive summary",
            "observations": [
                "Observation 1",
                "Observation 2"
            ],
            "anomalies_detected": [
                {{
                    "type": "rate_abuse | role_misuse | auth_failure | suspicious_ip | other",
                    "description": "...",
                    "severity": "Low | Medium | High"
                }}
            ],
            "recommendations": [
                {{
                    "priority": "Low | Medium | High",
                    "action": "Clear actionable mitigation step"
                }}
            ]
            }}
            """

        response = model.generate_content(prompt)

        return {
            "analysis": response.text
        }

    except Exception as e:
        return {"error": f"Gemini AI analysis failed: {str(e)}"}