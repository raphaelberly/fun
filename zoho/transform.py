
import sys
import json
import pandas as pd


def get_name_from_object(object):
    """
    The aim of this function is to compute the name used in the extracted JSON file from the name of the object
    :param object: object to query (e.g. "invoices", "expenses")
    :return: name used in the extracted JSON file
    """
    return '_'.join(object.split('s/'))


def transform(object, response_str, path_to_dump):
    """
    The aim of this function is to transform the data received from Zoho API and to store the result into a CSV dump.
    :param response_str: response string (UTF-8 encoding) of the API request
    :param path_to_dump: Path to the tmp dump
    :return: None
    """
    raw_json = json.loads(response_str)
    data = raw_json[get_name_from_object(object)]

    df = pd.DataFrame(data)

    if object == 'invoices':
        field_list = ["balance", "cf_407503000000062122", "cf_deposit", "cf_pick_up", "cf_platform", "created_time",
                      "currency_code", "currency_id", "customer_id", "customer_name", "date", "due_date", "due_days",
                      "exchange_rate", "invoice_id", "invoice_number", "is_emailed", "is_viewed_by_client",
                      "last_modified_time", "last_payment_date", "last_reminder_sent_date", "payment_expected_date",
                      "reminders_sent", "status", "total"]

    elif object == 'expenses':
        field_list = ['account_name', 'bcy_total', 'bcy_total_without_tax', 'cf_company_paid', 'cf_paid_by',
                      'cf_povrnjeno', 'created_time', 'currency_code', 'currency_id', 'custom_fields_list',
                      'customer_id', 'customer_name', 'date', 'description', 'distance', 'end_reading', 'exchange_rate',
                      'expense_id', 'expense_receipt_name', 'expense_type', 'has_attachment', 'is_billable',
                      'is_personal', 'last_modified_time', 'mileage_rate', 'mileage_type', 'mileage_unit',
                      'reference_number', 'report_id', 'report_name', 'start_reading', 'status', 'total',
                      'total_without_tax']

    elif object == 'creditnotes' or object == 'creditnotes/refunds':
        field_list = df.columns

    else:
        sys.exit('Object {} not yet supported by the transform function'.format(object))

    df = df[field_list]

    try:
        df.to_csv(path_to_dump, index=False)
    except:
        sys.exit('Could not dump data at the specified location.')
    else:
        print('Data successfully transformed and dumped at the specified location.')
