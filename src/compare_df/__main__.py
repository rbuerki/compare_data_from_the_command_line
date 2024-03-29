"""Compare Data From The Command Line
This is the library version, meant to be imported.

Usage:
------
Import the package and execute main():
    >>> import compare_df
    >>> df_diff, df_1, df_2 = compare_df.main('path_1',
                                              'path_2',
                                              ['load_params_1'],
                                              ['load_params_2'],
                                              )

See https://github.com/rbuerki/compare_data_from_the_command_line/ for more information

Contact:
--------
Author: Raphael Bürki
https://www.linkedin.com/in/raphael-buerki/
More information is available at:
https://github.com/rbuerki/compare_data_from_the_command_line/

Version:
--------
- raph-compare-df: v0.3.0
"""

from typing import Dict, Optional, Tuple, Union
from pathlib import Path

import pandas as pd

from compare_df import foos


def main(
    df_1: Union[str, Path, pd.DataFrame],
    df_2: Union[str, Path, pd.DataFrame],
    load_params_1: Optional[Dict[str, str]] = None,
    load_params_2: Optional[Dict[str, str]] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run the full comparison process for two CSV files. Report
    progress and results, return 3 dataframes for further investigation.
    Additionally offer the option to save `df_diff` to excel.

    Args:
        path_1: Either a Pandas DataFrame or a path to the first file
            (has to be either .XLSX or .CSV format). This dataframe is 
            referred to as "DF_1")
        path_2: Either a Pandas DataFrame or a path to the second file
            (has to be in the same format as for DF_1). This dataframe
            is referred to as "DF_1")
        load_params_1: Dict of key-value pairs in string format, to be
            passed to `pd.read_csv` for DF_1. Defaults to None.
        load_params_2: Dict of key-value pairs in string format, to be
            passed to `pd.read_csv` for DF_2. Defaults to None.

    Returns:
        df_diff: Boolean dataframe indicating the exact positions of
            the differing values ("True"). If the DFs are totally equal
            an empty dataframe ist returned.
        df_1: The final state of DF_1 after processing
        df_2: The final state of DF_2 after processing
    """
    input_type = foos.check_input_type(df_1, df_2)
    if input_type == "filepath":
        file_format = foos.indentify_file_format(df_1, df_2)
        df_1, df_2 = foos.load_files(
            df_1, df_2, file_format, load_params_1, load_params_2
        )
    df_1, df_2 = foos.impute_missing_values(df_1, df_2)
    df_diff = pd.DataFrame()

    if foos.check_if_dataframes_are_equal(df_1, df_2):
        print("Successfully compared, DFs are identical.")
    else:
        if foos.check_for_same_width(df_1, df_2):
            if not foos.check_for_identical_column_names(df_1, df_2):
                user_input = foos.get_user_input("columns")
                if user_input == "y":
                    df_1, df_2 = foos.handle_different_values(
                        "columns", df_1, df_2
                    )
                else:
                    df_1, df_2 = foos.enforce_column_identity(df_1, df_2)
        else:
            df_1, df_2 = foos.handle_different_values("columns", df_1, df_2)

        df_1, df_2 = foos.sort_columns(df_1, df_2)

        if not foos.check_for_identical_index_values(df_1, df_2):
            df_1, df_2 = foos.handle_different_values("index", df_1, df_2)

        if not foos.check_for_identical_dtypes(df_1, df_2):
            df_1, df_2 = foos.enforce_dtype_identity(df_1, df_2)

        df_diff = foos.compare(df_1, df_2)

        if df_diff.sum().sum() > 0:
            user_input = foos.get_user_input("output")
            if user_input == "y":
                foos.save_differences_to_xlsx(df_diff)

    return df_diff, df_1, df_2


if __name__ == "__main__":
    main()
