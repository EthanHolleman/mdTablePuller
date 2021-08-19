# mdTablePuller
A Python program that recursively searches for tables in markdown files and converts them to individual delimited files.

## Usage

```
python mdTablePuller.py --help
usage: mdTablePuller.py [-h] [--sep SEP] dir out

Recursively search a directory for markdown files containing tables and extract tables as delim files. This program currently just dumps all files into the output directory
without regard to the original file structure.

positional arguments:
  dir         Path to directory to search for tables
  out         Path to directory to write converted tables to

optional arguments:
  -h, --help  show this help message and exit
  --sep SEP   Delimiter to use for converted tables, default is tab.
 ```
 
 Example command.

```
python mdTablePuller.py {directory with markdown files} {output directory}
```

Each table will be extracted as an individual file. Markdown files with multible tables will therefore produce multiple output files. Naming scheme for output tables is below

```
{name of table's parent markdown file}_table_{index (base 1) of table in the file}.{csv | tsv | txt depending on the delimiter your set}
```

This program works best with well formatted markdown tables. Super wacky ones may not work correctly. I recommend installing and using a
markdown formatting program in your text editor.


