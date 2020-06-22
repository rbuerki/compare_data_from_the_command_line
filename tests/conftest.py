import os
import sys

import numpy as np
import pandas as pd
import pytest

# Append abs path of the module to the sys.path(), solving some import problems
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def df_1_base():
    """This is the first base dataframes for testing."""
    data = {
        "date_1": ["12.08.1978", "12.08.1978"],
        "int_2": [1, 1],
        "str_3": ["row1", "row2"],
        "float_4": [1000.0, 500.0],
        "float_5": [np.nan, 0.03],
        "string_6": ["hello", np.nan],
    }
    return pd.DataFrame(data)


@pytest.fixture
def df_2_base():
    """This is the 2nd base df, 3 values changed: (0,2), (0,6), and (1,5)."""
    data = {
        "date_1": ["12.08.1978", "12.08.1978"],
        "int_2": [1, np.nan],
        "str_3": ["row1", "row2"],
        "float_4": [1000.0, 500.0],
        "float_5": [np.nan, 0.034],
        "string_6": ["hell-o", np.nan],
    }
    return pd.DataFrame(data)


@pytest.fixture
def df_1_extended():
    """This dataframe is like the first base dataframe but with one additional row."""
    data = {
        "date_1": ["12.08.1978", "12.08.1978", "18.08.2016"],
        "int_2": [1, 1, np.nan],
        "str_3": ["row1", "row2", "row3"],
        "float_4": [1000.0, 500.0, 500.0],
        "float_5": [np.nan, 0.03, 0.5],
        "string_6": ["hello", np.nan, np.nan],
    }
    return pd.DataFrame(data)


# df_1 = df_1_base()
# df_1.to_csv("df_1_file.csv", index=False)
# df_1_ex = df_1_extended()
# df_1_ex.to_csv("df_1_ex_file.csv", index=False)
# df_2 = df_2_base()
# df_2.to_csv("df_2_file.csv", index=False)
