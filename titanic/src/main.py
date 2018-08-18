import pandas as pd
from classification import make_prediction
from preparation import prepare_dataset, prepare_pipeline


def main():
    """
    Main file of the program. Prepares the data, the pipeline, and finally trains the model and predicts classes for
    the test data (stored in data/prediction.csv)
    :return: None
    """

    # PREPARING TRAIN DATA
    print('\nPreparing the train data...')
    raw_train = pd.read_csv('data/train.csv')
    X_train = prepare_dataset(raw_train)
    y_train = raw_train.Survived

    # PREPARING TEST DATA
    print('Preparing the test data...')
    raw_test = pd.read_csv('data/test.csv')
    X_test = prepare_dataset(raw_test)

    # PREPARING PIPELINE, TRAINING AND PREDICTING
    print('Preparing and training the model...')
    pipe = prepare_pipeline()
    output = make_prediction(pipe, X_train, y_train, X_test)
    output.to_csv('data/prediction.csv', index=False, header=True)

    print('\nAll done. File exported to data/prediction.csv')


if __name__ == '__main__':

    # Run main function
    main()
