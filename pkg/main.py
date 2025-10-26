import click
from pkg.llm import generate_commit_messgae
from pkg.git import get_diff

@click.command()
@click.option('--type', type=click.Choice(['feat', 'refactor', 'fix']), prompt=True)
@click.option('--desc', prompt="Describe your changes")
def main(type, desc):
  diff = get_diff()
  commit_message = generate_commit_messgae(type, desc, diff)
  click.echo(commit_message)
  