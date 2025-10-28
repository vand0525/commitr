import click
from pkg.llm import generate_commit_message, generate_staging_groups
from pkg.git import get_unstaged_diff, get_staged_diff, get_unstaged_paths, unstage_all, stage, do_commit
from pkg.utils import process_staging_groups
from pkg.config import save_config, load_config

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
    current = load_config()
    api_key = click.prompt(
        "Enter your OpenAI API key",
        default=current.get("OPENAI_API_KEY", ""),
        hide_input=True,
        show_default=False
    )
    model = click.prompt(
        "Enter default model",
        default=current.get("OPENAI_MODEL", "gpt-4o-mini")
    )
    save_config(api_key, model)

if __name__ == '__main__':
  cli()

