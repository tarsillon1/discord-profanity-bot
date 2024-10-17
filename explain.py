import torch
from transformers import pipeline

model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

def explain(sentence: str):
    messages = [
        {"role": "user", "content": "Why is this inappropriate? Keep it short: \n\n" + sentence},
    ]
    outputs =  pipe(
        messages,
        max_new_tokens=256,
    )
    return outputs[0]["generated_text"][-1]['content']
