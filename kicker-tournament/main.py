
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from time import sleep


# Create a data frame with data from survey

def load_data():
    data = pd.read_csv('survey.csv')
    data['player'] = data['Your Name'].str.cat(data['Your Company'], sep=', ')
    data['position'] = data['Your Position']

    return data[['player', 'position']]


def assign_partners(dataframe):

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


# IF RUN AS A SCRIPT

if __name__ == '__main__':
    # Load data
    print('\nLoading data...')
    players = load_data()
    sleep(1)

    print('Shuffle data...')
    # Get the team indexes lists
    indexes_defense, indexes_offense = assign_partners(players)
    sleep(1)

    print('Create teams...')
    sleep(1)
    # Create the final data frame and export it
    df = pd.DataFrame({'defense': players.player[indexes_defense].values,
                       'offense': players.player[indexes_offense].values})
    print('\nRESULT TABLE:\n', df)

    df.to_csv('teams.csv', index=False)
    print('\nAll done. Enjoy!')
