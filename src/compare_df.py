"""
# Compare Pandas DataFrames From The Command Line

Author: [Raphael Bürki](https://github.com/rbuerki)\n
Source: [Github](https://www.linkedin.com/in/raphael-buerki/)
"""

import pandas as pd
import sys

# Parse CL arguments
try:
    files = [sys.argv[1], sys.argv[2]]
    df1 = pd.read_csv(files[0]).sort_index()
    df2 = pd.read_csv(files[1]).sort_index()
except:
    pass


def check(df1, df2):

    df1.fillna("None", inplace=True)
    df2.fillna("None", inplace=True)

    if df1.shape == df2.shape:
        if list(df1.columns) != list(df2.columns):
            raise Exception(
                "Cannot compare dataframes. Shape ok, but column labels differ."
            )
        if list(df1.index) != list(df2.index):
            raise Exception(
                "Cannot compare dataframes. Shape ok, but column labels differ."
            )

    if df1.shape[1] != df2.shape[1]:
        if df1.shape[0] != df2.shape[0]:
            raise Exception(
                "Cannot compare dataframes. Shape differs on columns and rows."
            )
        raise Exception("Cannot compare dataframes. Shape differs on columns.")

    if df1.shape[0] != df2.shape[0]:
        idx1 = set(df1.index.values)
        idx2 = set(df2.index.values)

        if idx1 > idx2:
            if len(idx2.difference(idx1)) != 0:
                raise Exception(
                    "Cannot compare dataframes. Index values do not overlap."
                )
            print(
                f"Dataframe 2 misses {len(idx1) - len(idx2)} rows.\n",
                "Will compare to the matching subset of dataframe 1.\n",
            )
            # Filter df1 for index values common with df2
            df1 = df1.reindex(df2.index)
            assert len(df1) == len(df2), "Filtering for same length went wrong ..."

        if idx2 > idx1:
            if len(idx1.difference(idx2)) != 0:
                raise Exception(
                    "Cannot compare dataframes. Index values do not overlap."
                )
            print(
                f"Dataframe 1 misses {len(idx2) - len(idx1)} rows.\n",
                "Will compare to the matching subset of dataframe 2.\n",
            )
            # Filter df2 for index values common with df1
            df2 = df2.reindex(df1.index)
            assert len(df1) == len(df2), "Filtering for same length went wrong ..."

    return df1, df2


def compare(df1, df2):
    if df2.equals(df1):
        print("Successfully compared. DataFrames are equal.")
    else:
        df_diff = df1 != df2
        print(
            "Successfully compared. Dataframes are NOT equal.\n",
            f"Differences in:\n\n{df_diff.sum()}",
        )


# df1 = pd.read_csv("./loeb_segments_2020-05-19-11-00-25.csv")
# df2 = pd.read_csv("./loeb_segments_2020-05-12-06-41-07.csv")


def main():
    df1_checked, df2_checked = check(df1, df2)
    compare(df1_checked, df2_checked)


if __name__ == "__main__":
    main()
