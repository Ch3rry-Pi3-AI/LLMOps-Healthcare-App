"""
api/index.py

FastAPI backend entrypoint for the LLMOps Healthcare App.

This module exposes a single POST endpoint at `/api` which:

1. Authenticates incoming requests using Clerk-issued JWTs via `fastapi-clerk-auth`.
2. Accepts a `Visit` payload containing patient name, date of visit, and free-text notes.
3. Constructs a carefully controlled system and user prompt for the OpenAI model.
4. Streams the model's response back to the client using Server-Sent Events (SSE),
   formatted as `text/event-stream`, so that the UI can render tokens incrementally.

The model is instructed to return exactly three sections:

- Summary of visit for the doctor's records
- Next steps for the doctor
- Draft of email to patient in patient-friendly language
"""

# ==========================
# Standard library imports
# ==========================

# Provides access to environment variables (e.g. CLERK_JWKS_URL)
import os
from typing import Iterator

# ==========================
# Third-party imports
# ==========================

# FastAPI framework for building the HTTP API
from fastapi import FastAPI, Depends  # type: ignore
# Response type for streaming Server-Sent Events (SSE)
from fastapi.responses import StreamingResponse  # type: ignore
# Pydantic base class for request/response models
from pydantic import BaseModel  # type: ignore
# Clerk configuration and auth guard for protecting the endpoint
from fastapi_clerk_auth import (  # type: ignore
    ClerkConfig,
    ClerkHTTPBearer,
    HTTPAuthorizationCredentials,
)
# OpenAI client for calling LLMs
from openai import OpenAI  # type: ignore


# ==========================
# FastAPI application setup
# ==========================

# Create the main FastAPI application instance
app = FastAPI()

# Read the Clerk JWKS URL from environment variables for JWT verification
clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))

# Create a reusable HTTP bearer auth guard using the Clerk configuration
clerk_guard = ClerkHTTPBearer(clerk_config)


# ==========================
# Data models
# ==========================

class Visit(BaseModel):
    """
    Request model representing a single patient visit.

    Parameters
    ----------
    patient_name : str
        Name of the patient whose consultation is being summarised.
    date_of_visit : str
        Date of the clinical visit, typically formatted as a human-readable string
        (for example, '2025-11-22' or '22 November 2025').
    notes : str
        Free-text notes written by the doctor during or after the visit.
        These should include relevant history, examination findings, and plan.
    """
    # Name of the patient for whom the consultation is being summarised
    patient_name: str
    # Date on which the patient attended their visit
    date_of_visit: str
    # Raw consultation notes written by the clinician
    notes: str


# ==========================
# Prompt templates
# ==========================

# System-level instructions that define the assistant's behaviour and output format
system_prompt = """
You are provided with notes written by a doctor from a patient's visit.
Your job is to summarize the visit for the doctor and provide an email.
Reply with exactly three sections with the headings:
### Summary of visit for the doctor's records
### Next steps for the doctor
### Draft of email to patient in patient-friendly language
"""


def user_prompt_for(visit: Visit) -> str:
    """
    Build the user prompt for a given patient visit.

    The prompt includes the patient's name, date of visit, and raw clinical notes.
    This is combined with the system prompt to guide the model to produce a structured,
    clinically useful summary and patient email.

    Parameters
    ----------
    visit : Visit
        The visit object containing patient name, visit date, and clinical notes.

    Returns
    -------
    str
        A formatted prompt string that is passed to the OpenAI chat completion API.
    """
    # Construct a formatted string that embeds the visit details into the user message
    return f"""Create the summary, next steps and draft email for:
Patient Name: {visit.patient_name}
Date of Visit: {visit.date_of_visit}
Notes:
{visit.notes}"""


# ==========================
# API endpoints
# ==========================

@app.post("/api")
def consultation_summary(
    visit: Visit,
    creds: HTTPAuthorizationCredentials = Depends(clerk_guard),
) -> StreamingResponse:
    """
    Generate a streamed consultation summary and patient email for a given visit.

    This endpoint:
    1. Uses Clerk to authenticate the incoming request.
    2. Constructs system and user prompts from the visit data.
    3. Calls the OpenAI chat completion API with streaming enabled.
    4. Converts the token stream into Server-Sent Events (SSE) and returns a
       `StreamingResponse` with `text/event-stream` MIME type.

    Parameters
    ----------
    visit : Visit
        The visit payload containing `patient_name`, `date_of_visit`, and `notes`.
    creds : HTTPAuthorizationCredentials, optional
        Credentials object produced by `ClerkHTTPBearer`, containing the decoded JWT.
        This is injected by FastAPI via `Depends(clerk_guard)`.

    Returns
    -------
    StreamingResponse
        A streaming HTTP response where each line is an SSE `data:` frame containing
        fragments of the model's response.
    """
    # Extract the Clerk user ID from the decoded JWT for auditing / logging (not used yet)
    user_id = creds.decoded["sub"]  # Available for tracking/auditing

    # Create a new OpenAI client instance using environment configuration
    client = OpenAI()

    # Build the user-level prompt that incorporates visit details
    user_prompt = user_prompt_for(visit)

    # Construct the full chat prompt with system and user messages
    prompt = [
        # System message that defines the assistant's role and required output format
        {"role": "system", "content": system_prompt},
        # User message that includes the specific visit details
        {"role": "user", "content": user_prompt},
    ]

    # Call the OpenAI chat completion API with streaming enabled
    stream = client.chat.completions.create(
        # Model identifier (small, low-latency model suitable for streaming)
        model="gpt-5-nano",
        # Full conversation messages (system + user)
        messages=prompt,
        # Enable token-by-token streaming from the API
        stream=True,
    )

    # ==========================
    # SSE streaming generator
    # ==========================

    def event_stream() -> Iterator[str]:
        """
        Convert the OpenAI streaming response into an SSE-compatible token stream.

        The OpenAI client yields chunks where each chunk may contain a fragment
        of the final response. This generator:

        - Extracts `delta.content` from each chunk.
        - Splits the text on newline characters.
        - For each line (except the last), sends:
          * `data: <line>\n\n`
          * `data:  \n` (an empty line to preserve paragraph spacing)
        - Sends the final line as `data: <last_line>\n\n`.

        Yields
        ------
        Iterator[str]
            Strings formatted according to the Server-Sent Events protocol,
            ready to be streamed back to the client.
        """
        # Iterate over each streamed chunk from the OpenAI API
        for chunk in stream:
            # Extract the incremental text content for this chunk
            text = chunk.choices[0].delta.content
            # Only proceed if the chunk actually contains text
            if text:
                # Split the text into individual lines on newline characters
                lines = text.split("\n")
                # Process all lines except the last one
                for line in lines[:-1]:
                    # Emit the line as an SSE data frame followed by a blank line
                    yield f"data: {line}\n\n"
                    # Emit an extra empty data line to represent a visual line break
                    yield "data:  \n"
                # Emit the final line as a standard SSE data frame
                yield f"data: {lines[-1]}\n\n"

    # Wrap the generator in a StreamingResponse with the SSE media type
    return StreamingResponse(event_stream(), media_type="text/event-stream")
