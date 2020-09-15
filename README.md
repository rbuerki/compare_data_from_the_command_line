# Compare Data From The Command Line

(A small side project, June 2020)

## Intro

This application loads tabular data from two CSV-files into pandas dataframes and compares the data for differences. If differences are found, it prints a summary with the count of differing values per column.

### What for?

_And what's so special about this? Why not just use Pandas built-in `df.equals(df)` functionality or perfrom a boolean check with `(df != df).any()`?_

Now, first, here we've got a command line interface, making it a very handy tool for a (super) quick check. But what makes it really special, is it's ability to handle dataframes of different size. (The aforementioned pandas functions don't do that.) So, if one dataframe is wider and / or longer than the other, the app checks for overlapping sections in the index and columns list and compares those sections only.

This is convenient if, for example, you want to compare data from different ETL pipepline runs where new data is added with each dump. Now you can make sure that the handling of the older datapoints ist consistent.

### Behaviour, Functionality

By design, this means that index values and column names have to be consistent. If these change the comparison will fail. (One consequence: New datapoints have to be assigned to new index values.)

There are two equality checks in this app. The first is run for dataframes of identical shape with the Pandas' `pd.equals()` function. This is a "strict" comparison that also takes into account the datatypes of the values.

If dataframes are not of the same size, as second check is run after some data handling, this time with a boolean comparison. That one is less strict and compares values indipendent of their datatypes. This is necessary because the handling can change datatypes (especially if you have NaN values in your dataframes). Be aware of that.

## Installation and Usage

Sorry, no "pip install" functionality implemented yet. Simply copy the `compare_df.py` file in the `src/` folder of this repo to your local machine and make it available whereever you need it.

Then you can use it from the command line, passing the path / names of the two CSV-files containing the data that you want to compare:

```python
python compare_df.py {source_file_1} {source_file_2}
```

You'll need Python >= 3.6 and a "contemporary" version of Pandas. ;-)

## Aknowledgements / Resources

This project was essentially a little playground for experimenting with test driven development and for working with a CLI. The following resources got me started:

- [Article on Command Line Interfaces with Argparse](https://realpython.com/command-line-interfaces-python-argparse/) on RealPython
- [Article on Unit Testing With Pytest](https://realpython.com/pytest-python-testing/) also on RealPython

## TODO - Up next (WIP)

- [ ] Validate results with birthday test (see test ipynb)
- [ ] Clean-up remaining TODO strings
- [ ] Update README
- [ ] Add XLSX support --> testcase "druckfiles" in dev folder
- [ ] Add logging to file (for exact debugging)
- [ ] Add function with output of difference 'coordinates'

## TODO - v0.3

- [ ] Prio 2: Add a setup.py
- [ ] Prio 2: Use the file names of the dataframes for output messages
- [ ] ...