
import pandas as pd
from sklearn.utils import shuffle
from time import sleep
import numpy as np


# Create a data frame with participants
def load_data():
    df = pd.read_csv('participants.csv')
    return df


# Create list of random indexes
def create_indexes(nb_participants):
    indexes = [i for i in range(nb_participants)]
    return shuffle(indexes)


# MAIN OF SCRIPT

if __name__ == '__main__':

    NUMBER_OF_GROUPS = 7

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
    data['Team'] = pd.Series(np.mod(indexes, NUMBER_OF_GROUPS))
    data = data.sort_values('Team').reset_index(drop=True)
    print('\nRESULT TABLE:\n', data)

    data.to_csv('teams.csv', index=False)
    print('\nAll done. Enjoy!')
