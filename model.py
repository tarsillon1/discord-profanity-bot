import os

import torch
from transformers import pipeline

from dotenv import load_dotenv

load_dotenv()

model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    temperature=0.2,
)

def output(messages, max_new_tokens=256):
    outputs = pipe(
        messages,
        max_new_tokens=max_new_tokens,
    )
    return outputs[0]["generated_text"][-1]['content']

def explain(sentence: str):
    explain_messages = [
        {"role": "user", "content": "Why is this inappropriate? Keep it short: \n\n" + sentence},
    ]
    return output(explain_messages)

system =  {"role": "system", "content": os.getenv("PERSONALITY")}
messages = []

def clean(response: str):
    return response.split(":", 1)[-1].lstrip()

name = os.getenv("NAME")
def is_talking_to_bot(sentence: str):
    return name in sentence.lower()

chat_window = int(os.getenv("CHAT_WINDOW"))
def respond(author: str, sentence: str):
    if len(messages) > chat_window:
        messages.pop(0)
        messages.pop(0)

    messages.append({ "role": "user", "content": author + ": " + sentence })

    all = [system] + messages + [system]

    response = clean(output(all))
    messages.append({ "role": "assistant", "content": response })
    return response
