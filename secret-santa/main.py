
import pandas as pd
from sklearn.utils import shuffle
from time import sleep


# Create a data frame with participants
def load_data():
    df = pd.read_csv('participants.csv')
    return df


# Create list of random indexes
def create_indexes(nb_participants):
    indexes = [i+1 for i in range(nb_participants)]
    return shuffle(indexes)


# MAIN OF SCRIPT

if __name__ == '__main__':

    # Load data
    print('\nLoading data...')
    data = load_data()
    sleep(1)

    # Randomize participants
    print('Randomizing participants...')
    n_participants = data.shape[0]
    indexes = create_indexes(n_participants)
    sleep(1)

    # Assign gifts to participants
    print('Assigning gifts to participants...')
    output = pd.DataFrame({'Name': data.Name, 'Gift': indexes}).sort_values('Gift')

    print('\nRESULT TABLE:\n', output)

    output.to_csv('gifts.csv', index=False)
    print('\nAll done. Enjoy!')
