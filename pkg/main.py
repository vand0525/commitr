import click
from pkg.llm import generate_commit_message
from pkg.git import get_diff

@click.command()
@click.argument('prompt', default='none')
def main(prompt):
  diff = get_diff()
  commit_message = generate_commit_message(prompt, diff)
  click.echo(commit_message)
  