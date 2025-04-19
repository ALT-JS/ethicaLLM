import json
import openai
from tqdm import tqdm
import os

openai.api_key = "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"

def get_response(sentences):
    prompt = "1"
    system = "2"
    prompt += "\n".join(sentences)
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        max_tokens = 15000,
        temperature = 0.7
    )
    
    ans = response['choices'][0]['message']['content']
    
    return ans