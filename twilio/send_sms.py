
import argparse
import configparser
import json
import sys
from twilio.rest import Client


def send_main(recipient, sms_body, path_to_credentials, path_to_register="register.json", sender="twilio"):

    # Load JSON directory
    with open(path_to_register) as f:
        register = json.loads(f.read())

    # Check that the recipient and sender are in the directory
    if recipient not in register.keys():
        sys.exit("Unknown recipient {}".format(recipient))
    if sender not in register.keys():
        sys.exit("Unknown sender {}".format(sender))

    # Read credentials
    config = configparser.ConfigParser()
    config.read(path_to_credentials)

    # Create client using credentials
    client = Client(config.get("TWILIO", "account_sid"), config.get("TWILIO", "auth_token"))

    # Send the SMS using the created client
    message = client.api.account.messages.create(to=register[recipient],
                                                 from_=register[sender],
                                                 body=sms_body)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('recipient', type=str, help='Recipient of the SMS')
    parser.add_argument('body', type=str, help='Body of the SMS')
    parser.add_argument('path_to_credentials', type=str, help='Path to the credentials file')
    parser.add_argument('--path_to_register', "-d", type=str, default='register.json', help='Path to nb register file')
    parser.add_argument('--sender', '-s', type=str, default='twilio', help='Sender of the SMS')

    args = vars(parser.parse_args())

    send_main(args.get('recipient'), args.get('body'), args.get('path_to_credentials'),
              path_to_register=args.get('path_to_register'), sender=args.get('sender'))
