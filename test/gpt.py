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