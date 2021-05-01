# Compare Data From The Command Line

(Side project, Summer 2020, actual version: 0.2.0)

## Intro

This application loads tabular data from two CSV-files into Pandas DataFrames and compares them. If a full comparison with Pandas' built-in `df.equals(df)` is not possible the data is pre-processed step-by-step to enable a boolean matching that is as close as possible using Pandas' `df.ne(df)`.

The app tries to catch and handle many edge cases that I have encountered in my daily work. If necessary, the user is asked on how to proceed with the pre-processing.

## Features

Contrary to the project's title, the package can now be used either as:

1) an importable library, for example to be used within a jupyter notebook
2) a handy stand-alone CLI tool for super-quick data checks

It results in:

- Standard-out process report and summary with the count of differing values per column (both versions)
- Option to save a boolean dataframe to excel, indicating the exact locations of these differing values (both versions)
- (Library version only) Return of 3 dataframes: The boolean 'df_diff' and the final states of the two processed input files

Special features for processing are (same for both versions):

- Possiblity to define specific load parameters for each file that will be passed to Pandas' `read_csv` function
- Possiblity to define a specific column to be used as the index
- Possiblity to enforce the same column names if these differ but the width of the 2 dataframes is the same
- Handling of different shapes by finding matching subsets in the columns / indexes for the comparison
- As far as possible: Handling of different dtypes as long as they are not of `object` type

## Data prerequisites

- For the moment the app accepts CSV files only.
- Index values and column names of the two tables have to be consistent respective to the values they contain. Else a comparison is not possible. (For example this means: If new datapoints are added to a table, they have to be assigned to new index values while the existing index values are not allowed to change. Else they can not be compared with an earlier version of the table.)
- If you pass a specific column name to be used as index, make sure it exists in both dataframes (if not, use the load_params to rename columns). Also make sure the index columns have no duplicate values.

## Usage

### Command line Version

```shell
compare_df [options] [path_1] [path_2]
```

Available options are:

| Prefix                | Description                        |
| --------------------- | ---------------------------------- |
| -l_1, --load_params_1 | Load params for file at path_1     |
| -l_2, --load_params_2 | Load params for file at path_2     |
| -i, --index_col       | Name of column to be used as index |

Note: The optional load params have to be passed as single key-value-pairs in string format, each of them separatly for the respective dataframe. You can pass all the args that are accepted by [pandas.read_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

A full example could look as follows:

```shell
compare_df "data/file_manual.csv" "data/file_auto.csv" -l_1 "engine"="python" -l_1 "sep"=";" -l_2 "encoding"="UTF-8" -l_2 "sep"=";" -i "customer_ID"
```

### Library Version

```python
>>> import compare_df
>>> df_diff, df_1, df_2 = compare_df.main(
    'path_1',
    'path_2',
    ['load_params_1'],
    ['load_params_2'],
    ['index_col']
)
```

Note: Contrary to the CLI version the optional load params are passed as dicts with key-value-pairs in string format. Again, you can pass all the args that are accepted by [pandas.read_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

A full example of calling the main() function could look as follows:

```python
df_diff, df_1, df_2 = compare_df.main(
    "data/file_manual.csv",
    "data/file_auto.csv",
    load_params_1={"engine": "python", "sep": ";"},
    load_params_2={"encoding": "UTF-8", "sep": ";"},
    index_col="customer_ID"
)
```

## Installation

Quick & dirty:

- Clone or fork this repo to your machine
- Activate a virtual envirenment of your choice (make sure you have pip installed)
- Open a terminal, navigate to the repo's top-level folder (where `setup.py` is located)
- Run the following command:

```shell
pip install .
```

Dependencies: `Python >= 3.6`, `Pandas` and `xlsx_writer` (or alternatively `openpyxl`).

## Aknowledgements / Resources

This project was essentially a little playground for experimenting with test driven development, working with a CLI and making a locally installable package (in development mode). The following resources got me started:

- [Article on Unit Testing With Pytest](https://realpython.com/pytest-python-testing/) on RealPython
- [Article on Command Line Interfaces with Argparse](https://realpython.com/command-line-interfaces-python-argparse/) on RealPython
- [Topic on parsing to a dictionary](https://stackoverflow.com/questions/29986185/python-argparse-dict-arg) on Stackoverflow (could do a bit more sophisticated)
- [Article on how to install a local package in DEV mode](https://realpython.com/python-import/#create-and-install-a-local-package) on RealPython
- [Setuptools documentation](https://setuptools.readthedocs.io/en/latest/setuptools.html#id8) on how to configure the `setup.py` file in detail

# WIP

- Add the possibility to compare existing df in the library version
- Add XLSX support --> testcase "druckfiles" in dev folder

  - [ ] Implement load_xlsx foo
  - [ ] Refactor load_csv foo
  - [ ] Adapt __main__ with new workflow for loading
  - [ ] Adapt docs and version to 0.3

## TODO

Possible new features for future versions:

- [ ] Enable proper installation, add build / dist
- [ ] Add a simple GUI (using a separate [setuptools entry point](https://setuptools.readthedocs.io/en/latest/setuptools.html#id16))
- [ ] Make an executable with PyInstaller (see [here](https://realpython.com/pyinstaller-python/#distribution-problems))
