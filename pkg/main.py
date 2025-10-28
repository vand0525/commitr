import click
from pkg.llm import generate_commit_message, generate_staging_groups
from pkg.git import get_unstaged_diff, get_staged_diff, get_unstaged_paths, unstage_all, stage, commit
from pkg.utils import process_staging_groups

@click.group()
def cli():
  pass

@cli.command()
@click.argument('prompt', required=False)
def commit(prompt):
  unstage_all()
  unstaged_diff = get_unstaged_diff()
  unstaged_paths = get_unstaged_paths()
  staging_groups = generate_staging_groups(unstaged_diff, unstaged_paths)
  process_staging_groups(prompt, staging_groups)

@cli.command()
def config():
  click.echo('Configuring')

if __name__ == '__main__':
  cli()

