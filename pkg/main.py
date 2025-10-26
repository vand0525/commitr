import click
from pkg.llm import generate_commit_messgae

@click.command()
@click.option('--type', type=click.Choice(['feat', 'refactor', 'fix']), prompt=True)
@click.option('--desc', prompt="Describe your changes")
def main(type, desc):
  commit_message = generate_commit_messgae(type, desc)
  click.echo(commit_message)
  