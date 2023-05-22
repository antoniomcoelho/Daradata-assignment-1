''' Pipeline for clean data code'''
import sys

from clean_files import Country, CleanFile



def add_region_user() -> str:
    ''' Function to create a command-line option to select the region'''
    try:
        return_value = [sys.argv[2]]
        for i in range(3, len(sys.argv)):
            return_value.append(sys.argv[i])
    except:
        Country.list_countries(Country)

        return_value = ['PT']

    return return_value

def add_file_type_user() -> str:
    ''' Function to create a command-line option to select the file type'''
    try:
        return_value = sys.argv[1]
    except:
        return_value = 'TSV'

    return return_value


def main(region_user: list[str] = ["PT"], file_type: str = "TSV") -> None:
    ''' Load, clean and save data'''
    clean_df = CleanFile(region_user, file_type)

    csv_table = clean_df.load_data()
    df_final = clean_df.clean_data(csv_table, region_user)
    clean_df.save_data(df_final, region_user)


if __name__ == '__main__': # pragma: no cover
    FILE_TYPE = add_file_type_user()
    REGION_USER = add_region_user()

    main(REGION_USER, FILE_TYPE)
