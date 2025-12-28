import requests
url = "http://localhost:8080/v1/rag/chat"
headers = {"Authorization": "Bearer sk-alapi-e6d996e0393e3ee3e36dc602e669fe5c93d3b020401731b9845716b465208cba"}
payload = {
    "collection_id": "aefea5db-b94a-4fce-becb-db77e74bc8ad",
    "query": "ماهو نظام المعاملات؟",
    "top_k": 5
}
response = requests.post(url, headers=headers, json=payload)
print(response.json()["answer"])