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

# TODO sort columns, only if you are sure that cols are ident
# df = df[sorted(list(df.columns))]


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
    """TODO - input_string probably wrong for dtyes, I wont remove
    non matching cols
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
                f"We continue with differing dtypes. "
            )
            print(message)
            return df_a, df_b


def _align_dtypes(
    df_a: pd.DataFrame, df_b: pd.DataFrame
) -> Tuple[List[int], pd.DataFrame, pd.DataFrame]:
    """Try to enforce the dtypes of non-object type of one dataframe
    on the other. Return a list of index values for those columns
    where it is not possible and the two dataframes (one of them
    transformed).
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
    """x"""
    common, only_1, only_2 = _get_subsets(dim, df_1, df_2)


def _get_subsets(
    dim: str, df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[set, set, set]:
    """Depending on passed dimension, return three separate subset of
    'columns' or 'index' of the dataframes, the first consisting of
    common values, the second of values exclusive to the first
    dataframe, the third of values exclusive to the second dataframe.
    This function is called within `handle_different_values`.
    """
    DIM_DICT = {
        "columns": [df_1.columns, df_2.columns],
        "index": [df_1.index, df_2.index],
    }
    common = set(DIM_DICT[dim][0]).intersection(set(DIM_DICT[dim][1]))
    only_1 = set(DIM_DICT[dim][0]).difference(set(DIM_DICT[dim][1]))
    only_2 = set(DIM_DICT[dim][1]).difference(set(DIM_DICT[dim][0]))
    return common, only_1, only_2


def handle_different_length(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """When dataframes do not have the same length but the index values
    are overlapping, return the overlapping part of the longer dataframe
    only to make a comparison possible. If index values do not overlap
    raise a value error.
    """
    if len(df_1) > len(df_2):
        df_1 = check_for_overlapping_index_values(df_1, df_2)
        return df_1, df_2
    elif len(df_2) > len(df_1):
        df_2 = check_for_overlapping_index_values(df_2, df_1)
        return df_1, df_2
    else:
        # Asserting one of these "I swear this cannot happen" issues ;-)
        assert (
            check_for_identical_index_values(df_1, df_2) is False
        ), "Something strange happened ..."
        raise ValueError("Cannot compare DFs. Index values are not identical.")

    return df_1, df_2


def check_for_overlapping_index_values(
    df_long: pd.DataFrame, df_short: pd.DataFrame
) -> pd.DataFrame:
    """Check if the index values of the longer dataframe fully overlap
    with the values of the shorter dataframe, then reindex the longer
    dataframe, so that it is shortened to match the index values of
    the shorter dataframe. This function is called within the
    `handle_different_length` function.
    """
    len_df_long_orig = len(df_long)
    if len(set(df_short.index).difference(set(df_long.index))) != 0:
        raise ValueError("Cannot compare DFs. Index values do not overlap.")
    else:
        df_long = df_long.reindex(df_short.index)
        print(
            f"INFO: DF 1 has {len_df_long_orig - len(df_short)}",
            "rows more than DF 2.",
            "Only the overlapping subset is compared.",
        )

    return df_long


def handle_different_width(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """When dataframes do not have the same witdh but the column names
    are overlapping, return the overlapping part of the wider dataframe
    only to make a comparison possible. If column names do not overlap
    raise a value error.
    """
    if df_1.shape[1] > df_2.shape[1]:
        df_1 = check_for_overlapping_column_names(df_1, df_2)
        return df_1, df_2
    elif df_2.shape[1] > df_1.shape[1]:
        df_2 = check_for_overlapping_column_names(df_2, df_1)
        return df_1, df_2
    else:
        # Asserting one of these "I swear this cannot happen" issues ;-)
        assert (
            check_for_identical_column_names(df_1, df_2) is False
        ), "Something strange happened ..."
        raise ValueError("Cannot compare DFs. Column names are not identical.")

    return df_1, df_2


def check_for_overlapping_column_names(
    df_wide: pd.DataFrame, df_slim: pd.DataFrame
) -> pd.DataFrame:
    """Check if the column names of the longer dataframe fully overlap
    with the values of the shorter dataframe, then reindex the wider
    dataframe, so that it is slimmed down to match the column names of
    the slimmer dataframe. This function is called within the
    `handle_different_width` function.
    """
    width_df_wide_orig = df_wide.shape[1]
    if len(set(df_slim.columns).difference(set(df_wide.columns))) != 0:
        raise ValueError("Cannot compare DFs. Column names do not overlap.")
    else:
        df_wide = df_wide[df_slim.columns]
        print(
            f"INFO: DF 1 has {width_df_wide_orig - len(df_slim)}",
            "columns more than DF 2.",
            "Only the overlapping subset is compared.",
        )
    return df_wide


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
            "Successfully compared. DFs are NOT indentical.\n",
            f"Count of differences per column:\n\n{df_diff.sum()}",
        )
