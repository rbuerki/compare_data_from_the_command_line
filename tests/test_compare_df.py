from pandas.testing import assert_index_equal
import pytest

from src.compare_df import (
    load_files,
    impute_missing_values,
    check_if_dataframes_are_equal,
    check_for_same_length,
    check_for_same_width,
    check_for_identical_column_names,
    check_for_identical_index_values,
    handle_different_length,
    check_for_overlapping_index_values,
    handle_different_width,
    check_for_overlapping_column_names,
    main,
)


# TODO: Test properly, check monkeypatches
def test_load_files():
    df_1, df_2 = load_files("tests/df_1_file.csv", "tests/df_2_file.csv")
    assert df_1.shape == (2, 6)
    assert df_2.shape == (2, 6)
    assert list(df_1.columns)[:2] == ["date_1", "float_4"]
    assert list(df_1.iloc[:, 1].values) == [1000.0, 500.0]


def test_impute_missing_values(df_1_base, df_2_base):
    assert df_1_base.isnull().sum().sum() == 2
    df_1, df_2 = impute_missing_values(df_1_base, df_2_base)
    assert (df_1.values == "MISSING").sum() == 2


def test_check_if_dataframes_are_equal(df_1_base, df_2_base):
    assert check_if_dataframes_are_equal(df_1_base, df_2_base) is False
    assert check_if_dataframes_are_equal(df_1_base, df_1_base)


def test_check_for_same_length(df_1_base, df_2_base, df_1_extended):
    assert check_for_same_length(df_1_base, df_1_extended) is False
    assert check_for_same_length(df_1_base, df_2_base)


def test_check_for_same_width(df_1_base, df_1_extended):
    assert check_for_same_width(df_1_base, df_1_extended)
    df_1_extended = df_1_extended[list(df_1_extended.columns)[1:]]
    assert check_for_same_width(df_1_base, df_1_extended) is False


def test_check_for_identical_column_names(df_1_base, df_1_extended):
    assert check_for_identical_column_names(df_1_base, df_1_extended)
    df_1_extended.columns = ["a", "b", "c", "d", "e", "f"]
    assert check_for_identical_column_names(df_1_base, df_1_extended) is False


def test_check_for_identical_index_values(df_1_base, df_2_base, df_1_extended):
    assert check_for_identical_index_values(df_1_base, df_2_base)
    assert check_for_identical_index_values(df_1_base, df_1_extended) is False


def test_check_for_overlapping_index_values(df_1_base, df_1_extended):
    df_1_extended = check_for_overlapping_index_values(df_1_extended, df_1_base)
    assert_index_equal(df_1_extended.index, df_1_base.index)

    df_1_base.index = [1, 3]
    with pytest.raises(
        ValueError, match="Cannot compare dataframes. Index values do not overlap."
    ) as e:
        check_for_overlapping_index_values(df_1_extended, df_1_base)
        assert e.type is ValueError


def test_handle_different_length(df_1_base, df_2_base, df_1_extended):
    df_1, df_2 = handle_different_length(df_1_extended, df_1_base)
    assert len(df_1) == len(df_2)

    df_1, df_2 = handle_different_length(df_1_base, df_1_extended)
    assert len(df_1) == len(df_2)

    with pytest.raises(AssertionError, match="Something strange happened ...") as e:
        handle_different_length(df_1_base, df_2_base)
        assert e.type is AssertionError

    df_2_base.index = [0, 2]
    with pytest.raises(
        ValueError, match="Cannot compare dataframes. Index values are not identical."
    ) as e:
        handle_different_length(df_1_base, df_2_base)
        assert e.type is ValueError


def test_check_for_overlapping_column_names(df_1_base, df_1_extended):
    df_1_base = df_1_base[list(df_1_base.columns)[1:]]
    df_1_extended = check_for_overlapping_column_names(df_1_extended, df_1_base)
    assert df_1_extended.shape[1] == df_1_base.shape[1]

    df_1_base.columns = ["a", "b", "c", "d", "e"]
    with pytest.raises(
        ValueError, match="Cannot compare dataframes. Column names do not overlap."
    ) as e:
        check_for_overlapping_column_names(df_1_extended, df_1_base)
        assert e.type is ValueError


def test_handle_different_width(df_1_base, df_2_base, df_1_extended):
    df_1_extended = df_1_extended[list(df_1_extended.columns)[1:]]
    df_1, df_2 = handle_different_width(df_1_extended, df_1_base)
    assert df_1.shape[1] == df_2.shape[1]

    df_1, df_2 = handle_different_width(df_1_base, df_1_extended)
    assert df_1.shape[1] == df_2.shape[1]

    with pytest.raises(AssertionError, match="Something strange happened ...") as e:
        handle_different_width(df_1_base, df_2_base)
        assert e.type is AssertionError

    df_2_base.columns = ["a", "b", "c", "d", "e", "f"]
    with pytest.raises(
        ValueError, match="Cannot compare dataframes. Column names are not identical."
    ) as e:
        handle_different_width(df_1_base, df_2_base)
        assert e.type is ValueError


def test_main(capsys):
    main("tests/df_1_file.csv", "tests/df_1_file.csv")
    captured = capsys.readouterr()  # Capture output
    assert "Successfully compared, dataframes are identical" in captured.out

    main("tests/df_1_file.csv", "tests/df_2_file.csv")
    captured = capsys.readouterr()  # Capture output
    assert "Successfully compared. Dataframes are NOT indentical." in captured.out

    main("tests/df_1_file.csv", "tests/df_1_ex_file.csv")
    captured = capsys.readouterr()  # Capture output
    assert (
        "Successfully compared. Matching subsets of dataframes are identical."
        in captured.out
    )
