import pathlib
import click
from texmodules import get_tex_table


@click.command()
@click.argument("file", type=click.File(encoding="utf-8"), nargs=1)
@click.option(
    "-a",
    "--alignment",
    type=click.Choice(["c", "l", "r"]),
    default="c",
    show_default=True,
    help="The alignment option of values in the table. "
    "Valid values: c for center, l for left, r for right.",
)
@click.option(
    "-v", "--vseparator", is_flag=True, help="Add single line vertical separators."
)
@click.option(
    "-h", "--hseparator", is_flag=True, help="Add single line horizontal separators."
)
@click.option(
    "-e",
    "--external-border",
    is_flag=True,
    help="Add a single line external border around the whole table.",
)
def cli(file, alignment, vseparator, hseparator, external_border):
    """
    A function that receives the FILE with the data,
    generates a code in LaTeX, and outputs it in table.tex file.
    Only supported single line for rules.
    """

    # generating the input data
    input_data = []
    for line in file.readlines():
        input_data.append(line.split())

    resp_text = get_tex_table(
        input_data, alignment, vseparator, hseparator, external_border
    )

    output_file = pathlib.Path("artifacts/2_1_table.tex")
    with open(output_file, "w") as f:
        f.write(resp_text)


if __name__ == "__main__":
    cli()
