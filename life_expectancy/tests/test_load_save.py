"""Tests for the cleaning module"""
import unittest.mock as mock  # pylint: disable=consider-using-from-import
from unittest.mock import patch
from pathlib import Path

from life_expectancy.load_save import load_data, save_data
from . import OUTPUT_DIR

DATA_DIR = Path(__file__).parent.parent / 'data'

@patch("life_expectancy.load_save.pd.read_table")
def test_load_data(mock_load, load_data_expected):
    """Run the `load_data` function and compare the output to the expected output"""

    mock_load.return_value = load_data_expected
    load_data()

    name_file = DATA_DIR / "eu_life_expectancy_raw.tsv"
    mock_load.assert_called_once_with(name_file, sep='\t')


def test_save_data(pt_life_expectancy_expected):
    """Run the `save_data` function and compare the output to the expected output"""
    save_data_expected = pt_life_expectancy_expected
    with mock.patch.object(save_data_expected, "to_csv") as to_csv_mock:
        save_data(save_data_expected)
        to_csv_mock.assert_called_with(OUTPUT_DIR / "pt_life_expectancy.csv", index=False)
