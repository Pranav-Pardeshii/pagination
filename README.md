# pagination

A tiny FastAPI + SQLModel example that demonstrates simple offset-based pagination. This repository was created as a learning project while I implemented pagination for my CoRe project — the code here was used to explore approaches and confirm behavior before integrating the feature into the main app.

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

This repository contains a small FastAPI service that exposes a Campaign model and demonstrates offset-based pagination on the `GET /campaigns/` endpoint. It uses SQLite (file-based) via SQLModel so the example is self-contained and easy to run.

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

This is a copy-pasted learning project: I wanted to learn and experiment with pagination before adding it to my CoRe project. The goal was to prototype the behavior, confirm acceptable defaults and limits (page size bounds), and document a minimal, reproducible example.

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
  - Query parameters:
    - `page` (int, default=1, min=1)
    - `page_size` (int, default=10, min=10, max=30)
  - Example:
    - `GET /api/v1/campaigns/?page=1&page_size=10`
  - Response: { "data": [ ... campaigns ... ] }

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

- Pagination here is offset-based (SQL LIMIT/OFFSET). For very large datasets, cursor-based pagination is recommended.
- This project was intentionally small and self-contained for learning; it is not hardened for production usage (no auth, no migrations, no connection pooling tuned for concurrency).

## Contributing

This repository is a personal learning artifact. If you'd like to suggest improvements (examples, better pagination strategies, or tests), open an issue or a pull request.
