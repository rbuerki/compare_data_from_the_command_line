"""
# Compare Data From The Command Line

Author: [Raphael Bürki](https://www.linkedin.com/in/raphael-buerki/)\n
Source: [Github](https://github.com/rbuerki/compare_data_from_the_command_line/)
"""

import argparse
from typing import Optional

import foos


arg_parser = argparse.ArgumentParser(
    description="".join(
        [
            "Load the content of two csv-files into Pandas DataFrames ",
            "and compare them or their matching subsets.",
        ]
    )
)
arg_parser.add_argument("path_1", help="Path to the first file", type=str)
arg_parser.add_argument("path_2", help="Path to the second file", type=str)
arg_parser.add_argument(
    "-i",
    "--index_col",
    help=(
        "Name of column to use as index, dropping the original index.",
        "Defaults to None.",
    ),
    default=None,
)


def main(path_1: str, path_2: str, index_col: Optional[str]):
    df_1, df_2 = foos.load_files(path_1, path_2, index_col)
    df_1, df_2 = foos.impute_missing_values(df_1, df_2)

    if foos.check_if_dataframes_are_equal(df_1, df_2):
        print("Successfully compared, DFs are identical.")
    else:
        if foos.check_for_same_length(df_1, df_2):
            if foos.check_for_identical_index_values(df_1, df_2) is False:
                raise ValueError(
                    "Cannot compare DFs. Index values are not identical."
                )
        else:
            df_1, df_2 = foos.handle_different_length(df_1, df_2)

        if foos.check_for_same_width(df_1, df_2):
            if foos.check_for_identical_column_names(df_1, df_2) is False:
                raise ValueError(
                    "Cannot compare DFs. Column names are not identical."
                )
        else:
            df_1, df_2 = foos.handle_different_width(df_1, df_2)

        foos.compare(df_1, df_2)


if __name__ == "__main__":
    args = arg_parser.parse_args()

    path_1 = args.path_1
    path_2 = args.path_2
    index_col = args.index_col

    main(path_1, path_2, index_col)
