
"""
SEND SMS

This script aims at providing the necessary functions to send SMS from Python using Twilio. All Twilio-registered
numbers should be provided in a register.json file, and the credentials provided in a credentials.ini file.
"""


import argparse
import configparser
import json
import sys
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def get_numbers_from_register(recipient_name, sender_name="twilio", path_to_register="register.json"):
    """
    Gets the phone numbers of the specified users in the register. If the specified name is not in the register,
    throws an error.
    :param recipient_name: name of the recipient of the SMS
    :param sender_name: name of the sender of the SMS, twilio by default (sending number of the BI team)
    :param path_to_register: path to register.json file
    :return: (recipient_number, sender_number) tuple
    """

    # Load JSON directory
    with open(path_to_register) as f:
        register = json.loads(f.read())

    # Check that the recipient_name and sender_name are in the directory
    if recipient_name not in register.keys():
        sys.exit("Unknown recipient_name {}".format(recipient_name))
    if sender_name not in register.keys():
        sys.exit("Unknown sender_name {}".format(sender_name))

    # Return (recipient_number, sender_number) tuple
    return register[recipient_name], register[sender_name]


def send_sms(recipient_name, sms_body, path_to_credentials, path_to_register="register.json", sender_name="twilio"):
    """
    This function sends an SMS to the provided recipient to the provided sender.
    :param recipient_name: name of the recipient of the SMS
    :param sms_body: body of the SMS
    :param path_to_credentials: path to the credentials file
    :param path_to_register: path to register.json file
    :param sender_name: name of the sender of the SMS, twilio by default (sending number of the BI team)
    :return: None
    """
    # Read credentials
    config = configparser.ConfigParser()
    config.read(path_to_credentials)

    # Create client using credentials
    client = Client(config.get("TWILIO", "account_sid"), config.get("TWILIO", "auth_token"))

    # Get recipient_name and sender_name numbers
    recipient_number, sender_number = get_numbers_from_register(recipient_name, sender_name, path_to_register)

    # Send the SMS using the created client
    try:
        client.api.account.messages.create(to=recipient_number, from_=sender_number, body=sms_body)
    except TwilioRestException:
        sys.exit('Twilio REST API could not send SMS. Please check sender number is valid and recipient is registered.')
    except TimeoutError:
        sys.exit('Operation timed out. SMS was not sent.')
    else:
        print('SMS was sent successfully to {}.'.format(recipient_name))


# IF RUN AS A SCRIPT
if __name__ == '__main__':

    # Create argument parser
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('recipient', type=str, help='Recipient of the SMS')
    parser.add_argument('body', type=str, help='Body of the SMS')
    parser.add_argument('path_to_credentials', type=str, help='Path to the credentials file')
    parser.add_argument('--path_to_register', "-d", type=str, default='register.json', help='Path to nb register file')
    parser.add_argument('--sender', '-s', type=str, default='twilio', help='Sender of the SMS')

    # Parse arguments
    args = vars(parser.parse_args())

    # Send the SMS
    send_sms(args.get('recipient'), args.get('body'), args.get('path_to_credentials'),
             path_to_register=args.get('path_to_register'), sender_name=args.get('sender'))
