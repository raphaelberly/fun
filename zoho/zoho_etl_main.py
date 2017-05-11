"""
MAIN ZOHO ETL

The purpose of this script is to run successively the extract.py, transform.py and load.py scripts in order to perform
the ETL of Zoho data.

It should be run with Python 3. Example cmd:
python invoices 1ovYUVPeCWsujKyPnoADtQz8ly7yGjlTCMNKADp4AqHg ../credentials.ini dump.csv client_secret.json
"""


import argparse
from extract import extract
from transform import transform
from load import load


def main_etl(object, spreadsheet_id, path_to_credentials, path_to_dump, path_to_secret_json):
    """
    Main function of the ETL process. Runs successively extract, transform and load
    :param object: object to query (e.g. "invoices", "expenses")
    :param spreadsheet_id: id of the spreadsheet to upload the data in
    :param path_to_credentials: Path to the credentials.ini file
    :param path_to_dump: Path to the tmp dump
    :param path_to_secret_json: path to the client_secret.json file (Google Spreadsheet credentials)
    :return: None
    """
    # Extract the data
    print('\nExtracting data...')
    response = extract(object, path_to_credentials)

    # Transform the data
    print('\nTransforming data...')
    transform(object, response, path_to_dump)

    # Load the data in the spreadsheet
    print('\nLoading data...')
    load(path_to_dump, spreadsheet_id, path_to_secret_json)


# If run as a script
if __name__ == '__main__':

    object_list = ['invoices', 'expenses', 'creditnotes', 'creditnotes/refunds']

    # Create argument parser
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('object', type=str, choices=object_list, help='Object to be queried from Zoho API.')
    parser.add_argument('spreadsheet_id', type=str, help='ID of the Google spreadsheet to use.')
    parser.add_argument('path_to_credentials', type=str, help='Path to the credentials.ini file')
    parser.add_argument('path_to_dump', type=str, help='Path to the credentials.ini file')
    parser.add_argument('path_to_secret_json', type=str, help='Path to the client_secret.json file')

    # Parse arguments
    args = vars(parser.parse_args())

    # Run main script
    main_etl(args['object'], args['spreadsheet_id'], args['path_to_credentials'], args['path_to_dump'],
             args['path_to_secret_json'])
