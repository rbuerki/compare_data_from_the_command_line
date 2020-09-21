# Compare Data From The Command Line

(Side project, Summer 2020)

## Intro

This application loads tabular data from two CSV-files into pandas dataframes and compares them. If differences are found, it prints a summary with the count of differing values per column, and optionally, saves XLSX table with boolean values indicating the location of these differences.

### Why that?

_And what's so special about this? Why not just use Pandas built-in `df.equals(df)` functionality or perfrom a boolean check with `(df != df).any()` or `df.ne(df)`?_

Now, first, here we've got a **command line interface**, making it a very handy tool for a (super) quick check. But what makes it really special, is it's ability to handle **a couple of edge cases**. (And believe me, I have encountered all of them for real in my daily work.)

It starts with **different encodings, special formatting and so on**: When starting the process from the CLI, you can enter all those special parameters that will then be passed to pandas' `pd.load_csv()` function for each of the two dataframes separately.

If your dataframes are of **different shape**, the application will handle that. It checks for common values in the (sorted) index and columns list and compares those sections only. It will tell you which rows or / columns have been dropped before the comparison. (This is convenient if, for example, you want to compare data from different ETL pipepline runs where new data is added with each dump. You can make sure that the handling of the older datapoints is consistent.)

... and don't worry: You can define **any column with non-duplicate values to be used as index** and if it happens that your dataframes have the same number of columns but their names differ, the app will double check if you want to the column names to be matched or if you really want the non-overlapping values to be dropped.

Finally the app will even try to ensure that the **dtypes of the differente columns are identical** (so long as they are not of dtype "object", because that could result in loss of information for some datetime formats). If this is not possible you'll get a warning, but the comparison will go on nevertheless.

### Behaviour, Functionality

To be effective the index values and column names of the two dataframes have to be consistent respective to the contained values. If they are not the comparison will fail. (One consequence for example: If new datapoints are added to a table, they have to be assigned to new index values, the old index values must persist. Only these older index values will be compared with an earlier version of the table.)

The app runs two equality checks. The first is run at the start of the process for dataframes of identical shape with the Pandas' `pd.equals()` function. It is a "strict" comparison that also takes into account the datatypes of the values.

Only if this strict check fails, the edge-case handling process is run ending with a final second equality check. This time with a boolean comparison. That one is less strict and compares values independent of their datatypes. (But you'll get a warning anyway if the dtypes differ.)

## Installation and Usage

Sorry, no "pip install" functionality implemented yet. Simply copy the `compare_df` folder in this repo to your local machine and make it available where ever you need it.

You can start the process from the command line, and, in the simplest of use cases, you'll simply pass the path strings / names of the two CSV-files containing the data that you want to compare:

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

For the whole thing to work, you'll need `Python >= 3.6`, a version of `Pandas` that's not too old, and either `xlsx_writer` or `pyarrow` for saving the final output to xlsx.

## Aknowledgements / Resources

This project was essentially a little playground for experimenting with test driven development and for working with a CLI. The following resources got me started:

- [Article on Unit Testing With Pytest](https://realpython.com/pytest-python-testing/) also on RealPython
- [Article on Command Line Interfaces with Argparse](https://realpython.com/command-line-interfaces-python-argparse/) on RealPython
- [Stackoverflow topic on parsing to a dictionary](https://stackoverflow.com/questions/29986185/python-argparse-dict-arg) (could do even more sophisticated)


## TODO - Version 0.3

- [ ] Add a GUI
- [ ] Add XLSX support --> testcase "druckfiles" in dev folder
- [ ] Make pip-installable, add a setup.py

