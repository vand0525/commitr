from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system = {"role": "system", "content": "Write a git commit message based on the type and changes"}

def generate_commit_messgae(type: str, desc: str) -> str:
  resp = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL"),
    messages=[system, {"role": "user", "content": f"Commit type: {type}, Described changes: {desc}"}]
  )
  return resp.choices[0].message.content