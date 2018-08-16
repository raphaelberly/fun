
"""
IBAN CHECKER

The aim of this script is to check whether a French IBAN is correct or not, by computing the key and comparing it to the
entered one.
"""

import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def to_digit_str(iban):
    """
    The aim of this function is to create a lowercase digit string based on the IBAN provided as a string as a
    parameter of the function.
    :param iban: string of the IBAN. Spaces are ignored
    :return: iban digit string (letters replaced by numbers)
    """

    # Prepare the letter dictionary to be used to convert letters to digits
    letter_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 1,
                   'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9, 's': 2, 't': 3,
                   'u': 4, 'v': 5, 'w': 6, 'x': 7, 'y': 8, 'z': 9}

    digit_list = []
    for character in iban.lower():
        if character.isdigit():
            digit_list.append(character)
        elif character.isalpha():
            digit_list.append(str(letter_dict[character]))
        elif character == " ":
            pass
        else:
            sys.exit('Invalid character '.format(character))

    return "".join(digit_list)


def get_iban_key(iban_account_number):
    """
    This function aims at computing the IBAN key, given the iban account number
    :param iban_account_number: iban account number, string of 21 characters
    :return: 2-digit string (key)
    """

    # Check that the iban account number is the right length and the right format
    assert len(iban_account_number) == 21, 'Invalid input parameter: length should be 21'

    iban_account_number_str = to_digit_str(iban_account_number)

    # Compute the variables to be used for the computation of the key
    b = int(iban_account_number_str[0:5])
    g = int(iban_account_number_str[5:10])
    c = int(iban_account_number_str[10:21])

    # Compute the key
    key = 97 - ((89 * b + g * 15 + 3 * c) % 97)

    # Return the key string
    return '{:02d}'.format(key)


def check_iban(iban):
    """
    This function aims at using get_iban_key to check whether a provided IBAN is correct or invalid.
    :param iban: IBAN string to be tested
    :return: True if the IBAN is correct, False if it is not
    """

    # Remove spaces from the IBAN string
    iban_cln = "".join([letter for letter in iban if letter != " "])

    # Proceed with some checks
    assert len(iban_cln) == 27, 'Invalid IBAN: provided length should be 27'
    assert iban_cln.isalnum(), 'Invalid IBAN: must be alphanumerical'

    # Compute the IBAN key based on the iban account number
    iban_account_number = iban_cln[4:25]
    key = get_iban_key(iban_account_number)

    # Return True if the IBAN is correct, False if it is not
    return key == iban_cln[-2:]


if __name__ == '__main__':

    # Create arguments parser
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('iban', type=str, help='IBAN to check (string format, can contain spaces)')

    # Parse arguments
    args = parser.parse_args()
    iban = args.iban

    # Print the result of the check
    if check_iban(iban):
        LOGGER.info('\nYay. The specified IBAN is correct.\n')
    else:
        LOGGER.error('\nInvalid IBAN!!\n')
