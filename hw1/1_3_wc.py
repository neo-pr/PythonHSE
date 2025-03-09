import click


@click.command()
@click.argument("file", type=click.File("rb"), nargs=-1)
def cli(file):
    """
    Simple program that prints newline, word, and byte counts for
    each FILE, and a total line if more than one FILE is specified.
    If no FILE is given, reads from standard input.
    """
    # lists with information for displaying in the result
    lines, words, bytes = [], [], []
    # base variable for width when displaying data
    max_byte = 0

    for f in file:
        content = f.read()
        lines.append(content.count(b"\n"))
        words.append(len(content.split()))
        bytes.append(byte := len(content))

        if byte > max_byte:
            max_byte = byte  # first we get the maximum number of bytes

    # width for displaying data based on number of digits in maximum bytes
    w = len(str(max_byte))
    # Alternate name for displaying stdin
    if len(file) == 1 and file[0].name == "<stdin>":
        w = max(7, w)
        stdin_name = ""
    else:
        stdin_name = "-"

    # displaying the result
    for idx, (line, word, byte) in enumerate(zip(lines, words, bytes)):
        if (name := file[idx].name) == "<stdin>":
            name = stdin_name
        click.echo(f"{line:{w}d} {word:{w}d} {byte:{w}d} {name}")

    # displaying total if more than one file
    if idx > 0:
        click.echo(f"{sum(lines):{w}d} {sum(words):{w}d} {sum(bytes):{w}d} total")


if __name__ == "__main__":
    cli()
