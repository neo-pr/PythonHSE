FROM python:3.13.2-alpine

WORKDIR /code

# installing tex dependencies
# source: https://github.com/mattmahn/docker-latex/blob/master/Dockerfile
RUN apk add -U make

# dependencies for texlive
RUN apk add -U --repository http://dl-3.alpinelinux.org/alpine/edge/main \
    poppler harfbuzz-icu

# zziplib (found in edge/community repository) is a dependency to texlive-luatex
RUN apk add -U --repository http://dl-3.alpinelinux.org/alpine/edge/community \
    zziplib

# my personnal comment: this ones takes a long time
RUN apk add -U --repository http://dl-3.alpinelinux.org/alpine/edge/testing \
    texlive-full

RUN ln -s /usr/bin/mktexlsr /usr/bin/mktexlsr.pl

# python and base files
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./2*.py .
COPY artifacts/2_1_table.tex artifacts/2_1_table.tex
COPY artifacts/2_2_img.tex artifacts/2_2_img.tex
COPY data data

# when in linux it only works if you run from the main_tex path
WORKDIR artifacts

CMD ["python", "../2_2_tex_pdf.py", "--main_tex_path", ".", "2_1_table.tex", "2_2_img.tex"]
