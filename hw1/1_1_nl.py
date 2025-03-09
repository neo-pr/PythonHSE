import click


@click.command()
@click.argument("file", type=click.File(encoding="utf-8"), nargs=1)
@click.option(
    "-w", type=int, default=6, help="The width when displaying the line numbers."
)
def cli(file, w):
    """
    Simple program that writes FILE to standard output with line numbers added.
    If no FILE is given, reads from standard input.
    """

    i = 1  # the line counter
    while x := file.readline():
        click.echo(f"{i:{w}d}  {x}", nl=False)
        i += 1


if __name__ == "__main__":
    cli()
