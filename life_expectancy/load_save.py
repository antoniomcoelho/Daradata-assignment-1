''' Clean data code'''
import argparse
from pathlib import Path # pylint: disable=import-error
import pandas as pd


DATA_DIR = Path(__file__).parent / 'data'


def load_data() -> pd.DataFrame:
    ''' Load data '''
    name_file = DATA_DIR / "eu_life_expectancy_raw.tsv"
    csv_table = pd.read_table(name_file, sep='\t')
    return csv_table


def save_data(df_final: pd.DataFrame) -> None:
    ''' Save data as csv'''
    df_final.to_csv(DATA_DIR / 'pt_life_expectancy.csv', index=False)

