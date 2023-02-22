"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import clean_data, load_data, save_data
from . import OUTPUT_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    CSV_TABLE = load_data()
    DF_FINAL = clean_data(CSV_TABLE, 'PT')
    save_data(DF_FINAL)
    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
