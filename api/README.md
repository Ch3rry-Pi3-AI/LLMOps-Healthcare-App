# 🩺 API – LLMOps Healthcare App

This folder contains the **Python backend** for the LLMOps Healthcare application.
Vercel automatically detects this directory and deploys it as a **serverless FastAPI function**, allowing the frontend to communicate with a secure, low-latency clinical reasoning endpoint.

The backend is responsible for:

* 🔐 **Authenticating requests** via **Clerk**
* 📝 **Receiving visit notes** from the clinician
* 🤖 **Generating structured summaries** using OpenAI
* 📡 **Streaming responses in real time** via SSE
* 🧩 **Preparing future endpoints** (triage, risk flags, medication checks, etc.)

The entrypoint for the backend is:

```
api/index.py
```

This file implements:

* The **FastAPI app**
* The `Visit` Pydantic model
* The OpenAI prompt logic
* Clerk authentication guards
* The `/api` POST endpoint
* The streaming generator that returns incremental content to the UI

## 📦 Dependencies

The backend uses a minimal, efficient set of packages listed in `requirements.txt`:

* `fastapi` – API framework
* `uvicorn` – local development server
* `openai` – model communication
* `fastapi-clerk-auth` – Clerk JWT verification
* `pydantic` – data validation

Vercel installs these automatically when deploying the serverless function.

## 🚀 How the Endpoint Works (High-Level)

1. A signed request from the frontend (Clerk JWT) is sent to `/api`.
2. The request includes:

   * patient name
   * date of visit
   * raw consultation notes
3. The backend:

   * validates the data
   * builds a structured system + user prompt
   * streams OpenAI model output token-by-token
4. The frontend displays the text as it arrives.

This architecture keeps responses **fast**, **secure**, and **clinically formatted**.

## 📁 File Overview

```
api/
└── index.py          # FastAPI application (LLM-powered consultation summariser)
```

If you need additional endpoints in future (e.g., symptom triage, medication checks, model switching), they will also be added inside this folder.
