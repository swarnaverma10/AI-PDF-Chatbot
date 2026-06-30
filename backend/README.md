# AI PDF Chatbot – Backend

> **Phase 1 – FastAPI Foundation**  
> A production-ready FastAPI backend that will power an AI-driven PDF question-answering chatbot for a Unity 6 frontend.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | FastAPI 0.115 |
| ASGI Server | Uvicorn |
| Config / Validation | Pydantic v2 + pydantic-settings |
| Env Variables | python-dotenv |
| AI (Phase 2+) | OpenRouter API via httpx |
| PDF Reading (Phase 3+) | pdfplumber |
| Frontend (separate) | Unity 6 |

---

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app factory, routes, lifespan hooks
│   ├── config.py        # Settings loaded from .env (Pydantic BaseSettings)
│   ├── models.py        # Pydantic request / response schemas
│   ├── utils.py         # Logging setup, shared helpers
│   ├── chatbot.py       # Chatbot service (Phase 2+ stub)
│   └── pdf_reader.py    # PDF reader service (Phase 3+ stub)
├── knowledge_base/
│   └── AI_Knowledge_Base.pdf
├── .env                 # Local environment variables (not committed)
├── .env.example         # Template – copy to .env and fill in values
├── requirements.txt     # Pinned Python dependencies
└── README.md            # This file
```

---

## Prerequisites

- Python **3.11** or newer
- `pip` (comes with Python)
- *(Recommended)* A virtual environment tool such as `venv` or `conda`

---

## Setup Instructions

### 1 – Clone / navigate to the project

```bash
# If you have not cloned the repo yet:
git clone <repo-url>
cd AI-PDF-Chatbot/backend
```

### 2 – Create and activate a virtual environment

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3 – Install dependencies

```bash
pip install -r requirements.txt
```

### 4 – Configure environment variables

```bash
# Windows (PowerShell)
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` in your editor and update any values you need to change.  
For **Phase 1** the defaults work out of the box — no API keys are required yet.

### 5 – Run the development server

```bash
# From the backend/ directory:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the built-in entry point:

```bash
python -m app.main
```

The server will start at **http://localhost:8000**.

---

## API Endpoints (Phase 1)

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Welcome message + docs URL |
| `GET` | `/health` | Service health check |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | ReDoc API documentation |

### Example responses

**GET /**
```json
{
  "message": "Welcome to the AI PDF Chatbot API!",
  "version": "1.0.0",
  "docs_url": "/docs"
}
```

**GET /health**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-06-30T09:45:00.000000+00:00"
}
```

---

## CORS

CORS is pre-configured to allow requests from Unity's default development
origins (`localhost:8080`, `127.0.0.1:8080`, etc.).  
To customise the allowed origins, update the `ALLOWED_ORIGINS` list in
`.env` or directly in `app/config.py`.

---

## Logging

Structured logs are written to **stdout** in the format:

```
2026-06-30T09:45:00 | INFO     | app.main | Starting AI PDF Chatbot v1.0.0 | debug=False
```

Control verbosity with the `LOG_LEVEL` environment variable  
(`DEBUG` | `INFO` | `WARNING` | `ERROR` | `CRITICAL`).

---

## Roadmap

| Phase | Feature | Status |
|---|---|---|
| **1** | FastAPI foundation, CORS, health endpoint | ✅ Complete |
| **2** | OpenRouter API integration + chat endpoint | 🔜 Planned |
| **3** | pdfplumber PDF ingestion + context retrieval | 🔜 Planned |
| **4** | Unity 6 frontend integration | 🔜 Planned |

---

## Contributing

1. Create a feature branch off `main`.
2. Follow the existing code style (docstrings, type hints, structured logging).
3. Run the test suite before opening a PR: `pytest tests/`.
4. Keep each PR focused on a single concern.
