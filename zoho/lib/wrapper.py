import json
import logging
import os
import sys

import gspread
import pandas as pd
import requests
import yaml
from gspread.exceptions import RequestError
from oauth2client.service_account import ServiceAccountCredentials

LOGGER = logging.getLogger(__name__)


class ZohoWrapper:

    def __init__(self, config_folder, secret_json, dump_file='dump.txt'):

        with open(os.path.join(config_folder, 'credentials.yaml')) as f:
            self.config = {'credentials': yaml.load(f)}

        with open(os.path.join(config_folder, 'config.yaml')) as f:
            self.config.update(yaml.load(f))

        self.secret_json = secret_json
        self.dump_file = dump_file

    def extract(self, object):
        """
        The aim of this function is to query data from the Zoho API and return it as a UTF-8 string
        :param object: object to query (e.g. "invoices", "expenses")
        :return: response string (UTF-8 encoding)
        """
        LOGGER.info('Extracting data...')

        # Prepare the query
        url = self.config['credentials']['url']
        params = {'authtoken': self.config['credentials']['authtoken'],
                  'organization_id': self.config['credentials']['organization_id']}

        # Query the data
        try:
            response = requests.get(url=url.format(object), params=params).content
        except:
            sys.exit('Failed to query {} from Zoho API.'.format(object))
        else:
            LOGGER.info('Data successfully extracted from Zoho API.')

        # Return response
        return response.decode("utf-8")

    def transform(self, object, response_str):
        """
        The aim of this function is to transform the data received from Zoho API and to store the result into a CSV dump.
        :param response_str: response string (UTF-8 encoding) of the API request
        :param path_to_dump: Path to the tmp dump
        :return: None
        """
        LOGGER.info('Transforming data...')

        raw_json = json.loads(response_str)
        data = raw_json[self._get_name_from_object(object)]

        df = pd.DataFrame(data)

        if object in self.config['field_list']:
            field_list = self.config['field_list'][object]
        else:
            field_list = df.columns

        df = df[field_list]

        try:
            df.to_csv(self.dump_file, index=False)
        except:
            sys.exit('Could not dump data at the specified location.')
        else:
            LOGGER.info('Data successfully transformed and dumped at the specified location.')
    
    @staticmethod
    def _get_name_from_object(object):
        """
        The aim of this function is to compute the name used in the extracted JSON file from the name of the object
        :param object: object to query (e.g. "invoices", "expenses")
        :return: name used in the extracted JSON file
        """
        return '_'.join(object.split('s/'))

    def load(self, spreadsheet_id):
        """
        This function loads the data from a CSV dump into a spreadsheet
        :param spreadsheet_id: id of the spreadsheet to upload the data in
        :return: None
        """
        LOGGER.info('Loading data to spreadsheet {}'.format(spreadsheet_id))
        
        # Use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.secret_json, scope)
        client = gspread.authorize(creds)

        # Load the CSV to be uploaded to the spreadsheet
        with open(self.dump_file) as f:
            dump_str = f.read()

        # Upload CSV dump on the first sheet of the spreadsheet
        try:
            client.import_csv(spreadsheet_id, dump_str)
        except RequestError:
            sys.exit('Invalid request. Please check permissions and spreadsheet ID.')
        else:
            LOGGER.info('CSV dump successfuly loaded to spreadsheet {}'.format(spreadsheet_id))
