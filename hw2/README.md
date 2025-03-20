### 2_1

Команда для запуска первой задачи (2_1):

```
PS > uv run 2_1_tex_table.py data/table_data_2_1.txt -v -h -e
```

### 2_2

Команды для запуска второй задачи (2_2):

Сгенерировать изображение в латехе:
2_2_tex_img.py 'png file name'
```
PS > uv run 2_2_tex_img.py universe
```

Сгенерировать main.tex и pdf:
2_2_tex_pdf.py 'path to tex table' 'path to tex img'
```
PS > uv run 2_2_tex_pdf.py "artifacts/2_1_table.tex" "artifacts/2_2_img.tex"
```

**Артефакт 1**
2_2_main.pdf

**Артефакт 2**
Ссылка на репозиторий в Pypi в файле artifacts/linkpypi.txt:
https://pypi.org/project/texesm/


### 2_3

Команда для запуска третьей задачи (2_3):

```
$ docker compose up
```

(сделано в WSL)
Результат сохранён как в папке артефактов
2_2_main_docker.pdf