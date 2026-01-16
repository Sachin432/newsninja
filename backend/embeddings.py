import os
import requests
from typing import List, Union
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
HF_API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{HF_EMBEDDING_MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}


def embed_text(texts: Union[str, List[str]]):
    """
    Generate embeddings using Hugging Face Inference API.

    Args:
        texts: Single string or list of strings

    Returns:
        List[List[float]] embeddings
    """
    if isinstance(texts, str):
        texts = [texts]

    payload = {
        "inputs": texts,
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(
        HF_API_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"HuggingFace API error {response.status_code}: {response.text}"
        )

    embeddings = response.json()

    # Mean pooling if token-level embeddings are returned
    if isinstance(embeddings[0][0], list):
        embeddings = [
            [sum(col) / len(col) for col in zip(*sentence)]
            for sentence in embeddings
        ]

    return embeddings
