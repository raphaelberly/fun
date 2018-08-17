
import pandas as pd
from sklearn.utils import shuffle
import numpy as np
import argparse
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def create_indexes(nb_participants):
    """
    Create list of random indexes.
    :param nb_participants: size of the list of random indexes to create
    :return: shuffled list of integers from 0 to nb_participants-1
    """
    indexes = [i for i in range(nb_participants)]
    return shuffle(shuffle(indexes))


# Main function of the script
def main(input_file, output_file, team_size):
    """
    Creates random N-person teams, using a list of names and a provided team size. The output is written as a CSV file
    at the specified location/
    :param input_file: path to the input CSV file
    :param output_file: path to the output CSV file
    :param team_size: minimum size of the teams to create
    :return: None
    """
    # Load data
    LOGGER.info('Loading data...')
    data = pd.read_csv(input_file, header=0)

    # Randomize participants
    LOGGER.info('Randomizing participants...')
    n_participants = data.shape[0]
    indexes = create_indexes(n_participants)
    nb_teams = n_participants // team_size

    # Assign teams
    LOGGER.info('Assigning teams...')
    data['Team'] = pd.Series(np.mod(indexes, nb_teams))
    data = data.sort_values('Team').reset_index(drop=True)

    data.to_csv(output_file, index=False)
    LOGGER.info('All done. Output file: {}'.format(output_file))


if __name__ == '__main__':

    # Create a parser to get the number of teams
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--input', required=True, type=str, help='Path to the input CSV file')
    parser.add_argument('--output', required=True, type=str, help='Path to the output CSV file')
    parser.add_argument('--team_size', required=True, type=int, help='Minimum number of participants per team')

    # Parse the entered argument
    args = parser.parse_args()

    # Run the main function of the file
    main(args.input, args.output, args.team_size)

