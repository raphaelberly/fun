import pandas as pd
from classify_data import make_prediction
from prepare_data import get_train_datasets, get_test_datasets, dummify, fill_ages_train, fill_ages_test

from src.scale_data import create_scaler_1, apply_scaler_1, create_scaler_2, apply_scaler_2


def training_set(X_train):

    X_train = dummify(X_train)

    scaler_1 = create_scaler_1(X_train)
    X_train = apply_scaler_1(scaler_1, X_train)

    X_train, age_reg = fill_ages_train(X_train)

    scaler_2 = create_scaler_2(X_train)
    X_train = apply_scaler_2(scaler_2, X_train)

    return X_train, scaler_1, scaler_2, age_reg


def test_set(X_test, scaler_1, scaler_2, reg):

    X_test = dummify(X_test)
    X_test = apply_scaler_1(scaler_1, X_test)
    X_test = fill_ages_test(X_test, reg)
    X_test = apply_scaler_2(scaler_2, X_test)

    return X_test


# IF SCRIPT IS RUN:

if __name__ == '__main__':

    # PREPARING TRAIN DATA
    print('\nPreparing the train data...')

    raw_train = pd.read_csv('src/train.csv')
    X_train, y_train = get_train_datasets(raw_train)

    X_train, scaler_1, scaler_2, age_reg = training_set(X_train)

    # PREPARING TEST DATA
    print('Preparing the test data...')

    raw_test = pd.read_csv('src/test.csv')
    X_test = get_test_datasets(raw_test)

    X_test = test_set(X_test, scaler_1, scaler_2, age_reg)

    # MAKING PREDICTION
    print('Making the prediction...')

    y_pred = make_prediction(X_train, y_train, X_test).astype(int)
    y_pred.to_csv('src/prediction.csv', header=True)

    print('\nAll done.')
