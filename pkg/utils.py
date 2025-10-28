import click
from pkg.llm import generate_commit_message
from pkg.git import stage, get_staged_diff, do_commit

def process_staging_groups(prompt: str | None, staging_groups: list[dict]):
  for i, group in enumerate(staging_groups, start=1):
    type = group["type"]
    paths = group["paths"]

    stage(paths)
    diff = get_staged_diff()

    message = f"[{type}] {generate_commit_message(prompt, type, diff)}"
    click.echo(f"\nCommit #{i}\n{message}\n")
  
    do_commit(message)