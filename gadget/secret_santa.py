import argparse

import pandas as pd
from sklearn.utils import shuffle
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


# Create list of random indexes
def create_indexes(nb_participants):
    indexes = [i+1 for i in range(nb_participants)]
    return shuffle(indexes)


if __name__ == '__main__':

    # Create arguments parser
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--input', required=True, type=str, help='Path to the input CSV file')
    parser.add_argument('--output', required=True, type=str, help='Path to the output CSV file')

    # Parse arguments
    args = parser.parse_args()

    # Load data
    LOGGER.info('Loading data...')
    data = pd.read_csv(args.input)

    # Randomize participants
    LOGGER.info('Randomizing participants...')
    n_participants = data.shape[0]
    indexes = create_indexes(n_participants)

    # Assign gifts to participants
    LOGGER.info('Assigning gifts to participants...')
    output = pd.DataFrame({'Name': data.name, 'Gift': indexes}).sort_values('Gift')

    output.to_csv(args.output, index=False)
    LOGGER.info('All done. Output file: {}'.format(args.output))
