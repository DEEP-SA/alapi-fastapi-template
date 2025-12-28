import requests
import os
from typing import List, Dict, Any

class ALAPIClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def list_collections(self) -> List[Dict[str, Any]]:
        resp = requests.get(f"{self.base_url}/rag/collections", headers=self.headers)
        resp.raise_for_status()
        return resp.json().get("collections", [])

    def create_collection(self, name: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}/rag/collections",
            headers=self.headers,
            json={"name": name}
        )
        resp.raise_for_status()
        return resp.json()

    def upload_document(self, collection_id: str, file_path: str) -> Dict[str, Any]:
        # 1. Get Presigned URL
        filename = os.path.basename(file_path)
        presigned_resp = requests.post(
            f"{self.base_url}/rag/collections/{collection_id}/presigned-url",
            headers=self.headers,
            json={"filename": filename}
        )
        presigned_resp.raise_for_status()
        presigned_data = presigned_resp.json()

        # 2. Upload to S3
        with open(file_path, "rb") as f:
            upload_resp = requests.put(presigned_data["presigned_url"], data=f)
            upload_resp.raise_for_status()

        # 3. Confirm Upload
        confirm_payload = {
            "document_id": presigned_data["document_id"],
            "s3_path": presigned_data["s3_path"],
            "filename": filename,
            "size": os.path.getsize(file_path)
        }
        confirm_resp = requests.post(
            f"{self.base_url}/rag/collections/{collection_id}/confirm-upload",
            headers=self.headers,
            json=confirm_payload
        )
        confirm_resp.raise_for_status()
        return confirm_resp.json()

    def chat_with_rag(self, collection_id: str, query: str, top_k: int = 5) -> Dict[str, Any]:
        payload = {
            "collection_id": collection_id,
            "query": query,
            "top_k": top_k
        }
        resp = requests.post(f"{self.base_url}/rag/chat", headers=self.headers, json=payload)
        resp.raise_for_status()
        return resp.json()
