import os

from huggingface_hub import login
from transformers import pipeline

login(token=os.getenv('HUGGING_FACE_TOKEN'))

explainer = pipeline(
    "text-generation", model="mistralai/Mistral-7B-Instruct-v0.3")


def explain(sentence: str):
    messages = [
        {"role": "system", "content": "You are a chat moderator that explains why a provided sentence is bad. Do not include the original sentence in your response."},
        {"role": "user", "content": sentence},
    ]
    return explainer(messages)
