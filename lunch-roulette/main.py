
import pandas as pd
from sklearn.utils import shuffle
from time import sleep
import numpy as np
import argparse


# Create a data frame with participants
def load_data():
    df = pd.read_csv('participants.csv')
    return df


# Create list of random indexes
def create_indexes(nb_participants):
    indexes = [i for i in range(nb_participants)]
    return shuffle(indexes)


# Main function of the script
def main(nb_teams):

    # Load data
    print('\nLoading data...')
    data = load_data()
    sleep(1)

    # Randomize participants
    print('Randomizing participants...')
    n_participants = data.shape[0]
    indexes = create_indexes(n_participants)
    sleep(1)

    # Assign teams
    print('Assigning teams...')
    data['Team'] = pd.Series(np.mod(indexes, nb_teams))
    data = data.sort_values('Team').reset_index(drop=True)
    print('\nRESULT TABLE:\n', data)

    data.to_csv('teams.csv', index=False)
    print('\nAll done. Enjoy!')



# MAIN OF SCRIPT

if __name__ == '__main__':

    # Create a parser to get the number of teams
    argparser = argparse.ArgumentParser(add_help=False)
    argparser.add_argument('nb_teams', type=str, help='Number of teams to create')

    # Parse the entered argument
    nb_teams = int(vars(argparser.parse_args())['nb_teams'])

    # Run the main function of the file
    main(nb_teams)

