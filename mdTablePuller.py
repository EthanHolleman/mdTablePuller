import argparse
import re
from pathlib import Path

# Program to recursively extract markdown tables and convert to delimiated 
# file types.

TABLE_REGEX = r"((\r?\n){2}|^)([^\r\n]*\|[^\r\n]*(\r?\n)?)+(?=(\r?\n){2}|$)"


def get_args():
    '''Parse command line arguments using argparse.
    '''

    parser = argparse.ArgumentParser(
        description="Recursively search a directory for markdown files containing \
            tables and extract tables as delim files. This program currently \
            just dumps all files into the output directory without regard to \
            the original file structure."
    )
    parser.add_argument("dir", help="Path to directory to search for tables")
    parser.add_argument("out", help="Path to directory to write converted tables to")
    parser.add_argument(
        "--sep",
        default="\t",
        help="Delimiter to use for converted tables, default is tab.",
    )

    return parser.parse_args()


def write_tables(target_dir, output_dir, delimiter):
    '''Extract and write markdown tables to text files. Recursively search
    for markdown files (with extension .md) within the target dir.

    Args:
        target_dir (str): Path to directory to search for markdown tables in.
        output_dir (str): Path to existing directory to write tables to.
        delimiter (str): Value seperator to use when writing files.
    '''
    target_dir = Path(target_dir)
    output_dir = Path(output_dir)
    for each_path in target_dir.iterdir():
        if each_path.is_dir():
            write_tables(each_path, output_dir, delimiter)
        elif each_path.is_file() and each_path.suffix == ".md":
            tables = convert_tables(each_path)
            for i, each_table in enumerate(tables):
                write_table_to_file(
                    each_table, output_dir, each_path, i + 1, delimiter,
                    )
                


def write_table_to_file(table_as_list, output_dir, md_path, table_number, 
                        delimiter):
    '''Write a formated table (list of lists) to a text file.

    Args:
        table_as_list (list): Content of markdown table as a list of lists.
        output_dir (Path): Directory to write file to.
        md_path (Path): Path to markdown file the table originates from.
        table_number (int): Index of the table in the markdown file (order of 
                            appearance if multiple files.)
        delimiter (str): Value seperator character to use.
    '''
    if delimiter == "\t":
        extension = "tsv"
    elif delimiter == ",":
        extension = "csv"
    else:
        extension = "txt"

    table_name = f"{md_path.stem}_table_{table_number}.{extension}"
    table_path = output_dir.joinpath(table_name)

    with open(str(table_path), "w") as handle:
        for row in table_as_list:
            line = f"{delimiter}".join(row)
            handle.write(line)
            handle.write("\n")


def convert_tables(md_file):
    '''Converts all tables in a markdown file to list of lists.

    Args:
        md_file (Path): Path to markdown file to extract tables from.

    Returns:
        list: List of list of lists (lol). Each item in the list is one table
              (represented as a list of lists) extracted from the markdown
              file.

    '''
    clean_tables = []
    with open(str(md_file)) as handle:
        content = handle.read()
        tables = re.finditer(TABLE_REGEX, content)
        for each_match in tables:
            each_table = each_match[0].strip()
            clean_tables.append(clean_table(each_table))
    return clean_tables


def clean_table(table_string):
    '''Clean up the table string extracted by the TABLE_REGEX to a list
    of lists.

    Args:
        table_string (str): Table string extracted from markdown file 
                            by TABLE_REGEX

    Returns:
        list: List of lists with table contents.
    '''
    # split by \n to get rows
    table_rows = table_string.split("\n")
    table_row_cols = [row.split("|") for row in table_rows]
    table_row_cols_clean = [
        [cell.strip() for cell in row if cell] for row in table_row_cols
    ]
    # remove the second row which is just the markdown header indicator
    table_row_cols_clean = [table_row_cols_clean[0]] + table_row_cols_clean[2:]
    return table_row_cols_clean


def main():

    args = get_args()
    write_tables(args.dir, args.out, args.sep)


if __name__ == "__main__":
    main()
