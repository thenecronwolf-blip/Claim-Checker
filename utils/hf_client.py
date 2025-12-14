# utils/hf_client.py
from huggingface_hub import InferenceClient
import os

client = InferenceClient(token=os.environ.get("HF_API_KEY"))
