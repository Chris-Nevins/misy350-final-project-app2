import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

try:
    from openai import OpenAI
except ModuleNotFoundError:
    OpenAI = None


def _load_environment():
    if load_dotenv is None:
        return

    service_dir = Path(__file__).resolve().parent
    project_dir = service_dir.parent

    for env_path in (
        service_dir / ".env",
        project_dir / ".env",
        project_dir / "ui" / ".env",
    ):
        load_dotenv(env_path)

    load_dotenv()


def _get_api_key():
    return (os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_KEY") or "").strip()


_load_environment()

api_key = _get_api_key()
client = OpenAI(api_key=api_key) if api_key and OpenAI is not None else None

def build_prompt(context_hint: str):
    return "You're an AI Helper for the Employee that oversees the Inventory of PC Parts."\
    f"This is testing {context_hint}"

def _messages_for_openai(chat_history: list):
    valid_roles = {"system", "user", "assistant"}
    messages = []

    for message in chat_history:
        role = message.get("role", "assistant")
        messages.append(
            {
                "role": role if role in valid_roles else "assistant",
                "content": message.get("content", ""),
            }
        )

    return messages


def get_ai_response(client, chat_history: list, context_hint:str):
    if client is None:
        raise RuntimeError("OpenAI client is not available.")

    prompt = build_prompt(context_hint)

    prompt_message = [
        {
            "role":'system',
            "content":prompt
        }
    ]

    messages = prompt_message + _messages_for_openai(chat_history)

    ai_reponse = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        temperature=1
    )

    return ai_reponse.choices[0].message.content
