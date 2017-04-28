
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import RequestError


def load(path_to_dump, spreadsheet_id, path_to_secret_json):
    """
    This function loads the data from a CSV dump into a spreadsheet
    :param path_to_dump: Path to the tmp dump
    :param spreadsheet_id: id of the spreadsheet to upload the data in
    :param path_to_secret_json: path to the client_secret.json file (Google Spreadsheet credentials)
    :return: None
    """
    # Use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(path_to_secret_json, scope)
    client = gspread.authorize(creds)

    # Load the CSV to be uploaded to the spreadsheet
    with open(path_to_dump) as f:
        dump_str = f.read()

    # Upload CSV dump on the first sheet of the spreadsheet
    try:
        client.import_csv(spreadsheet_id, dump_str)
    except RequestError:
        sys.exit('Invalid request. Please check permissions and spreadsheet ID.')
    else:
        print('CSV dump successfuly loaded to spreadsheet {}'.format(spreadsheet_id))
