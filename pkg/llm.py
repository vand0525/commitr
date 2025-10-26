from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_commit_messgae(type: str, desc: str, diff: str) -> str:
  system_prompt = get_system_prompt(diff, type, desc)
  resp = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL"),
    messages=[system_prompt, {"role": "user", "content": "Generate the commit message now."}]
  )
  return resp.choices[0].message.content

def get_system_prompt(diff: str, type: str, desc: str) -> dict:
    """
    Builds the complete system message for the OpenAI API.

    Combines the unstaged diff, the commit type, and the user's description
    into a single structured system message.
    """
    return {
        "role": "system",
        "content": (
            "You are an AI assistant that writes high-quality, conventional "
            "git commit messages. Use the provided commit type, user description, "
            "and diff to generate a concise commit message.\n\n"
            f"Commit type: {type}\n"
            f"User description: {desc}\n\n"
            "Project diff (unstaged changes):\n"
            f"{diff}"
        ),
    }