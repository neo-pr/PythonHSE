import subprocess
import pathlib
import click
from subprocess import PIPE
from subprocess import STDOUT


@click.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False), nargs=2)
@click.option("--main_tex_path", default="./artifacts", help= "relative path to save the main tex code")
def cli(filename, main_tex_path):
    """
    Task 2.2
    A function that combines two tex FILENAMEs: a table and an image,
    and then generates: the main.tex file and the pdf version.
    tex files should be stored in artifacts folder
    img file should be stored in data folder
    """

    # getting file names
    fnames = [click.format_filename(f, shorten=True).split(".")[0] for f in filename]

    # main tex file generation
    header = """\\documentclass{article}
    \\usepackage[subpreambles=true]{standalone}
    \\usepackage{import}\n\\begin{document}"""
    body = f"""\\import{{.}}{{{fnames[0]}}}\n\\import{{.}}{{{fnames[1]}}}"""

    footer = "\\end{document}"
    res_main_tex = "\n".join([header, body, footer])

    # to place main tex file in the same folder as the others
    main_tex_file = pathlib.Path(main_tex_path).joinpath("2_2_main.tex")

    with open(main_tex_file, "w") as f:
        f.write(res_main_tex)

    # generating the pdf
    # for some weird reason it should be run two times
    for _ in range(2):
        with open(main_tex_file, "rb") as f:
            args = [
                "pdflatex",
                "-output-directory",
                main_tex_path,
                "-job-name",
                "2_2_main",
            ]
            result = subprocess.run(args, input=f.read(), stdout=PIPE, stderr=STDOUT)
            result.check_returncode()


if __name__ == "__main__":
    cli()
