import click
from pkg.llm import generate_commit_message
from pkg.git import get_diff, stage, commit

@click.command()
@click.argument('prompt', required=False)
def main(prompt):
  diff = get_diff()
  commit_message = generate_commit_message(prompt, diff)
  stage()
  commit(commit_message)
  click.echo(f"Committed with message:\n{commit_message}")
  