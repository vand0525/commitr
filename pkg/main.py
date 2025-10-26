import click

@click.command()
@click.option('--type', type=click.Choice(['feat', 'refactor', 'fix']), prompt=True)
@click.option('--desc', prompt="Describe your changes")
def main(type, desc):
  click.echo(f'{type}')
  click.echo(f"{desc}")