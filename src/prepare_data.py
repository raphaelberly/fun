
# PREPARATION DATA FUNCTIONS

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

def get_train_datasets(raw_data):

    raw_data = raw_data.drop(['Name', 'Ticket', 'Cabin'], axis=1)  # Drop useless features
    raw_data = raw_data.set_index('PassengerId')
    raw_data['Age'] = raw_data['Age'].fillna(-1)  # Fill missing ages
    raw_data['Embarked'] = raw_data['Embarked'].fillna('X')  # Fill missing Embarked

    X_train = raw_data.drop('Survived', axis=1)
    y_train = raw_data['Survived']

    return X_train, y_train


def get_test_datasets(raw_data):

    raw_data = raw_data.drop(['Name', 'Ticket', 'Cabin'], axis=1)  # Drop useless features
    raw_data = raw_data.set_index('PassengerId')
    raw_data['Age'] = raw_data['Age'].fillna(-1)  # Fill missing ages
    raw_data['Embarked'] = raw_data['Embarked'].fillna('X')  # Fill missing Embarked
    raw_data['Fare'] = raw_data['Fare'].fillna(np.mean(raw_data.Fare))

    return raw_data


def dummify(X):

    # This function will dummify X

    aux = pd.get_dummies(X[['Embarked']])
    X = X.drop(['Embarked'], 1).join(aux)
    try: X = X.drop('Embarked_X', 1)
    except ValueError: pass

    return X


def fill_ages_train(X_train):

    Xf_train = X_train[X_train.Age >= 0]
    yf_train = Xf_train['Age']
    Xf_train = Xf_train.drop('Age', 1, errors='ignore')

    Xf_test = X_train[X_train.Age == -1].drop('Age', 1, errors='ignore')

    clf = KNeighborsRegressor()
    clf.fit(Xf_train, yf_train)
    yf_test = clf.predict(Xf_test)

    X_train.loc[Xf_test.index, 'Age'] = yf_test

    return X_train, clf


def fill_ages_test(X_test, clf):

    Xf_test = X_test[X_test.Age == -1].drop('Age', 1, errors='ignore')
    yf_test = clf.predict(Xf_test)

    X_test.loc[Xf_test.index, 'Age'] = yf_test

    return X_test

