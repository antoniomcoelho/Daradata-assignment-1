''' Clean data code'''
import argparse
import pandas as pd


def clean_data(region_user):
    ''' Function to clean data from eu_life_expectancy_raw.tsv file'''
    # Read tsv file and transform it to csv
    csv_table = read_file()

    column0 = csv_table.columns[0] # Name of first column
    data = [] # Vector with all fields
    for i in range(0, len(csv_table)): # len(csv_table)
        for j in range(1, len(csv_table.columns)):
            # Split the first column into unit, sex, age and region
            data_prov = csv_table[column0][i].split(',')

            # Convert value to float
            value, flag_value_is_not_float = convert_value_to_float(csv_table, j, i)

            # Append necessary information (unit, sex, age and region, year)
            data = append_information(data_prov, data, flag_value_is_not_float,
                                      region_user, csv_table, value, j)         # pylint: disable=line-too-long


    # Create dataframe and rename columns
    columns_name = {0:'unit', 1:'sex', 2:'age', 3:'region', 4:'year', 5:'value'}
    df_data = pd.DataFrame(data).rename(columns=columns_name)

    # Save csv
    df_data.to_csv('pt_life_expectancy.csv', index=False)

def read_file():
    ''' Read tsv file and transform it to csv '''
    name_file = "C:\\Users\\amfcc\\MyDocuments\\Data Engineering\\DareData pod 3\\assignments\\" \
                "life_expectancy\\data\\eu_life_expectancy_raw.tsv"             # pylint: disable=line-too-long
    csv_table = pd.read_table(name_file, sep='\t')

    return csv_table

def convert_value_to_float(csv_table, j, i):
    ''' Convert value to float '''
    value = 0
    flag = 0  # Indicate if the value is not a value convertible to float (ex. ":")

    # If the value starts with a number (ex. "42.1")
    if str(csv_table[csv_table.columns[j]][i])[0].isdigit():
        # Split the value when it has a number and a letter (ex. "42.1 e")
        value = str(csv_table[csv_table.columns[j]][i]).split(" ", maxsplit=1)[0]
        # Convert value to float
        value = float(value)
    else:
        flag = 1  # The value is not convertible to float (ex. ":")

    return value, flag

def append_information(data_prov, data, flag_value_is_not_float, region_user,   # pylint: disable=too-many-arguments
                       csv_table, value, j):                                    # pylint: disable=too-many-arguments
    ''' Append necessary information (unit, sex, age and region, year) to data vector '''
    if flag_value_is_not_float == 0:
        if data_prov[3] == region_user:  # Select regions that equal to region  # pylint: disable=line-too-long
                                            # defined by the user (region_user) # pylint: disable=line-too-long
            # Append year to data_prov (= [unit, sex, age and region, year])
            data_prov.append(int(csv_table.columns[j]))
            # Append value of that year (= [unit, sex, age, region, year, value])
            data_prov.append(value)
            data.append(data_prov)
    return data

def add_region_user():
    ''' Function to create a command-line option to select the region'''
    region_user_parser = argparse.ArgumentParser()
    region_user_parser.add_argument("region", help="select region", type=str)
    args = region_user_parser.parse_args()

    return args.region

if __name__ == '__main__': # pragma: no cover
    REGION_USER = add_region_user()
    clean_data(REGION_USER)
