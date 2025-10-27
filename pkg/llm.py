from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_commit_message(prompt: str | None, diff: str) -> str:
  system_prompt = get_system_prompt(prompt, diff)
  resp = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL"),
    messages=[system_prompt, {"role": "user", "content": "Generate the commit message now."}]
  )
  return resp.choices[0].message.content

def get_system_prompt(prompt: str | None, diff: str) -> dict:
    return {
        "role": "system",
        "content": (
            "You are an AI assistant that writes high-quality, conventional"
            "git commit messages. Do not use backticks. You generate based on the following:\n\n"
            + (f"User description: {prompt}\n\n" if prompt is not None else "")
            + "Project diff (unstaged changes):\n"
            + diff
        ),
    }