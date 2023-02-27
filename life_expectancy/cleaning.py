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


def load_data():
    ''' Load data '''
    name_file = DATA_DIR / "eu_life_expectancy_raw.tsv"
    csv_table = pd.read_table(name_file, sep='\t')
    return csv_table


def clean_data(csv_table, region_user):
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

    # Filter per region
    filtered_df = df_first_column[df_first_column['region'] == region_user]

    # Ensure "value" is a float
    # First, it identifies which number is really a number
    # or if is other type (ex: ":")
    filtered_df = filtered_df[[filtered_df['value'].iloc[i][0].isdigit()
                               for i in range(0, len(filtered_df))]]

    # Second, when there is a number and a letter (ex. "42.1 e"),
    # it selects only the numbers
    filtered_df['value'] = [filtered_df['value'].iloc[i].split(" ", maxsplit=1)[0]
                            for i in range(0, len(filtered_df))]

    filtered_df['value'] = filtered_df['value'].astype(float)

    # Ensure "year" is an integral
    filtered_df['year'] = filtered_df['year'].astype(int)

    return filtered_df


def save_data(df_final):
    ''' Save data as csv'''
    df_final.to_csv('pt_life_expectancy.csv', index=False)


def main(region_user):
    ''' Load, clean and save data'''
    csv_table = load_data()
    df_final = clean_data(csv_table, region_user)
    save_data(df_final)


if __name__ == '__main__': # pragma: no cover
    REGION_USER = add_region_user()

    main(REGION_USER)
