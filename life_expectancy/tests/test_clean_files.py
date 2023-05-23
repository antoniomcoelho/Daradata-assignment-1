"""Tests for the cleaning module"""
import pandas as pd
import unittest.mock as mock  # pylint: disable=consider-using-from-import

from pathlib import Path # pylint: disable=import-error

from life_expectancy.clean_files import CleanFile, Country, TSVstrategy, JSONstrategy
from . import FIXTURES_DIR, OUTPUT_DIR



DATA_DIR = Path(__file__).parent.parent / 'data'


def test_load_data_TSV(load_data_expected):
    """Run the `load_data` function and compare the output to the expected output of TSV files"""
    actual_data = TSVstrategy().load_data()
    pd.testing.assert_frame_equal(actual_data, load_data_expected)


def test_load_data_JSON(load_data_expected_JSON):
    """Run the `load_data` function and compare the output to the expected output of JSON files"""
    actual_data = JSONstrategy().load_data()
    pd.testing.assert_frame_equal(actual_data, load_data_expected_JSON)


def test_clean_data_tsv(pt_life_expectancy_expected, load_data_expected):
    """Run 'clean_data` function for TSV files"""
    pt_life_expectancy_actual = TSVstrategy().clean_data(load_data_expected, ['PT'])
    pd.testing.assert_frame_equal(pt_life_expectancy_actual[0].reset_index(drop=True), pt_life_expectancy_expected)


def test_countries_list():
    """ Function that test the countries in the list """
    actual_countries_list = Country.list_countries()
    expected_countries_list = ['PT', 'BE', 'DK']

    assert actual_countries_list == expected_countries_list


def test_save_data(pt_life_expectancy_expected):
    """Run the `save_data` function and compare the output to the expected output"""
    save_data_expected = pt_life_expectancy_expected
    with mock.patch.object(save_data_expected, "to_csv") as to_csv_mock:
        CleanFile(['PT'], 'TSV').save_data([save_data_expected], ['PT'])
        to_csv_mock.assert_called_with(OUTPUT_DIR / "pt_life_expectancy.csv", index=False)

