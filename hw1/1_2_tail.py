import click
from collections import deque


@click.command()
@click.argument("file", type=click.File(encoding="utf-8"), nargs=-1)
def cli(file):
    """
    Simple program that prints the last 10 lines of each FILE to standard output.
    With more than one FILE, precede each with a header giving the file name.
    If no FILE is given, reads the last 17 lines from standard input.
    """
    # last n lines: 17 if input is stdin or 10 if file(s)
    n = 17 if file[0].name == "<stdin>" and len(file) == 1 else 10

    for f in file[:-1]:
        click.echo(f"==> {f.name} <==")
        for line in deque(f, n):
            click.echo(line, nl=False)
        click.echo()

    if len(file) > 1:
        click.echo(f"==> {file[-1].name} <==")

    for line in deque(file[-1], n):
        click.echo(line, nl=False)


if __name__ == "__main__":
    cli()
