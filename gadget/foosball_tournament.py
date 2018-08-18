import argparse

import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def assign_roles(dataframe):
    """
    Assigne a role to each player from the input (i.e. assign "No preference" players to "Offense" or "Defense")
    :param dataframe: input pandas dataframe containing two columns: players,position
    :return: two shuffled lists of player indexes, one for offense and the other one for defense
    """

    n_defense = dataframe.position.value_counts()['Defense']
    n_offense = dataframe.position.value_counts()['Offense']
    n_both = dataframe.position.value_counts()['No preference']

    # Assert data format correct
    assert dataframe.shape[0] % 2 == 0, 'There should be an even number of players.'
    assert np.min([n_defense, n_offense]) + n_both >= np.max([n_defense, n_offense]), 'Positions are too unbalanced.'

    indexes_defense = []
    indexes_offense = []
    indexes_both = []

    for index, row in dataframe.iterrows():
        if row[1] == 'Defense': indexes_defense.append(index)
        if row[1] == 'Offense': indexes_offense.append(index)
        if row[1] == 'No preference': indexes_both.append(index)

    n_both_defense = n_offense - n_defense if n_offense > n_defense else 0
    n_both_offense = n_defense - n_offense if n_defense > n_offense else 0
    n_both_rest = (n_both - n_both_offense - n_both_defense) // 2

    indexes_defense += indexes_both[:(n_both_defense + n_both_rest)]
    indexes_offense += indexes_both[(n_both_defense + n_both_rest):]

    return shuffle(indexes_defense), shuffle(indexes_offense)


if __name__ == '__main__':

    # Create arguments parser
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--input', required=True, type=str, help='Path to the input CSV file')
    parser.add_argument('--output', required=True, type=str, help='Path to the output CSV file')

    # Parse arguments
    args = parser.parse_args()

    # Load data
    LOGGER.info('Loading data...')
    players = pd.read_csv(args.input)[['player', 'position']]

    LOGGER.info('Shuffling data...')
    # Get the team indexes lists
    indexes_defense, indexes_offense = assign_roles(players)

    LOGGER.info('Creating teams...')
    # Create the final data frame and export it
    df = pd.DataFrame({'defense': players.player[indexes_defense].values,
                       'offense': players.player[indexes_offense].values})

    df.to_csv(args.output, index=False)
    LOGGER.info('All done. Output file: {}'.format(args.output))
