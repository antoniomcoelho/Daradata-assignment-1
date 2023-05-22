''' Clean data code'''
import argparse
from pathlib import Path # pylint: disable=import-error
import pandas as pd
from abc import ABC, abstractmethod
import numpy as np
from enum import Enum, unique


DATA_DIR = Path(__file__).parent / 'data'



class Country(Enum):
    ''' List of possible countries '''
    Portugal = 'PT'
    Belgium = 'BE'
    Denmark = 'DK'
    Spain = 'SP'

    def list_countries(cls):
        print('List of countries:')
        for country in cls:
            print("    ", country.name, ":", country.value)
        countries = [country.value for country in cls]
        return countries


class DataFormatsStrategy(ABC):
    """ Definition of strategy classes"""
    @abstractmethod
    def load_data(self):
        """ Loads data files """

    @abstractmethod
    def clean_data(self, csv_table: pd.DataFrame, region_user: list[str] = ['PT']) -> pd.DataFrame:
        """ Clean data files """


class TSVstrategy(DataFormatsStrategy):
    def load_data(self):
        ''' Load data from TSV files '''
        name_file = DATA_DIR / "eu_life_expectancy_raw.tsv"
        csv_table = pd.read_table(name_file, sep='\t')
        return csv_table

    def clean_data(self, csv_table: pd.DataFrame, region_user: list[str] = ['PT']) -> pd.DataFrame:
        ''' Function to clean data from eu_life_expectancy_raw.tsv file'''
        first_column = csv_table.columns[0]
        other_cols = csv_table.columns[1:]
        first_column_split = ['unit', 'sex', 'age', 'region']

        # Split the values of the first column into 'unit', 'sex', 'age', 'region'
        csv_table[first_column_split] = csv_table[first_column].str.split(',', expand=True)

        # Expand the "value" according to "year"
        selected_columns = list(first_column_split) + list(other_cols)
        df_first_column = csv_table[selected_columns]
        df_first_column = df_first_column.melt(id_vars=first_column_split,
                                               var_name="year", value_name="value")
        filtered_df_list = []

        for region in region_user:
            filtered_df = df_first_column[df_first_column['region'].isin([region])].copy()
            filtered_df = self._convert_value_to_float(filtered_df)
            filtered_df['year'] = filtered_df['year'].astype(np.int64)
            filtered_df_list.append(filtered_df)

        return filtered_df_list

    def _convert_value_to_float(self, filtered_df: pd.DataFrame) -> pd.DataFrame:
        ''' Function to convert the column "values" to float '''
        filtered_df['value'] = filtered_df['value'].str.replace(r'[^0-9.]+', '', regex=True)
        filtered_df['value'] = pd.to_numeric(filtered_df['value'], errors='coerce')
        filtered_df = filtered_df.dropna(subset=['value'])

        return filtered_df


class JSONstrategy(DataFormatsStrategy):
    def load_data(self):
        ''' Load data from JSON files '''
        name_file = DATA_DIR / "eurostat_life_expect.json"
        csv_table = pd.read_json(name_file)
        return csv_table

    def clean_data(self, csv_table: pd.DataFrame, region_user: list[str] = ['PT']) -> pd.DataFrame:
        ''' Function to clean data '''
        selected_columns = ['unit', 'sex', 'age', 'country', 'year', 'life_expectancy']

        df_first_column = csv_table[selected_columns]
        filtered_df_list = []
        for region in region_user:
            filtered_df = df_first_column[df_first_column['country'].isin([region])].copy()
            filtered_df['year'] = filtered_df['year'].astype(np.int64)
            filtered_df_list.append(filtered_df)

        return filtered_df_list


class CleanFile:
    def __init__(self, region_user: list[str], file_type: str):
        self.region_user = region_user
        self.file_type = file_type
        self.strategies: Dict[str: dataFormatsStrategy] = {
            "TSV": TSVstrategy(),
            "JSON": JSONstrategy(),
            None: TSVstrategy(),
        }

    def load_data(self) -> pd.DataFrame:
        ''' Function to load the data '''
        csv_table = self.strategies[self.file_type].load_data()
        return csv_table

    def clean_data(self, csv_table: pd.DataFrame, region_user: str = 'PT') -> pd.DataFrame:
        ''' Function to clean data '''
        filtered_df = self.strategies[self.file_type].clean_data(csv_table, region_user)

        return filtered_df

    def save_data(self, df_final: pd.DataFrame, region_user: list[str]) -> None:
        ''' Save data as csv '''
        for i in range(0, len(df_final)):
            df_final[i].to_csv(DATA_DIR / f'{region_user[i].lower()}_life_expectancy.csv', index=False)



