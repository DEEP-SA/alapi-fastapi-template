# alAPI RAG FastAPI Starter Template

A ready-to-use FastAPI starter template for building RAG (Retrieval-Augmented Generation) agents using the [alAPI](https://github.com/DEEP-SA/alAPI) service.

## Overview

This starter project provides a minimal FastAPI application with a built-in Chat UI that demonstrates how to integrate with alAPI's RAG endpoints. It includes:

- **Chat UI**: A simple, clean interface for chatting with your documents.
- **Collection Management**: Create and switch between RAG collections.
- **RAG Chat**: Query your document collections with natural language.

## Features

- FastAPI-based REST API
- Built-in Chat UI (no complex frontend framework required)
- RAG-powered question answering
- Python Client wrapper (`alapi_client.py`) for easy integration

## Prerequisites

- Python 3.8 or higher
- An alAPI account with API key
- alAPI service running (self-hosted or cloud instance)

## Installation

### Option 1: Using `uv` (Recommended)

If you have `uv` installed:

```bash
uv run main.py
```

This will automatically handle dependencies and start the server.

### Option 2: Standard pip

1. Clone the repository:
   ```bash
   git clone https://github.com/DEEP-SA/alapi-fastapi-template.git
   cd alapi-fastapi-template
   ```

## Configuration

1. Create a `.env` file in the project root:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:

   ```env
   ALAPI_KEY=your_api_key_here
   ALAPI_BASE_URL=https://alapi.deep.sa/v1
   ```

   **Note**: Replace `your_api_key_here` with your actual alAPI API key.

## Usage

### Start the Server

**Using uv (Recommended):**
```bash
uv run main.py
```

**Using standard python:**
Ensure dependencies are installed first (`pip install .`), then:
```bash
python main.py
```

The application will be available at **`http://localhost:8000`**.

### Using the Chat UI

1. Open `http://localhost:8000` in your browser.
2. Create a new collection using the sidebar.
3. Select the collection to start chatting.
4. **Note**: To upload documents, please use the [alAPI Dashboard](https://dev.alapi.deep.sa/dashboard).

### API Endpoints

#### 1. List Collections

Get all available RAG collections:

```http
GET /collections
```

#### 2. Create Collection

Create a new RAG collection:

```http
POST /collections
Content-Type: application/json

{
  "name": "My Knowledge Base"
}
```

#### 3. Ask RAG

Query a collection with a question:

```http
POST /ask
Content-Type: application/json

{
  "collection_id": "collection-123",
  "query": "What is the main topic?",
  "top_k": 5
}
```

### Programmatic File Uploads

While the UI directs users to the Dashboard for uploads, the `ALAPIClient` class in `alapi_client.py` includes an `upload_document` method if you wish to implement programmatic uploads in your own scripts:

```python
from alapi_client import ALAPIClient
import os

client = ALAPIClient(api_key=os.getenv("ALAPI_KEY"), base_url=...)
client.upload_document(collection_id="...", file_path="./my-doc.pdf")
```

## Project Structure

```
alapi-rag-starter/
├── main.py              # FastAPI application & endpoints
├── alapi_client.py      # Python wrapper for alAPI RAG endpoints
├── static/              # Static files for Chat UI
│   └── index.html       # Single-page Chat UI
├── pyproject.toml       # Project metadata & dependencies
├── .env                 # Environment variables
└── README.md            # Documentation
```

## License

This starter template is provided as-is for use with the alAPI service.
