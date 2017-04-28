
import sys
import json
import pandas as pd


def transform(response_str, path_to_dump):
    """
    The aim of this function is to transform the data received from Zoho API and to store the result into a CSV dump.
    :param response_str: response string (UTF-8 encoding) of the API request
    :param path_to_dump: Path to the tmp dump
    :return: None
    """
    raw_json = json.loads(response_str)
    invoices = raw_json['invoices']

    df = pd.DataFrame(invoices)

    field_list = ["balance", "cf_407503000000062122", "cf_deposit", "cf_pick_up", "created_time", "currency_code",
                  "currency_id", "customer_id", "customer_name", "date", "due_date", "due_days", "exchange_rate",
                  "invoice_id", "invoice_number", "is_emailed", "is_viewed_by_client", "last_modified_time",
                  "last_payment_date", "last_reminder_sent_date", "payment_expected_date", "reminders_sent", "status",
                  "total"]

    df = df[field_list]

    try:
        df.to_csv(path_to_dump, index=False)
    except:
        sys.exit('Could not dump data at the specified location.')
    else:
        print('Data successfully transformed and dumped at the specified location.')
