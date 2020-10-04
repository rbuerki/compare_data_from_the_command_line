"""Compare Data From The Command Line
This is the script version.

Usage:
------
    $ compare_df [options] [path_1] [path_2]

Available options are:
    -l_1, --load_params_1   Load params for file 1
    -l_2, --load_params_2   Load params for file 2
    -i, --index_col         Name of column to be used as index

Contact:
--------
Author: Raphael Bürki
https://www.linkedin.com/in/raphael-buerki/
More information is available at:
https://github.com/rbuerki/compare_data_from_the_command_line/

Version:
--------
- raph-compare-df: v0.2.0
"""


import argparse

from compare_df import __main__

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
    "-l_1",
    "--load_params_1",
    action="append",
    type=lambda kv: kv.split("="),
    dest="load_params_1",
    help=(
        "A DF_1-specific key-value-pair to be passed as argument to "
        "`pd.read_csv()`, e.g.`'encoding'='UFT-8'`. You can pass multiple pairs. "
        "Defaults to None. "
    ),
    default=None,
)
arg_parser.add_argument(
    "-l_2",
    "--load_params_2",
    action="append",
    type=lambda kv: kv.split("="),
    dest="load_params_2",
    help=(
        "A DF_2-specific key-value-pair to be passed as argument to "
        "`pd.read_csv()`, e.g. 'encoding'='UFT-8'`. You can pass multiple pairs. "
        "Defaults to None."
    ),
    default=None,
)
arg_parser.add_argument(
    "-i",
    "--index_col",
    help=(
        "Name of a column to use as index, dropping the original index. "
        "Is the same for both dataframes. Defaults to None."
    ),
    default=None,
)


def cli() -> None:
    """Run the full comparison process for two CSV files. Report
    progress and results. Offer the option to save a boolean dataframe
    to excel that indicates the exact position of differing values.
    """
    args = arg_parser.parse_args()

    path_1 = args.path_1
    path_2 = args.path_2
    if args.load_params_1:
        load_params_1 = dict(args.load_params_1)
    else:
        load_params_1 = args.load_params_1
    if args.load_params_2:
        load_params_2 = dict(args.load_params_2)
    else:
        load_params_2 = args.load_params_2
    index_col = args.index_col

    __main__.main(path_1, path_2, load_params_1, load_params_2, index_col)


if __name__ == "__main__":
    cli()
