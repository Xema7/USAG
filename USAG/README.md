🚀 Universal Secure API Gateway (USAG)

A plug-and-play security middleware layer for backend services.

USAG acts as a protective gateway in front of any backend system and automatically provides:

        JWT Authentication

        Role-Based Access Control (RBAC)

        Rate Limiting

        Audit Logging

        Compliance Tagging

        AI-Powered Security Risk Analysis (Gemini)

        Request Validation

        Centralized Security Enforcement

🏗️ Architecture Overview

Client → USAG (Security Gateway) → Target Backend Service

The gateway intercepts every request and applies:

    1. Authentication

    2. Authorization

    3. Rate limiting

    4. Compliance tagging

    5. AI risk analysis

    6. Audit logging

    7. Forwarding to backend

This design makes it easy to secure any existing backend service without modifying its internal logic.

🔐 Security Features
1️⃣ JWT Authentication

Validates tokens using configurable secret key

Supports role extraction from token payload

Rejects invalid or expired tokens

2️⃣ Role-Based Access Control

Differentiates between admin and user

Restricts sensitive endpoints (e.g., audit logs)

3️⃣ Rate Limiting

Configurable requests per minute

Prevents brute-force and DoS attacks

Returns HTTP 429 on limit breach

4️⃣ Audit Logging

Every request logs:

    user_id

    role

    endpoint

    HTTP method

    status code

    risk_level

    compliance_tag

    timestamp

    response time

Logs are stored in MongoDB.

5️⃣ Compliance Tagging

Each route is tagged for compliance classification:

    Internal

    Public

    Sensitive

This enables enterprise audit reporting.

6️⃣ AI Security Analysis (Gemini)

Suspicious payloads are analyzed using Google Gemini API.

The AI returns:

    1. risk_level (Low / Medium / High)

    2. observations

    3. recommendations

This transforms static logging into intelligent threat detection.

🧠 AI Prompt Strategy

The system uses a structured security prompt that:

    Analyzes API payloads

    Detects injection patterns

    Identifies malicious behavior

    Generates mitigation suggestions

    Returns structured JSON output

Designed for deterministic and consistent risk evaluation.

🛠️ Tech Stack

Python 3.12+

FastAPI

MongoDB

Pydantic v2

JWT (PyJWT)

Google Gemini API

Uvicorn

📂 Project Structure
    USAG/
    │
    ├── app/
    │   ├── core/
    │   ├── middleware/
    │   ├── routes/
    │   ├── services/
    │   ├── db/
    │   ├── models/
    │   └── main.py
    │
    ├── sample_backend/
    ├── test/
    ├── generate_token.py
    ├── .env
    └── README.md

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone <repo-url>
cd USAG
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Setup MongoDB

Ensure MongoDB is running locally:

mongodb://localhost:27017
4️⃣ Configure Environment Variables

Create .env file:

JWT_SECRET_KEY=your_secret_key
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=secure_gateway_db
RATE_LIMIT_PER_MINUTE=10
AI_PROVIDER=gemini
AI_API_KEY=your_gemini_api_key
AI_MODEL_NAME=gemini-2.5-flash
TARGET_BACKEND_URL=http://localhost:9000

⚠️ Never commit .env file.

🚀 Running the Gateway

Start backend service (if using sample backend): uvicorn sample_backend.main:app --port 9000

Start gateway: uvicorn app.main:app --reload

Gateway runs at: http://127.0.0.1:8000

🧪 Postman Test Flow
1️⃣ Health Check
GET /health
2️⃣ Access Protected Route Without Token
GET /users

Expected: 401 Unauthorized

3️⃣ Generate Token
python generate_token.py
4️⃣ Access With User Token

Add header:

Authorization: Bearer <token>
5️⃣ Access Admin-Only Endpoint

Test role enforcement.

6️⃣ Trigger Rate Limit

Send rapid repeated requests → Expect 429.

7️⃣ AI Risk Analysis

Send suspicious payload → Receive structured risk analysis.

📊 Audit Data Example

Stored log example:

{
  "user_id": "test_user",
  "role": "admin",
  "endpoint": "/users",
  "status_code": 200,
  "risk_level": "Low",
  "compliance_tag": "Internal",
  "timestamp": "...",
  "response_time_ms": 120
}
🧩 Design Philosophy

USAG is built as:

Modular

Middleware-driven

Backend-agnostic

Enterprise-ready

AI-enhanced

It can be integrated in front of:

Microservices

REST APIs

Internal enterprise systems

Third-party backend services

🏆 Hackathon Value Proposition

This project demonstrates:

Secure API architecture

Centralized security enforcement

Intelligent threat detection

Compliance-aware logging

Scalable middleware design

Production-ready configuration management

🔒 Security Considerations

All secrets stored in .env

JWT expiration enforced

Rate limiting configurable

Audit logs persistent

AI responses structured and controlled

No sensitive data exposed in logs

🧪 Testing

Run unit tests:

pytest

Covers:

Authentication

Authorization

Rate limiting

Compliance enforcement

Health endpoint

📌 Future Enhancements

Multi-tenant support

Distributed rate limiting (Redis)

Admin analytics UI

Threat scoring history tracking

Webhook alerts for high-risk events

OpenAPI-based auto compliance tagging

📄 License


MIT License
