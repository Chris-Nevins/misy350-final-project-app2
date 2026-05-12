import uuid
from typing import List, Dict
from datetime import date

import os


from openai import OpenAI



from dotenv import load_dotenv

if load_dotenv:
    load_dotenv()

api_key = os.getenv("OPEN_AI_KEY")

client = OpenAI(api_key=api_key) if api_key and OpenAI else None

def build_prompt(context_hint: str):
    return "You're an AI Helper for the Employee that oversees the Inventory of PC Parts."\
    f"This is testing {context_hint}"

def get_ai_response(client:OpenAI, chat_history: list, context_hint:str):
    if client is None:
        raise RuntimeError("OpenAI client is not available.")

    prompt = build_prompt(context_hint)

    prompt_message = [
        {
            "role":'system',
            "content":prompt
        }
    ]

    messages = prompt_message + chat_history

    ai_reponse = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        temperature=1
    )

    return ai_reponse.choices[0].message.content
