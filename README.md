# pagination

A tiny FastAPI + SQLModel example that demonstrates simple offset-based pagination. This repository was created as a learning project while I implemented pagination for my CoRe project — the code...

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Why I built this](#why-i-built-this)
- [Getting started](#getting-started)
  - [Run locally](#run-locally)
- [API Endpoints](#api-endpoints)
- [Notes](#notes)
- [Contributing](#contributing)

---

## About

This repository contains a small FastAPI service that exposes a Campaign model and demonstrates offset-based pagination on the `GET /campaigns/` endpoint. It uses SQLite (file-based) via SQLModel [...]

## Features

- Simple REST API for Campaign resources
- Offset-based pagination with `page` and `page_size` query parameters
- Examples of create/read/update/delete operations
- Self-contained SQLite database created at startup

## Tech stack

- Python 3.10+
- FastAPI
- SQLModel (SQLAlchemy / Pydantic integration)
- SQLite (local file db)

## Why I built this

This is a copy-pasted learning project: I wanted to learn and experiment with pagination before adding it to my CoRe project. The goal was to prototype the behavior, confirm acceptable defaults an[...]

## Getting started

### Prerequisites

- Python 3.10 or newer
- (optional) `uv` / `uvicorn` to run the app

### Run locally

1. Clone the repository

```bash
git clone https://github.com/Pranav-Pardeshii/pagination.git
cd pagination
```

2. Install dependencies

If you use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python -m pip install -U pip
python -m pip install fastapi sqlmodel uvicorn
```

3. Start the app

```bash
# using uv (if installed)
uv run uvicorn main:app --reload

# or with python -m uvicorn
python -m uvicorn main:app --reload
```

The app runs with a root path of `/api/v1` (see `main.py`). By default the repository will create a `database.db` file in the project root and seed a few Campaign rows on first startup.

## API Endpoints

Base path: `/api/v1`

- GET `/` — health check
  - Response: {"message": "connection successfull!"}

- GET `/campaigns/` — list campaigns with pagination
  - This repository demonstrates two pagination styles in different files:
    - Offset-based (main.py): `page` (int, default=1) and `page_size` (int, default=10)
    - Cursor-based (main_v2.py): `cursor` (opaque string) and `limit` (int, default=10)
  - Offset example:
    - `GET /api/v1/campaigns/?page=1&page_size=10`
    - Response: `{ "data": [ ... campaigns ... ] }`
  - Cursor example (see `main_v2.py`):
    - Request: `GET /api/v1/campaigns/?cursor=<opaque_token>&limit=10`
    - Behavior: the service returns up to `limit` items ordered by `campaign_id`. If more items exist the response includes a `next` URL containing an opaque cursor token.
    - Example response:

      ```json
      {
        "data": [
          { "campaign_id": 101, "name": "Item 101", "due_date": "...", "created_at": "..." },
          { "campaign_id": 102, "name": "Item 102", "due_date": "...", "created_at": "..." }
        ],
        "next": "https://api.example.com/api/v1/campaigns/?cursor=eyJpZCI6IjEwMiJ9&limit=10"
      }
      ```

    - Notes: The cursor token in `main_v2.py` is an opaque base64-encoded JSON payload (server-encoded). Clients should treat it as opaque and pass it back to the `cursor` query param to advance pages.

- GET `/campaigns/{id}` — fetch single campaign
  - Returns 404 if not found

- POST `/campaigns/` — create campaign
  - Body: { "name": "...", "due_date": "ISO timestamp" }
  - Returns created campaign (201)

- PUT `/campaign/{id}` — update campaign
  - Body same as POST
  - Returns updated campaign or 404

- DELETE `/campaign/{id}` — delete campaign (204) or 404 if missing

## Notes

- Pagination here originally used offset-based (SQL LIMIT/OFFSET). For very large or frequently-changing datasets, cursor-based pagination is recommended — this repository now includes a `main_v2.py` example that implements a simple cursor flow.
- `main_v2.py` details:
  - Query parameters: `cursor` (opaque string), `limit` (int, default=10, min 10, max 30 in the example file)
  - Cursors are encoded as a base64 JSON payload containing the last-seen `campaign_id` (treat as opaque).
  - The endpoint returns a `next` URL when there are more results; clients should call that URL or use the `cursor` token to continue paging.
- Best practices: always return items in a deterministic, stable order (for example, `created_at` + `id`) to avoid duplicates or missing items; document any limits and whether `total` counts (if provided) are exact or approximate.
- This project was intentionally small and self-contained for learning; it is not hardened for production usage (no auth, no migrations, no connection pooling tuned for concurrency).

## Contributing

This repository is a personal learning artifact. If you'd like to suggest improvements (examples, better pagination strategies, or tests), open an issue or a pull request.
