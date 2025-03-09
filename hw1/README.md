Все тесты проведены в Windows PowerShell

Список команд для каждой задачи

### 1_1 

```
uv run 1_1_nl.py data/missing_files.txt
uv run 1_1_nl.py data/tale.txt
ls -Name | uv run 1_1_nl.py -
Get-ChildItem -Name | uv run 1_1_nl.py -w 10 -
```

### 1_2 

```
uv run 1_2_tail.py data/missing_files.txt
uv run 1_2_tail.py data/missing_files.txt data/missing_pairs.txt
cat data/missing_files.txt | uv run 1_2_tail.py -
```

### 1_3 

```
uv run 1_3_wc.py data/missing_files.txt
uv run 1_3_wc.py data/missing_files.txt data/missing_pairs.txt data/tale.txt
Get-ChildItem -Name | uv run 1_3_wc.py -
Get-ChildItem -Name | uv run 1_3_wc.py - -
Get-ChildItem -Name | uv run 1_3_wc.py data/tale.txt -
```