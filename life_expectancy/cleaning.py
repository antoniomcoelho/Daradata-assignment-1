''' Clean data code'''
import argparse
from pathlib import Path # pylint: disable=import-error
import pandas as pd


DATA_DIR = Path(__file__).parent / 'data'



def add_region_user():
    ''' Function to create a command-line option to select the region'''
    region_user_parser = argparse.ArgumentParser()
    region_user_parser.add_argument("region", help="select region", type=str)
    args = region_user_parser.parse_args()

    return args.region


def load_data() -> pd.DataFrame:
    ''' Load data '''
    name_file = DATA_DIR / "eu_life_expectancy_raw.tsv"
    csv_table = pd.read_table(name_file, sep='\t')
    return csv_table


def clean_data(csv_table: pd.DataFrame, region_user: str) -> pd.DataFrame:
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

    filtered_df = df_first_column[df_first_column['region'].isin([region_user])].copy()

    filtered_df = convert_value_to_float(filtered_df)

    filtered_df['year'] = filtered_df['year'].astype(int)

    return filtered_df

def convert_value_to_float(filtered_df: pd.DataFrame) -> pd.DataFrame:
    ''' Function to convert the column "values" to float '''
    filtered_df['value'] = filtered_df['value'].str.replace(r'[^0-9.]+', '', regex=True)
    filtered_df['value'] = pd.to_numeric(filtered_df['value'], errors='coerce')
    filtered_df = filtered_df.dropna(subset=['value'])

    return filtered_df

def save_data(df_final: pd.DataFrame) -> None:
    ''' Save data as csv'''
    df_final.to_csv('pt_life_expectancy.csv', index=False)


def main(region_user: str = "PT") -> None:
    ''' Load, clean and save data'''
    csv_table = load_data()
    df_final = clean_data(csv_table, region_user)
    save_data(df_final)


if __name__ == '__main__': # pragma: no cover
    #REGION_USER = add_region_user()
    REGION_USER = 'PT'
    main(REGION_USER)
