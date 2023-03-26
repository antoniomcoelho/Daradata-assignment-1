"""Tests for the cleaning module"""
import pandas as pd
import unittest.mock as mock

from life_expectancy.cleaning import clean_data
from life_expectancy.load_save import load_data, save_data
from . import INIT_DIR, FIXTURES_DIR, OUTPUT_DIR


def test_load_data(load_data_expected):
    """Run the `load_data` function and compare the output to the expected output"""

    load_data_actual = load_data()
    #load_data_expected = pd.read_csv( FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep="\t")

    pd.testing.assert_frame_equal(
        load_data_actual, load_data_expected
    )


def test_save_data(pt_life_expectancy_expected):
    """Run the `save_data` function and compare the output to the expected output"""
    save_data_expected = pt_life_expectancy_expected
    with mock.patch.object(save_data_expected, "to_csv") as to_csv_mock:
        save_data(save_data_expected)
        to_csv_mock.assert_called_with(OUTPUT_DIR / "pt_life_expectancy.csv", index=False)


