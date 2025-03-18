import pathlib
import click
from texmodules import get_tex_image


@click.command()
@click.argument("image", nargs=1)
@click.option(
    "-p",
    "--img_position",
    type=click.Choice(["h", "t", "b", "p"]),
    default="h",
    show_default=True,
    help="The alignment of the image in the page.",
)
@click.option(
    "-c",
    "--img_centering",
    is_flag=True,
    default=True,
    show_default=True,
    help="Center the image inside its position or else keep it left.",
)
def cli(image, img_position, img_centering):
    """
    Task 2.2
    A function that receives IMAGE, the image file name,
    and returns the code in LaTeX to generate it.

    img_position parameter tells where in the page to
    place the image. Valid params:
    h for here, t for top, b for bottom, p for special page
    Not supported combinations or ! and H

    The image file should be stored in the parent directory
    in folder data (../data).
    """

    result = get_tex_image(image, img_position, img_centering)
    output_file = pathlib.Path("artifacts/2_2_img.tex")
    with open(output_file, "w") as f:
        f.write(result)


if __name__ == "__main__":
    cli()
