import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

from titanic.src.scale_data import create_scaler_1, apply_scaler_1, create_scaler_2, apply_scaler_2


def dummify(X):

    """
    This function dummifies the 'Embarked' feature of a dataset
    :param X: dataset
    :return: same dataset 'Embarked' column dummified
    """

    return X.drop(['Embarked'], 1).join(pd.get_dummies(X[['Embarked']]))


def get_datasets(raw_data, set):

    """
    This function prepares the data for the next step of the data pre-processing.
    :param raw_data: the raw data from the CSV file
    :param set: 'test' or 'train' (i.e. is there a 'Survived' feature?)
    :return: the dataset without unused features, with pre-filled missing values (will be adjusted later)
    """

    # Drop unused features
    raw_data = raw_data.drop(['Name', 'Ticket', 'Cabin'], axis=1).set_index('PassengerId')

    # Fill missing values
    raw_data['Age'] = raw_data['Age'].fillna(-1)  # Temporary filled value
    raw_data['Embarked'] = raw_data['Embarked'].fillna(raw_data['Embarked'].value_counts().index[0])
    raw_data['Fare'] = raw_data['Fare'].fillna(np.mean(raw_data.Fare))


    if set == 'train':
        X_train = dummify(raw_data.drop('Survived', axis=1))
        y_train = raw_data['Survived']
        return X_train, y_train

    if set == 'test':
        return dummify(raw_data)


def fill_ages_train(X_train):

    """
    This function fills the missing values from the 'Age' feature of the training set. The missing values are those
    with the value -1. A KNN regression is used to fill these missing ages.
    :param X_train: train dataset
    :return X_train: train dataset with missing ages filled
    :return reg: KNN-regressor used to compute them
    """

    Xf_train_raw = X_train[X_train.Age >= 0]
    yf_train = Xf_train_raw['Age']
    Xf_train = Xf_train_raw.drop('Age', 1, errors='ignore')

    Xf_test = X_train[X_train.Age == -1].drop('Age', 1, errors='ignore')

    reg = KNeighborsRegressor()
    reg.fit(Xf_train, yf_train)
    yf_test = reg.predict(Xf_test)

    X_train.loc[Xf_test.index, 'Age'] = yf_test

    return X_train, reg


def fill_ages_test(X_test, reg):

    """
    This function fills the missing values from the 'Age' feature of the testing set. The missing values are those
    with the value -1. The regressor created on the training phase is used to fill these missing ages.
    :param X_test: test dataset
    :param reg: regressor created on the training phase
    :return X_test: test dataset with missing ages filled
    """

    Xf_test = X_test[X_test.Age == -1].drop('Age', 1, errors='ignore')
    yf_test = reg.predict(Xf_test)

    X_test.loc[Xf_test.index, 'Age'] = yf_test

    return X_test


def prepare_train_set(X_train):

    scaler_1 = create_scaler_1(X_train)
    X_train = apply_scaler_1(scaler_1, X_train)

    X_train, age_reg = fill_ages_train(X_train)

    scaler_2 = create_scaler_2(X_train)
    X_train = apply_scaler_2(scaler_2, X_train)

    return X_train, scaler_1, scaler_2, age_reg


def prepare_test_set(X_test, scaler_1, scaler_2, reg):

    X_test = apply_scaler_1(scaler_1, X_test)
    X_test = fill_ages_test(X_test, reg)
    X_test = apply_scaler_2(scaler_2, X_test)

    return X_test
