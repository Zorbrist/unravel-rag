# Unravel RAG

A retrieval-augmented generation (RAG) project. The backend is a FastAPI service that accepts zip uploads, backed by PostgreSQL with the pgvector extension for storing embeddings.

> **Status:** early development. File upload and the database setup are in place; the embedding, retrieval, and frontend parts are not built yet.

## Tech stack

- **Backend:** Python 3.10, [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** PostgreSQL + [pgvector](https://github.com/pgvector/pgvector) (via Docker)
- **Frontend:** not started (`unravel-frontend/` is a placeholder)

## Project structure

```
unravel-rag/
├── unravel-backend/
│   ├── main.py              # FastAPI app (upload endpoint)
│   ├── docker-compose.yaml  # Postgres + pgvector container
│   ├── init.sql             # Enables the vector extension on first start
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variable template
└── unravel-frontend/        # Placeholder
```

## Getting started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose

### 1. Start the database

```bash
cd unravel-backend
docker compose up -d
```

This starts Postgres with pgvector on `localhost:5432`. The `vector` extension is enabled automatically by `init.sql` the first time the container is created.

### 2. Set up the Python environment

```bash
cd unravel-backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.example .env
```

The `.env` file is git-ignored and must never be committed.

### 4. Run the API

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive docs are available at `http://127.0.0.1:8000/docs`.

## API

### `POST /upload_file`

Uploads a `.zip` archive and extracts it to `./uploaded_files` on the server.

| Check | Limit |
| --- | --- |
| File extension | Must be `.zip` |
| Compressed size | Max 50 MB |
| Uncompressed size | Max 250 MB (zip bomb protection) |
| Paths inside the archive | Rejected if they escape the target directory (zip slip protection) |

Example:

```bash
curl -X POST http://127.0.0.1:8000/upload_file \
  -F "file=@my-documents.zip"
```

Success response:

```json
{ "status": "Success", "extracted_to": "/path/to/uploaded_files" }
```

## Roadmap

- [ ] Parse and chunk extracted documents
- [ ] Generate embeddings and store them in pgvector
- [ ] Similarity search / retrieval endpoint
- [ ] LLM answer generation over retrieved context
- [ ] Frontend

## Notes

- The default database credentials in `docker-compose.yaml` are for **local development only**. Change them before deploying anywhere.
- Uploaded and extracted files are git-ignored.