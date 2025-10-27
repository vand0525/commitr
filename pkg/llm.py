from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_commit_message(desc: str, diff: str) -> str:
  system_prompt = get_system_prompt(desc, diff)
  resp = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL"),
    messages=[system_prompt, {"role": "user", "content": "Generate the commit message now."}]
  )
  return resp.choices[0].message.content

def get_system_prompt(desc: str, diff: str) -> dict:
    return {
        "role": "system",
        "content": (
            "You are an AI assistant that writes high-quality, conventional "
            "git commit messages. Use the user description"
            "and diff to generate a concise commit message.\n\n"
            f"User description: {desc}\n\n"
            "Project diff (unstaged changes):\n"
            f"{diff}"
        ),
    }