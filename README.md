# Compare Data From The Command Line

(Side project, Summer 2020)

## Intro

This application loads tabular data from two CSV-files into pandas dataframes and compares the data. If differences are found, it prints a summary with the count of differing values per column, and optionally saves a new dataframe with boolean values indicating the location of the differences.

### What for?

_And what's so special about this? Why not just use Pandas built-in `df.equals(df)` functionality or perfrom a boolean check with `(df != df).any()` or `df.ne(df)`?_

Now, first, here we've got a command line interface, making it a very handy tool for a (super) quick check. But what makes it really special, is it's ability to handle a couple of edge cases. (And believe me, I have encountered all of them in my daily work.)

It starts with **different encodings, special formatting and so on**: When starting the process from the CLI, you can enter all those special parameters that will then be passed to pandas' `pd.load_csv()` function for each of the two dataframes separately.

If your dataframes are of **different shape**, the application will handle that. It checks for common values in the (sorted) index and columns list and compares those sections only. It will tell you which rows or / columns have been dropped before the comparison. (This is convenient if, for example, you want to compare data from different ETL pipepline runs where new data is added with each dump. You can make sure that the handling of the older datapoints is consistent.)

... and don't worry: You can define **any column with non-duplicate values to be used as index** and if it happens that your dataframes have the same number of columns but their names differ, the app will double check if you want to the column names to be matched or if you really want the non-overlapping values to be dropped.

Finally the app will even try to ensure that the **dtypes of the differente columns are identical** (so long as they are not of dtype "object", because that could result in loss of information for some datetime formats). If this is not possible you'll get a warning, but the comparison will go on nevertheless.

### Behaviour, Functionality

To be effective the index values and column names of the two dataframes have to to consistent. If these are floating the comparison will fail. (One consequence: New datapoints have to be assigned to new index values.)

The app runs two equality checks. The first is run at the start of the process for dataframes of identical shape with the Pandas' `pd.equals()` function. It is a "strict" comparison that also takes into account the datatypes of the values.

Only if this fails, the edge-case handling get's activated and a final second check is run, this time with a boolean comparison. That one is less strict and compares values independent of their datatypes. (But you'll get a warning anyway if they differ.)

## Installation and Usage

Sorry, no "pip install" functionality implemented yet. Simply copy the `compare_df` folder in this repo to your local machine and make it available where ever you need it.

Then you can start the process from the command line, and, in the simplest of use cases, you'll simply pass the path strings / names of the two CSV-files containing the data that you want to compare:

```python
python compare_df {"source_file_1"} {"source_file_2"}
```

If you want to define a specific column to be used as index, you can do this with the prefix `-i` or `--index_col`.

If things get nasty and you have to pass some extra load params to get your dataframes properly loaded, you can pass the respective key-value-pairs as strings after the following prefixes (depending on the dataframe):

- `-l_1` / `--load_params_1` (first file)
- `-l_2` / `--load_params_2` (second file)

A full example could then look as follows:

```python
python compare_df "data/file_manual.csv" "data/file_auto.csv" -l_1 "engine"="python" -l_1 "sep"=";" -l_2 "encoding"="UTF-8" -l_2 "sep"=";" -i "customer_ID"
```

You'll need Python >= 3.6 and a version of Pandas that's not too old.

## Aknowledgements / Resources

This project was essentially a little playground for experimenting with test driven development and for working with a CLI. The following resources got me started:

- [Article on Unit Testing With Pytest](https://realpython.com/pytest-python-testing/) also on RealPython
- [Article on Command Line Interfaces with Argparse](https://realpython.com/command-line-interfaces-python-argparse/) on RealPython
- [Stackoverflow topic on parsing to a dictionary](https://stackoverflow.com/questions/29986185/python-argparse-dict-arg) (could do even more sophisticated)

## TODO - WIP

- [ ] Add function with output of difference 'coordinates' / save diff_df
- [ ] Add a WARNING when n cols = 1 - ask for next steps

## TODO - v0.3

- [ ] Add a GUI
- [ ] Add XLSX support --> testcase "druckfiles" in dev folder
- [ ] Prio 2: Add a setup.py
- [ ] Prio 2: Use the file names of the dataframes for output messages
- [ ] Maybe: Add logging to file (for exact debugging)

<!-- # TODO I could use this for logging? Or delete it ...
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
#         print("We will try to handle that ...\n") -->
