
import pandas as pd
from sklearn.utils import shuffle
import numpy as np
import argparse
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


# Create a data frame with participants
def load_data(input_file):
    df = pd.read_csv(input_file, header=0)
    df.columns = ['name']
    return df


# Create list of random indexes
def create_indexes(nb_participants):
    indexes = [i for i in range(nb_participants)]
    return shuffle(shuffle(indexes))


# Main function of the script
def main(input_file, output_file, team_size):

    # Load data
    LOGGER.info('Loading data...')
    data = load_data(input_file)

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


# MAIN OF SCRIPT

if __name__ == '__main__':

    # Create a parser to get the number of teams
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--input', required=True, type=str, help='Path to the input CSV file')
    parser.add_argument('--output', required=True, type=str, help='Path to the output CSV file')
    parser.add_argument('--team_size', required=True, type=int, help='Number of participants per team')

    # Parse the entered argument
    args = parser.parse_args()

    # Run the main function of the file
    main(args.input, args.output, args.team_size)

