from pandas.testing import assert_index_equal
import pytest

from src.compare_df import (
    impute_missing_values,
    compare_if_dataframes_are_equal,
    check_for_same_shape,
    check_for_identical_columns,
    check_for_identical_indexes,
    handle_different_length,
    check_for_overlapping_index,
)


# TODO: Test properly, check monkeypatches
def test_load_files(df_1_base, df_2_base):
    assert df_1_base.shape == (2, 6)
    assert df_2_base.shape == (2, 6)
    # assert list(df_1_base.columns)[:2] == ["date_1", "float_4"]


def test_impute_missing_values(df_1_base, df_2_base):
    assert df_1_base.isnull().sum().sum() == 2
    df_1, df_2 = impute_missing_values(df_1_base, df_2_base)
    assert (df_1.values == "MISSING").sum() == 2


def test_compare_if_dataframes_are_equal(df_1_base, df_2_base):
    assert compare_if_dataframes_are_equal(df_1_base, df_2_base) is False
    assert compare_if_dataframes_are_equal(df_1_base, df_1_base)


def test_check_for_same_shape(df_1_base, df_2_base, df_1_extended):
    assert check_for_same_shape(df_1_base, df_1_extended) is False
    assert check_for_same_shape(df_1_base, df_2_base)


def test_check_for_identical_columns(df_1_base, df_1_extended):
    assert check_for_identical_columns(df_1_base, df_1_extended)
    df_1_extended.columns = ["a", "b", "c", "d", "e", "f"]
    assert check_for_identical_columns(df_1_base, df_1_extended) is False


def test_check_for_identical_indexes(df_1_base, df_2_base, df_1_extended):
    assert check_for_identical_indexes(df_1_base, df_2_base)
    assert check_for_identical_indexes(df_1_base, df_1_extended) is False


def test_check_for_overlapping_index(df_1_base, df_1_extended):
    df_1_e, df_1_b = check_for_overlapping_index(df_1_extended, df_1_base)
    assert_index_equal(df_1_e.index, df_1_b.index)

    df_1_base.index = [1, 3]
    with pytest.raises(
        ValueError, match="Cannot compare dataframes. Index values do not overlap."
    ) as e:
        check_for_overlapping_index(df_1_extended, df_1_base)
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
        ValueError, match="Cannot compare dataframes. Index values not identical."
    ) as e:
        handle_different_length(df_1_base, df_2_base)
        assert e.type is ValueError
