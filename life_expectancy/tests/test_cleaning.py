"""Tests for the cleaning module"""
import pandas as pd

<<<<<<< HEAD
from life_expectancy.cleaning import main
=======
from life_expectancy.cleaning import clean_data, load_data, save_data
>>>>>>> 221def6ae36a2de6a8cac9897e747ef97c69e0a4
from . import OUTPUT_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
<<<<<<< HEAD
    main("PT")
=======
    CSV_TABLE = load_data()
    DF_FINAL = clean_data(CSV_TABLE, 'PT')
    save_data(DF_FINAL)
>>>>>>> 221def6ae36a2de6a8cac9897e747ef97c69e0a4
    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
