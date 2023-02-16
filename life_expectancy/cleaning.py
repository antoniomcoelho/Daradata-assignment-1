''' Clean data code'''
import pandas as pd
import argparse

def clean_data(region_user):
    ''' Function to clean data from eu_life_expectancy_raw.tsv file'''
    # Transform folder tsv to csv
    name_file = "C:\\Users\\amfcc\\MyDocuments\\Data Engineering\\DareData pod 3\\assignments\\" \
                "life_expectancy\\data\\eu_life_expectancy_raw.tsv" # pylint: disable=line-too-long
    csv_table = pd.read_table(name_file, sep='\t')

    column0 = csv_table.columns[0] # Name of first column
    data = []
    for i in range(0, len(csv_table)): # len(csv_table)
        for j in range(1, len(csv_table.columns)):

            # Split the first column into unit, sex, age and region
            data_prov = csv_table[column0][i].split(',')

            flag = 0 # Indicate if the value is not a value convertible to float (ex. ":")
            # Convert value to float
            ## If the value starts with a number (ex. "42.1")
            if str(csv_table[csv_table.columns[j]][i])[0].isdigit():
                # Split the value when it has a number and a letter (ex. "42.1 e")
                var1 = str(csv_table[csv_table.columns[j]][i]).split(" ", maxsplit=1)[0]
                # Convert value to float
                var1 = float(var1)
            else:
                flag = 1 # The value is not convertible to float (ex. ":")

            if flag == 0:
                if data_prov[3] == region_user: # Select regions that equal to PT (Portugal)
                    # Append year to data_prov (= [unit, sex, age and region, year])
                    data_prov.append(int(csv_table.columns[j]))
                    # Append value of that year (= [unit, sex, age, region, year, value])
                    data_prov.append(var1)
                    data.append(data_prov)

    # Create dataframe and rename columns
    columns_name = {0:'unit', 1:'sex', 2:'age', 3:'region', 4:'year', 5:'value'}
    df_data = pd.DataFrame(data).rename(columns = columns_name)

    # Save csv
    df_data.to_csv('pt_life_expectancy_test.csv', index=False)
    print("clean_data")



if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("region", help="select region",type=str)
    args = parser.parse_args()
    print(args.region)
    clean_data(args.region)
