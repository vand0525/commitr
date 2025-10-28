import click
from pkg.llm import generate_commit_message, generate_staging_groups
from pkg.git import get_unstaged_diff, get_staged_diff, get_unstaged_paths, unstage_all, stage, commit

@click.command()
@click.argument('prompt', required=False)
def main(prompt):
  unstage_all()
  unstaged_diff = get_unstaged_diff()
  unstaged_paths = get_unstaged_paths()
  staging_groups = generate_staging_groups(unstaged_diff, unstaged_paths)
  process_staging_groups(prompt, staging_groups)

def process_staging_groups(prompt: str | None, staging_groups: list[dict]):
  for i, group in enumerate(staging_groups, start=1):
    type = group["type"]
    paths = group["paths"]

    stage(paths)
    diff = get_staged_diff()

    message = f"[{type}] {generate_commit_message(prompt, type, diff)}"
    click.echo(f"\nCommit #{i}\n{message}\n")
  
    commit(message)

def say_hello():
  print('hello')


