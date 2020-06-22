"""
# Compare Pandas DataFrames From The Command Line

Author: [Raphael Bürki](https://github.com/rbuerki)\n
Source: [Github](https://www.linkedin.com/in/raphael-buerki/)
"""

from typing import Tuple
import pandas as pd


def load_files(path_1: str, path_2: str) -> Tuple[pd.DataFrame]:
    """Load data from files and return the dataframes."""
    dataframes = []
    for path in [path_1, path_2]:
        for separator in [",", ";", "\t", "|"]:
            df = pd.read_csv(path, sep=f"{separator}", engine="python",)
            if len(df.columns) > 1:
                break
        print(f"DF loaded, with shape {df.shape}")
        df = df.sort_index()
        df = df[sorted(list(df.columns))]
        dataframes.append(df.sort_index())
    return dataframes[0], dataframes[1]


def impute_missing_values(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Impute any missing values with a str, because they can mess up comparisons."""
    df_1.fillna("MISSING", inplace=True)
    df_2.fillna("MISSING", inplace=True)
    return df_1, df_2


def check_if_dataframes_are_equal(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Compare if the two dataframes are equal, return a boolean value."""
    return df_1.equals(df_2)


def check_for_same_length(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the dataframes have the same index length, return a boolean value."""
    return df_1.shape[0] == df_2.shape[0]


def check_for_same_width(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the dataframes have the same number of cols, return a boolean value."""
    return df_1.shape[1] == df_2.shape[1]


def check_for_identical_index_values(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the (ordered) indexes are identical, return a boolean value."""
    return set(df_1.index) == set(df_2.index)


def check_for_identical_column_names(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the (ordered) columns are identical, return a boolean value."""
    return list(df_1.columns) == list(df_2.columns)


def handle_different_length(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """When dataframes do not have the same length but the index values are overlapping,
    return the overlapping part of the longer dataframe only to make a comparison
    possible. If index values do not overlapp raise a value error.
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
        raise ValueError("Cannot compare dataframes. Index values are not identical.")

    return df_1, df_2


def check_for_overlapping_index_values(
    df_long: pd.DataFrame, df_short: pd.DataFrame
) -> pd.DataFrame:
    """Check if the index values of the longer dataframe fully overlap
    with the values of the shorter dataframe, then reindex the longer dataframe,
    so that it is shortened to match the index values of the shorter dataframe.
    This function is called within `handle_different_length` function.
    """
    len_df_long_orig = len(df_long)
    if len(set(df_short.index).difference(set(df_long.index))) != 0:
        raise ValueError("Cannot compare dataframes. Index values do not overlap.")
    else:
        df_long = df_long.reindex(df_short.index)
        print(
            f"INFO: DF 1 has {len_df_long_orig - len(df_short)} rows more than DF 2.",
            "Only the overlapping subset is compared.",
        )

    return df_long


def handle_different_width(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """When dataframes do not have the same witdh but the column names are overlapping,
    return the overlapping part of the wider dataframe only to make a comparison
    possible. If column names do not overlapp raise a value error.
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
        raise ValueError("Cannot compare dataframes. Column names are not identical.")

    return df_1, df_2


def check_for_overlapping_column_names(
    df_wide: pd.DataFrame, df_slim: pd.DataFrame
) -> pd.DataFrame:
    """Check if the column names of the longer dataframe fully overlap
    with the values of the shorter dataframe, then reindex the wider dataframe,
    so that it is slimmed down to match the column names of the slimmer dataframe.
    This function is called within the `handle_different_width` function.
    """
    width_df_wide_orig = df_wide.shape[1]
    if len(set(df_slim.columns).difference(set(df_wide.columns))) != 0:
        raise ValueError("Cannot compare dataframes. Column names do not overlap.")
    else:
        df_wide = df_wide[df_slim.columns]
        print(
            f"INFO: DF 1 has {width_df_wide_orig - len(df_slim)} columns more than DF 2.",
            "Only the overlapping subset is compared.",
        )

    return df_wide


def compare(df_1: pd.DataFrame, df_2: pd.DataFrame) -> None:
    # TODO: Write a proper docstring
    """Note we do not check for identical dtypes in the individual columns,
    but only for identical values (because NaN values could alter that, even
    after they have been eliminated in the previous steps).
    """
    if (df_1 != df_2).sum().sum() == 0:
        print("Successfully compared. Matching subsets of dataframes are identical.")
    else:
        df_diff = df_1 != df_2
        print(
            "Successfully compared. Dataframes are NOT indentical.\n",
            f"Differences in:\n\n{df_diff.sum()}",
        )


def main(path_1: str, path_2: str):
    df_1, df_2 = load_files(path_1, path_2)
    df_1, df_2 = impute_missing_values(df_1, df_2)

    if check_if_dataframes_are_equal(df_1, df_2):
        print("Successfully compared, dataframes are identical.")
    else:
        if check_for_same_length(df_1, df_2):
            if check_for_identical_index_values(df_1, df_2) is False:
                raise AssertionError("Message xy")  # TODO
            # else:
            #     pass
        else:
            df_1, df_2 = handle_different_length(df_1, df_2)

        if check_for_same_width(df_1, df_2):
            if check_for_identical_index_values(df_1, df_2) is False:
                raise AssertionError("Message yz")  # TODO
            # else:
            #     pass
        else:
            df_1, df_2 = handle_different_width(df_1, df_2)

        compare(df_1, df_2)


if __name__ == "__main__":
    # TODO: Implement ARGPARS
    main("tests/df_1_file.csv", "tests/df_1_ex_file.csv")
