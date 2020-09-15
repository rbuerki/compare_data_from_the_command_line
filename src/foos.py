import sys
from typing import List, Optional, Tuple

import pandas as pd


def load_files(
    path_1: str, path_2: str, index_col: Optional[str]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load data from files and return the dataframes."""
    dataframes = []
    for path in [path_1, path_2]:
        for separator in [",", ";", "\t", "|"]:
            try:
                df = pd.read_csv(
                    path, sep=f"{separator}", engine="python",
                )  # TODO: engine doesn't always fit the bill
            except FileNotFoundError:
                print(f"Sorry, file not found: '{path}'")
                sys.exit()
            if len(df.columns) > 1:
                break
        print(f"DF loaded, with original shape of {df.shape}")
        if index_col:
            df = _set_and_sort_index_col(df, index_col)
        else:
            df = df.sort_index()
        dataframes.append(df)
    return dataframes[0], dataframes[1]


def _set_and_sort_index_col(df: pd.DataFrame, index_col: str) -> pd.DataFrame:
    """
    If an index_col param is passed, check if that index_col has unique
    values only. If not, reject and exit. If yes, set to index and sort.
    This function is called within the load function.
    """
    if df[index_col].duplicated().sum() == 0:
        df = df.set_index(index_col, drop=True).sort_index()
        return df
    else:
        print(
            f"Error. Column {index_col} has duplicate values",
            "and cannot be used as dataframe index.",
        )
        sys.exit()


# TODO I could use this for logging? Or delete it ...
# def check_initial_structural_differences(
#     df_1: pd.DataFrame, df_2: pd.DataFrame
# ):
#     """Check if index, columns, datatypes are equal and
#     print info to console.
#     """
#     shape_check = df_1.shape == df_2.shape
#     col_check = df_1.columns == df_2.columns
#     idx_check = df_1.index == df_2.index
#     dtype_check = df_1.dtypes == df_2.dtypes

#     if not shape_check or not dtype_check:
#         print("\nInitial quickcheck for structural differences:")
#         print(f"Dataframe Shapes are identical: {shape_check}")
#         print(f"Column names are identical: {col_check}")
#         print(f"Indexes are identical: {idx_check}")
#         print(f"Data types are identical: {dtype_check}")
#         print("We will try to handle that ...\n")


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


# TODO - I don't need this probably and can remove it
def check_for_same_length(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the dataframes have the same index length, return
    a boolean value.
    """
    return df_1.shape[0] == df_2.shape[0]


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
    """TODO - I don't need this for dtypes, I think. I will remove the functionality.
    """
    if case == "columns":
        STR_VARS = ["width", "column names", "columns"]
    elif case == "dtypes":
        STR_VARS = ["column names", "dtypes", "columns"]

    INPUT_STRING = (
        f"The dataframes have the same {STR_VARS[0]}, but the "
        f"{STR_VARS[1]} differ. If you want to drop the "
        f"non-overlapping {STR_VARS[2]} for the comparison, "
        f"please press 'y'. If you think the data structure "
        f"is identical and want to enforce the {STR_VARS[1]} to "
        f"be identical for a full comparison, please press 'n'."
    )

    user_input = None
    while user_input != "y" or user_input != "n":
        user_input = input(INPUT_STRING)
        if user_input == "y":
            break
        elif user_input == "n":
            return user_input
            break
            print("Please press 'y' or 'n'.")
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
                f"Not possible to enforce dtype identity "
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
        print(f"Found difference in {dim} for the two dataframes.")
        dataframes = []
        for _tuple in SUBSETS:
            name, df, subset = _tuple[0], _tuple[1], _tuple[2]
            if len(subset) > 0:
                print(
                    f"{name} has {len(subset)} value(s) in {dim}",
                    "that could not be found in the other DF",
                    "and will be removed:",
                )
                for val in subset:
                    print(val)
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


def compare(df_1: pd.DataFrame, df_2: pd.DataFrame) -> None:
    """Compare if dataframe values are identical, if not, print a
    summary of the differences.

    Note: We do no longer check for identical dtypes in the
    individual columns, but only for identical values. This is because
    NaN values in a longer / wider dataframe can alter dtypes even
    after having been eliminated during previous steps.
    """
    if (df_1 != df_2).sum().sum() == 0:
        print("Successfully compared. Matching subsets of DFs are identical.")
    else:
        df_diff = df_1 != df_2
        print(
            "Successfully compared. DFs are NOT indentical.",
            f"\nCount of differences per column:\n\n{df_diff.sum()}",
        )
