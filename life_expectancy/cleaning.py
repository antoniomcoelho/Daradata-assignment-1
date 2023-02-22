''' Clean data code'''
import argparse
from pathlib import Path # pylint: disable=import-error
import pandas as pd


DATA_DIR = Path(__file__).parent / 'data'


def load_data():
    ''' Read tsv file and transform it to csv '''
    name_file = DATA_DIR / "eu_life_expectancy_raw.tsv"
    csv_table = pd.read_table(name_file, sep='\t')

    return csv_table


def clean_data(csv_table, region_user):
    ''' Function to clean data from eu_life_expectancy_raw.tsv file'''

    first_column = csv_table.columns[0]
    df_life = []

    for i in range(0, len(csv_table)):
        for j in range(1, len(csv_table.columns)):
            # Split the first column into unit, sex, age and region
            df_first_column = csv_table[first_column][i].split(',')

            # Convert value to float
            value, flag_value_is_not_float = convert_value_to_float(csv_table, j, i)

            # Append necessary information (unit, sex, age and region, year)
            df_life = append_information(df_first_column, df_life, flag_value_is_not_float,
                                         region_user, csv_table, value, j)

    # Rename columns and create dataframe
    columns_name = {0: 'unit', 1: 'sex', 2: 'age', 3: 'region', 4: 'year', 5: 'value'}
    df_life = pd.DataFrame(df_life).rename(columns=columns_name)

    return df_life




def convert_value_to_float(csv_table, j, i):
    ''' Convert value to float '''
    value = 0

    # 0 - it is convertible, 1 - it is not convertible
    flag_value_is_not_convertible = 0

    # If the value starts with a number (ex. "42.1"),
    # otherwise it is a word and not convertible to float
    if str(csv_table[csv_table.columns[j]][i])[0].isdigit():
        # Split the value when it has a number and a letter (ex. "42.1 e")
        value = str(csv_table[csv_table.columns[j]][i]).split(" ", maxsplit=1)[0]
        value = float(value)
    else:
        flag_value_is_not_convertible = 1  # The value is not convertible to float (ex. ":")

    return value, flag_value_is_not_convertible


def append_information(df_prov, df_life, region_user,  # pylint: disable=too-many-arguments
                       flag_value_is_not_float,
                       csv_table, value, j):  # pylint: disable=too-many-arguments
    ''' Append necessary information (unit, sex, age and region, year) to data vector '''
    region_column = 3
    if flag_value_is_not_float == 0:
        # Filters selected regions
        if df_prov[region_column] == region_user:

            # Append "year" (= [unit, sex, age and region, year])
            df_prov.append(int(csv_table.columns[j]))

            # Append "value" of that "year" (= [unit, sex, age, region, year, value])
            df_prov.append(value)
            df_life.append(df_prov)

    return df_life

def save_data(df_life):
    ''' Save data as csv'''
    df_life.to_csv('pt_life_expectancy.csv', index=False)


def add_region_user():
    ''' Function to create a command-line option to select the region'''
    region_user_parser = argparse.ArgumentParser()
    region_user_parser.add_argument("region", help="select region", type=str)
    args = region_user_parser.parse_args()

    return args.region


if __name__ == '__main__': # pragma: no cover
    REGION_USER = add_region_user()

    CSV_TABLE = load_data()

    DF_FINAL = clean_data(CSV_TABLE, REGION_USER)

    save_data(DF_FINAL)
