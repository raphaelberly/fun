
import sys
import requests
import configparser
import argparse


def extract(object, path_to_credentials):
    """
    The aim of this function is to query data from the Zoho API and return it as a UTF-8 string
    :param object: object to query (e.g. "invoices", "expenses")
    :param path_to_credentials: Path to the credentials.ini file
    :return: response string (UTF-8 encoding)
    """
    # Read credentials
    config = configparser.ConfigParser()
    config.read(path_to_credentials)

    # Prepare the query
    url = config.get('ZOHO', 'url')
    params = {'authtoken': config.get('ZOHO', 'authtoken'),
              'organisation_id': config.get('ZOHO', 'organisation_id')}

    # Query the data
    try:
        response = requests.get(url=url.format(object), params=params).content
    except:
        sys.exit('Failed to query {} from Zoho API.'.format(object))
    else:
        print('Data successfully extracted from Zoho API.')

    # Return response
    return response.decode("utf-8")


# If run as a script
if __name__ == '__main__':

    object_list = ['invoices', 'expenses']

    # Create argument parser
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('object', type=str, choices=object_list, help='Object to be queried from Zoho API.')
    parser.add_argument('path_to_credentials', type=str, help='Path to the credentials.ini file')

    # Parse arguments
    args = vars(parser.parse_args())

    # Run main scripts
    response = extract(args.get('object'), args.get('path_to_credentials'))
