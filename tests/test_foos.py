import numpy as np
import pandas as pd
import pytest

from compare_df import foos  # noqa

# from compare_df.__main__ import main  # noqa TODO, main test fails


def test_load_csv():
    df_1, df_2 = foos.load_csv(
        "tests/df_1_file.csv", "tests/df_2_file.csv", None
    )
    assert df_1.shape == (2, 6)
    assert df_2.shape == (2, 6)
    assert list(df_1.columns)[:2] == ["date_1", "int_2"]
    assert list(df_1.iloc[:, -1].values) == ["hello", np.NaN]


def test_load_csv_with_params():
    df_1, df_2 = foos.load_csv(
        "tests/df_1_file.csv",
        "tests/df_2_file.csv",
        load_params_1={"sep": ","},
        load_params_2={"sep": ","},
        index_col="str_3",
    )
    assert df_1.shape == df_2.shape == (2, 5)
    assert df_1.index.name == df_1.index.name == "str_3"


def test_load_csv_with_one_col_only(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    df_1, df_2 = foos.load_csv(
        "tests/df_1_file.csv",
        "tests/df_2_file.csv",
        load_params_1={"sep": ";"},
        load_params_2={"sep": ";"},
    )
    assert df_1.shape == df_2.shape == (2, 1)


def test_load_files_with_valid_index_col():
    df_1, df_2 = foos.load_csv(
        "tests/df_1_file.csv", "tests/df_2_file.csv", index_col="str_3"
    )
    assert df_1.shape == (2, 5)
    assert df_2.shape == (2, 5)
    assert list(df_1.columns)[:2] == ["date_1", "int_2"]
    assert list(df_1.index.values) == ["row1", "row2"]


def test_load_files_with_invalid_index_col(capsys):
    with pytest.raises(SystemExit) as exc_info:
        df_1, df_2 = foos.load_csv(
            "tests/df_1_file.csv", "tests/df_2_file.csv", index_col="date_1"
        )
        captured = capsys.readouterr()
        assert "Error. Column date_1" in captured.err
        assert exc_info.type is SystemExit


def test_impute_missing_values(df_1_base, df_2_base):
    assert df_1_base.isnull().sum().sum() == 2
    df_1, df_2 = foos.impute_missing_values(df_1_base, df_2_base)
    assert (df_1.values == "MISSING").sum() == 2


def test_check_if_dataframes_are_equal(df_1_base, df_2_base):
    assert foos.check_if_dataframes_are_equal(df_1_base, df_2_base) is False
    assert foos.check_if_dataframes_are_equal(df_1_base, df_1_base)


def test_check_for_same_width(df_1_base, df_1_extended):
    assert foos.check_for_same_width(df_1_base, df_1_extended)
    df_1_extended = df_1_extended[list(df_1_extended.columns)[1:]]
    assert foos.check_for_same_width(df_1_base, df_1_extended) is False


def test_check_for_identical_column_names(df_1_base, df_1_extended):
    assert foos.check_for_identical_column_names(df_1_base, df_1_extended)
    df_1_extended.columns = ["a", "b", "c", "d", "e", "f"]
    assert (
        foos.check_for_identical_column_names(df_1_base, df_1_extended) is False
    )


def test_check_for_identical_index_values(df_1_base, df_2_base, df_1_extended):
    assert foos.check_for_identical_index_values(df_1_base, df_2_base)
    assert (
        foos.check_for_identical_index_values(df_1_base, df_1_extended) is False
    )


def test_check_for_identical_dtypes(df_1_base, df_2_base):
    assert foos.check_for_identical_dtypes(df_1_base, df_1_base)
    assert foos.check_for_identical_dtypes(df_1_base, df_2_base) is False


def test_get_user_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    user_input = foos.get_user_input("columns")
    assert user_input == "y"


def test_enforce_column_identity(df_1_base, df_2_base):
    df_1 = df_1_base.loc[:, ::-1]
    df_1, df_2 = foos.enforce_column_identity(df_1, df_2_base)
    assert list(df_1.columns) == list(df_2.columns)
    assert list(df_1.columns)[0] == "string_6"


def test_align_dtypes(df_1_base, df_2_base):
    diff_list, _, _ = foos._align_dtypes(df_1_base, df_2_base)
    assert len(diff_list) == 1
    df_3 = df_1_base.copy()
    df_3["float_4"] = df_3["float_4"].astype(int)
    df_3["date_1"] = df_3["date_1"].astype(object)
    diff_list, _, _ = foos._align_dtypes(df_1_base, df_3)
    assert len(diff_list) == 0


def test_enforce_dtype_identity(df_1_base, df_2_base, capsys):
    df_1, df_2 = foos.enforce_dtype_identity(df_1_base, df_2_base)
    assert list(df_1.dtypes.values) == list(df_2.dtypes.values)
    captured = capsys.readouterr()
    assert captured.out == ""
    df_3 = df_1_base.copy()
    df_3.iloc[0, 3] = "str"
    df_1, df_3 = foos.enforce_dtype_identity(df_1_base, df_3)
    assert list(df_1.dtypes.values) != list(df_3.dtypes.values)
    captured = capsys.readouterr()
    assert "float_4" in captured.out


def test_get_subsets(df_1_base, df_1_extended):
    only_1, only_2 = foos._get_subsets("index", df_1_base, df_1_extended)
    assert (only_1 == set()) and (only_2 == set([2]))
    df_3 = df_1_extended.copy()
    colnames = list(df_3.columns)
    colnames[0] = "xxx"
    df_3.columns = colnames
    only_1, only_2 = foos._get_subsets("columns", df_1_base, df_3)
    assert (only_1 == set(["date_1"])) and (only_2 == set(["xxx"]))


def test_handle_different_values(df_1_base, df_1_extended, capsys):
    df_1, df_2 = foos.handle_different_values("index", df_1_base, df_1_extended)
    assert list(df_1.index) == list(df_2.index)
    captured = capsys.readouterr()
    assert captured.out.endswith("\n  - 2\n")


def test_sort_columns(df_1_base, df_2_base):
    df_1 = df_1_base.loc[:, ::-1]
    df_1, df_2 = foos.sort_columns(df_1, df_2_base)
    assert df_1.columns[0] == df_2.columns[0] == "string_6"


def test_compare(df_1_base, df_2_base, capsys):
    # NaN values have to be eliminated for this test
    df_1, df_2 = foos.impute_missing_values(df_1_base, df_2_base)

    df_diff = foos.compare(df_1, df_1)
    captured = capsys.readouterr()  # Capture output
    assert "They are identical" in captured.out
    assert df_diff.sum().sum() == 0

    df_diff = foos.compare(df_1, df_2)
    captured = capsys.readouterr()  # Capture output
    assert "They are NOT indentical." in captured.out
    assert df_diff.sum().sum() > 0


# def test_main(capsys):
#     main("tests/df_1_file.csv", "tests/df_1_file.csv", None)
#     captured = capsys.readouterr()  # Capture output
#     assert "Successfully compared, DFs are identical" in captured.out

#     main("tests/df_1_file.csv", "tests/df_2_file.csv", None)
#     captured = capsys.readouterr()  # Capture output
#     assert "Successfully compared. DFs are NOT indentical." in captured.out

#     main("tests/df_1_file.csv", "tests/df_1_ex_file.csv", None)
#     captured = capsys.readouterr()  # Capture output
#     assert (
#         "Successfully compared. Matching subsets of DFs are identical."
#         in captured.out
#     )

#     main("tests/df_1_file.csv", "tests/df_1_empty_row_file.csv", None)
#     captured = capsys.readouterr()  # Capture output
#     assert "Successfully compared. DFs are NOT indentical." in captured.out

#     with pytest.raises(
#         ValueError, match="Cannot compare DFs. Column names are not identical."
#     ) as e:
#         main("tests/df_1_file.csv", "tests/df_1_alt_col_file.csv", None)
#         assert e.type is ValueError
