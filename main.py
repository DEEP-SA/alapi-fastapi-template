from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import traceback
from dotenv import load_dotenv
from alapi_client import ALAPIClient

load_dotenv()

app = FastAPI(title="alAPI RAG Agent")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

client = ALAPIClient(
    api_key=os.getenv("ALAPI_KEY"),
    base_url=os.getenv("ALAPI_BASE_URL", "https://alapi.deep.sa/v1")
)

print(f"Initialized client with Base URL: {client.base_url}")

class QueryRequest(BaseModel):
    collection_id: str
    query: str
    top_k: int = 5

class CreateCollectionRequest(BaseModel):
    name: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return f.read()

@app.get("/collections")
async def get_collections():
    try:
        return client.list_collections()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/collections")
async def create_collection(request: CreateCollectionRequest):
    try:
        return client.create_collection(request.name)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_rag(request: QueryRequest):
    try:
        return client.chat_with_rag(request.collection_id, request.query, request.top_k)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
