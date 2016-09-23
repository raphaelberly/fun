import pandas as pd
from classify_data import make_prediction
from prepare_data import get_datasets, prepare_train_set, prepare_test_set


def main():

    # PREPARING TRAIN DATA
    print('\nPreparing the train data...')

    raw_train = pd.read_csv('src/train.csv')
    X_train, y_train = get_datasets(raw_train, 'train')

    X_train, scaler_1, scaler_2, age_reg = prepare_train_set(X_train)

    # PREPARING TEST DATA
    print('Preparing the test data...')

    raw_test = pd.read_csv('src/test.csv')
    X_test = get_datasets(raw_test, 'test')

    X_test = prepare_test_set(X_test, scaler_1, scaler_2, age_reg)

    # MAKING PREDICTION
    print('Making the prediction...')

    y_pred = make_prediction(X_train, y_train, X_test).astype(int)
    y_pred.to_csv('src/prediction.csv', header=True)

    print('\nAll done.')


if __name__ == '__main__':

    main()
