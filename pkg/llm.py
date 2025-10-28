import click
from typing import ClassVar, List
from pydantic import BaseModel, field_validator
from openai import OpenAI
from pkg.config import load_config

def get_client():
    """Safely initialize and return the OpenAI client."""
    cfg = load_config()
    api_key = cfg.get("OPENAI_API_KEY")
    if not api_key:
        click.echo("Missing OpenAI API key. Run 'commitr config' to set it up.")
        raise click.Abort()
    return OpenAI(api_key=api_key)


def get_model():
    """Return configured model or default fallback."""
    cfg = load_config()
    return cfg.get("OPENAI_MODEL", "gpt-4o-mini")

def generate_commit_message(prompt: str | None, commit_type: str, diff: str) -> str:
    """Generate a structured commit message using OpenAI."""
    client = get_client()
    model = get_model()

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

    try:
        resp = client.chat.completions.create(
            model=model,
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
    except Exception as e:
        click.echo(f"Error generating commit message: {e}")
        raise click.Abort()

class Group(BaseModel):
    type: str
    paths: List[str]

class GroupedDiffs(BaseModel):
    allowed_files: ClassVar[List[str]] = []
    groups: List[Group]

    @field_validator("groups")
    @classmethod
    def ensure_all_files_used(cls, groups):
        """Ensure every file path is used exactly once."""
        flat = [p for g in groups for p in g.paths]
        missing = [f for f in cls.allowed_files if f not in flat]
        extra = [f for f in flat if f not in cls.allowed_files]
        if missing:
            raise ValueError(f"Missing files: {missing}")
        if extra:
            raise ValueError(f"Invalid files not in allowed list: {extra}")
        return groups


def generate_staging_groups(diff: str, unstaged_paths: list[str]) -> list[dict[str, list[str]]]:
    """Ask the LLM to group diffs into commit sections."""
    client = get_client()
    model = get_model()
    GroupedDiffs.allowed_files = unstaged_paths

    try:
        response = client.responses.parse(
            model=model,
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

        return [{"type": g.type, "paths": g.paths} for g in response.output_parsed.groups]
    except Exception as e:
        click.echo(f"Error generating staging groups: {e}")
        raise click.Abort()




