from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator
from typing import ClassVar, List
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_commit_message(prompt: str | None, commit_type: str, diff: str) -> str:
    system_prompt = {
        "role": "system",
        "content": (
            "You are an assistant that writes clear, conventional git commit messages. "
            "Do not include the commit type (e.g., feat:, fix:, refactor:) — the system "
            "will add it later. Your message must have this format:\n\n"
            "Short description sentence of the change.\n"
            "\nChanges:\n"
            "- Specific change 1\n"
            "- Specific change 2\n"
            "- Specific change 3\n\n"
            "Be concise, technical, and specific. Do not use markdown code formatting or backticks.\n\n"
            + (f"User description: {prompt}\n\n" if prompt else "")
            + "Git diff:\n"
            + diff
        ),
    }

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            system_prompt,
            {
                "role": "user",
                "content": (
                    f"Write a commit message (without type prefix) for a '{commit_type}' change. "
                    "Start with a short, imperative description, then include a 'Changes:' list "
                    "summarizing key modifications from the diff."
                ),
            },
        ],
    )

    return resp.choices[0].message.content.strip()



class Group(BaseModel):
    type: str
    paths: List[str]

class GroupedDiffs(BaseModel):
    allowed_files: ClassVar[List[str]] = []
    groups: List[Group]

    @field_validator("groups")
    @classmethod
    def ensure_all_files_used(cls, groups):
        """Ensure all provided files are used exactly once."""
        flat = [p for g in groups for p in g.paths]
        missing = [f for f in cls.allowed_files if f not in flat]
        extra = [f for f in flat if f not in cls.allowed_files]
        if missing:
            raise ValueError(f"Missing files: {missing}")
        if extra:
            raise ValueError(f"Invalid files not in allowed list: {extra}")
        return groups

def generate_staging_groups(diff: str, unstaged_paths: list[str]) -> list[dict[str, list[str]]]:
    GroupedDiffs.allowed_files = unstaged_paths  # inject constraint

    response = client.responses.parse(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1"),
        input=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that analyzes a git diff and groups ONLY the provided "
                    "file paths into commit sections. Each section must include:\n"
                    "- `type`: the commit type (feat, fix, refactor, chore, etc.)\n"
                    "- `paths`: array of file paths that belong to this type\n\n"
                    "You must use every provided file path exactly once, assigning each to one type. "
                    "Do not invent or omit files."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Changed files:\n"
                    + "\n".join(unstaged_paths)
                    + "\n\nGit diff:\n"
                    + diff
                ),
            },
        ],
        text_format=GroupedDiffs,
    )

    return [
        {"type": g.type, "paths": g.paths}
        for g in response.output_parsed.groups
    ]



