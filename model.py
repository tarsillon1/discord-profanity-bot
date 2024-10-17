import torch
from transformers import pipeline

model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
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

messages = [
    {"role": "system", "content": "You are a discord user responding to messages. You are also a petty king named BeeBop who is great with the ladies. Do not include authors name in response."},
]

def clean(response: str):
    return response.split(":", 1)[-1].lstrip()

def is_talking_to_bot(sentence: str):
    return "beebop" in sentence.lower()

def respond(author: str, sentence: str):
    messages.append({ "role": "user", "content": author + ": " + sentence })
    response = clean(output(messages))
    messages.append({ "role": "assistant", "content": response })
    return response
