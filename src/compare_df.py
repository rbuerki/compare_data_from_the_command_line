"""
# Compare Pandas DataFrames From The Command Line

Author: [Raphael Bürki](https://github.com/rbuerki)\n
Source: [Github](https://www.linkedin.com/in/raphael-buerki/)
"""

from typing import Tuple
import pandas as pd


def load_files(path_1: str, path_2: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load data from files and return the dataframes."""
    dataframes = ()
    for path in [path_1, path_2]:
        for separator in [",", ";", "\t", "|"]:
            df = pd.read_csv(path, sep=f"{separator}", engine="python",)
            if len(df.columns) > 1:
                break
        print(f"DF loaded, with shape {df.shape}")
        df = df.sort_index()
        df.columns = sorted(list(df.columns))
        dataframes.append(df.sort_index())
        return dataframes


def impute_missing_values(
    df_1: pd.DataFrame, df_2: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Impute any missing values with a str, because they can mess up comparisons."""
    df_1.fillna("MISSING", inplace=True)
    df_2.fillna("MISSING", inplace=True)
    return df_1, df_2


def compare_if_dataframes_are_equal(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Compare if the two dataframes are equal."""
    return df_1.equals(df_2)


def check_for_same_shape(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the dataframes are of same shape, return a boolean value."""
    return df_1.shape == df_2.shape


def check_for_identical_columns(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the (ordered) columns are identical, return a boolean value."""
    return list(df_1.columns) == list(df_2.columns)


def check_for_identical_indexes(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the (ordered) indexes are identical, return a boolean value."""
    return set(df_1.index) == set(df_2.index)


def handle_different_length(df_1: pd.DataFrame, df_2: pd.DataFrame) -> bool:
    """Check if the index values of the shorter dataframe fully overlap
    with the values of the longer dataframe, return a boolean value.
    """
    if len(df_1) > len(df_2):
        df_1 = check_for_overlapping_index(df_1, df_2)
        return df_1, df_2
    elif len(df_2) > len(df_1):
        df_2 = check_for_overlapping_index(df_2, df_1)
        return df_1, df_2
    else:
        assert (
            check_for_identical_indexes(df_1, df_2) is False
        ), "Something strange happened ..."
        raise ValueError("Cannot compare dataframes. Index values not identical.")

    return df_1, df_2


def check_for_overlapping_index(
    df_long: pd.DataFrame, df_short: pd.DataFrame
) -> pd.DataFrame:
    """Called within overlap_index_check."""
    if len(set(df_short.index).difference(set(df_long.index))) != 0:
        raise ValueError("Cannot compare dataframes. Index values do not overlap.")
    else:
        df_long = df_long.reindex(df_short.index)
        print(
            f"INFO: DF 1 has {len(df_long) - len(df_short)} more rows than DF 2.",
            "Only the overlapping subset is compared.",
        )

    return df_long, df_short
