"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import clean_data
from . import FIXTURES_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""

    name_file = FIXTURES_DIR / "eu_life_expectancy_raw.tsv"
    csv_table = pd.read_table(name_file, sep='\t')
    pt_life_expectancy_actual = clean_data(csv_table, "PT")

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual.reset_index(drop=True), pt_life_expectancy_expected
    )

