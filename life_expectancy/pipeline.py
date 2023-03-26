''' Pipeline for clean data code'''
import argparse
from life_expectancy.load_save import load_data, save_data
from life_expectancy.cleaning import clean_data



def add_region_user():
    ''' Function to create a command-line option to select the region'''
    region_user_parser = argparse.ArgumentParser()
    region_user_parser.add_argument("region", help="select region", type=str)
    args = region_user_parser.parse_args()

    return args.region


def main(region_user: str = "PT") -> None:
    ''' Load, clean and save data'''
    csv_table = load_data()
    df_final = clean_data(csv_table, region_user)
    save_data(df_final)


if __name__ == '__main__': # pragma: no cover
    REGION_USER = add_region_user()

    main(REGION_USER)


