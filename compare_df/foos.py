import datetime as dt
import os
import sys
from typing import Dict, List, Optional, Tuple

import pandas as pd


def load_csv(
    path_1: str,
    path_2: str,
    load_params_1: Optional[Dict[str, str]] = None,
    load_params_2: Optional[Dict[str, str]] = None,
    index_col: Optional[str] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load data from files and return the dataframes. Optional load params
    for each dataframe can be specified (according to `pd.read_csv()`) and
    also an column name to be used as index.
    """
    dataframes = []
    for path, params in {path_1: load_params_1, path_2: load_params_2}.items():
        try:
            os.path.exists(path)
        except FileNotFoundError:
            sys.exit(f"Sorry, path {path} does not exist. Try again, please.")

        if params:
            df = pd.read_csv(path, **params)
        else:
            for separator in [",", ";", "\t", "|"]:
                df = pd.read_csv(path, sep=f"{separator}")
                if len(df.columns) > 1:
                    break
        print(f"- DF loaded, with original shape of {df.shape}")

        if df.shape[1] == 1:
            user_input = get_user_input("width_of_one")
            if user_input == "y":
                pass
            elif user_input == "n":
                sys.exit("Try again, please.")

        if index_col:
            try:
                df = _set_and_sort_index_col(df, index_col, path)
            except KeyError:
                print(f"Sorry, column {index_col} not found in file {path}.")
        else:
            df = df.sort_index()
        dataframes.append(df)

    return dataframes[0], dataframes[1]


def _set_and_sort_index_col(
    df: pd.DataFrame, index_col: str, path: str
) -> pd.DataFrame:
    """
    If an index_col param is passed, check if that index_col exists in
    the dataframe and if it has unique values only. If not, reject
    and exit. If yes, set to index and sort. This function is called
    within `load_files`.
    """
    if index_col not in df.columns:
        sys.exit(f"Sorry, column {index_col} not found in file {path}.")

    elif df[index_col].duplicated().sum() > 0:
        sys.exit(
            (
                f"Error. Column {index_col} has duplicate values",
                "and cannot be used as dataframe index.",
            )
        )
    else:
        df = df.set_index(index_col, drop=True).sort_index()
        return df


def impute_missing_values(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Impute any missing values with a str, because they can
    mess up boolean comparisons.
    """
    df_1.fillna("MISSING", inplace=True)
    df_2.fillna("MISSING", inplace=True)
    return df_1, df_2


def check_if_dataframes_are_equal(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> bool:
    """Compare if the two dataframes are equal,
    return a boolean value.
    """
    return df_1.equals(df_2)


def check_for_same_width(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the dataframes have the same number of cols, return
    a boolean value.
    """
    return df_1.shape[1] == df_2.shape[1]


def check_for_identical_index_values(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> bool:
    """Check if the (ordered) indexes are identical, return
    a boolean value.
    """
    return set(df_1.index) == set(df_2.index)


def check_for_identical_column_names(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> bool:
    """Check if the (ordered) columns are identical, return
    a boolean value.
    """
    return list(df_1.columns) == list(df_2.columns)


def check_for_identical_dtypes(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the dtypes for the columns are identical, return
    a boolean value. (Can only be True for identical columns.)
    """
    return list(df_1.dtypes.values) == list(df_2.dtypes.values)


def get_user_input(case: str) -> str:
    """Get user input on what to do if the the dataframes are of same
    width, but the column names differ.
    """
    if case == "columns":
        INPUT_STRING = (
            "\nThe dataframes have the same number of columns, but their "
            "names differ. If you want to drop the non-overlapping "
            "columns for the comparison, please press 'y'. "
            "If you think the data structure of the dataframes"
            "is identical and want to enforce the column names to "
            "be identical for a 'full' comparison, please press 'n'."
        )
    elif case == "output":
        INPUT_STRING = (
            "\nDo you wish to save an XLSX file indicating all the "
            "differing values in tabular format? It will be saved "
            "into the same folder as from where DF_1 has been loaded."
        )
    elif case == "width_of_one":
        INPUT_STRING = (
            "\nThe loaded dataframe has only one column. Maybe you have "
            "to specify different load parameters. If you nevertheless "
            " want to proceed, please press 'y'. Press 'n' to abort."
        )

    user_input = None
    while user_input != "y" or user_input != "n":
        user_input = input(INPUT_STRING)
        if user_input == "y":
            break
        elif user_input == "n":
            break
    return user_input


def enforce_column_identity(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """In case of the user wanting to align the column names when they
    differ for dataframes of the same width, the column names of df_1
    will be given to df_2.
    """
    df_2.columns = df_1.columns
    return df_1, df_2


def enforce_dtype_identity(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """First try to enforce the dtypes other than 'object' of df_1 on
    df_2, if this is not possible for all columns, try the other way
    round. If that too is not possible for all columns, print a warning.
    Return both dataframes with aligned dtypes where possible.
    """
    diff_list, df_a, df_b = _align_dtypes(df_1, df_2)
    if len(diff_list) == 0:
        return df_a, df_b
    else:
        diff_list, df_b, df_a = _align_dtypes(df_2, df_1)
        if len(diff_list) == 0:
            return df_a, df_b
        else:
            problematic_columns = [
                col
                for col in df_1.columns
                if list(df_1.columns).index(col) in diff_list
            ]
            message = (
                f"\nNot possible to enforce dtype identity "
                f"on following column(s): {problematic_columns}. "
                f"Process continues with differing dtypes. "
            )
            print(message)
            return df_a, df_b


def _align_dtypes(
    df_a: pd.DataFrame, df_b: pd.DataFrame
) -> Tuple[List[int], pd.DataFrame, pd.DataFrame]:
    """Try to enforce the dtypes of non-object type of one dataframe
    on the other. Return a list of index values for those columns
    where it is not possible and the two dataframes (one of them
    transformed). This function is called within the function
    `enforce_dtype_identity`.
    """
    dtypes = [str(x) for x in df_a.dtypes]
    for col, dtype in zip(df_b.columns, dtypes):
        try:
            if dtype.startswith("date"):
                df_b[col] = pd.to_datetime(
                    df_b[col], infer_datetime_format=True
                )
            elif dtype == "object":
                pass
            else:
                df_b[col] = df_b[col].astype(dtype)
        except (TypeError, ValueError):
            pass
    mask = list(df_b.dtypes.values == df_a.dtypes.values)
    diff_list = [mask.index(x) for x in mask if x == 0]
    return diff_list, df_a, df_b


def handle_different_values(
    dim: str, df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame]:
    """Check if the dataframes have differing values in the `columns`
    or the `index`, depending on the passed dimension. If so, output a
    warning and list the respective values. Return the dataframes with
    all non-matching values removed on the respecting dimension.
    """
    only_in_1, only_in_2 = _get_subsets(dim, df_1, df_2)
    SUBSETS = [("DF 1", df_1, only_in_1), ("DF 2", df_2, only_in_2)]

    if len(only_in_1) == 0 and len(only_in_2) == 0:
        return df_1, df_2
    else:
        print(f"\nFound differences in the {dim} of the two dataframes.")
        dataframes = []
        for _tuple in SUBSETS:
            name, df, subset = _tuple[0], _tuple[1], _tuple[2]
            if len(subset) > 0:
                print(
                    f"- {name} has {len(subset)} value(s) in {dim}",
                    "that could not be found in the other DF",
                    "and will be removed:",
                )
                for val in subset:
                    print(f"  - {val}")
            if dim == "index":
                df = df.loc[~df.index.isin(subset)]
            elif dim == "columns":
                cols = [col for col in df.columns if col not in subset]
                df = df[cols]
            dataframes.append(df)
        return dataframes[0], dataframes[1]


def _get_subsets(
    dim: str, df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[set, set, set]:
    """Return two separate subsets of `columns` or `index` of the
    dataframes, depending on the passed dimension. The first subsets
    is consisting of values exclusive to the first dataframe, the
    second of values exclusive to the second dataframe.  (If there
    are no such values, the substets are returned empty.) This function
    is called within `handle_different_values`.
    """
    DIM_DICT = {
        "columns": [df_1.columns, df_2.columns],
        "index": [df_1.index, df_2.index],
    }
    only_in_1 = set(DIM_DICT[dim][0]).difference(set(DIM_DICT[dim][1]))
    only_in_2 = set(DIM_DICT[dim][1]).difference(set(DIM_DICT[dim][0]))
    return only_in_1, only_in_2


def sort_columns(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Make sure that the column order of the two dataframes
    is identical for the comparison: Sort columns of df_2 according
    to column order of df_2.
    """
    df_2 = df_2.reindex(df_1.columns, axis=1)
    return df_1, df_2


def compare(df_1: pd.DataFrame, df_2: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Compare if dataframe values are identical, if not, print a
    summary of the differences.

    Note: We do no longer check for identical dtypes in the
    individual columns, but only for identical values. This is because
    NaN values in a longer / wider dataframe can alter dtypes even
    after having been eliminated during previous steps.
    """
    df_diff = df_1.ne(df_2)
    if df_diff.sum().sum() == 0:  # TODO
        print(
            f"\nDataframes successfully compared with shape {df_1.shape}.",
            " They are identical.",
        )
        return None
    else:
        print(
            f"\nDataframes successfully compared with shape {df_1.shape}.",
            "They are NOT indentical.",
            f"\n# of differences per column:\n\n{df_diff.sum()}",
        )
        return df_diff


def save_differences_to_xlsx(path_1: str, df_diff: pd.DataFrame) -> None:
    """Save a boolean dataframe indicating all differences as "True". The
    file is saved to XLSX format with a timestamped file name to the same
    folder as to where DF_1 was loaded from.
    """
    out_path = os.path.split(path_1)[0]
    out_name = f"compare_df_diff_output_{dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M-%S')}.xlsx"
    full_out_path = os.path.join(out_path, out_name)
    writer = pd.ExcelWriter(full_out_path)
    df_diff.to_excel(writer)
    writer.save()
    print(f"\nOutput saved to: \n{os.path.abspath(full_out_path)}")
