
import pandas as pd

from sklearn.svm import SVC
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline, make_union

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Imputer


def prepare_dataset(raw):
    """
    Prepares X_train and X_test from the raw data (unused features dropping, categorical features dummifying, etc)
    :param raw: raw dataset (either raw_train or raw_train)
    :return: A new dataset with only the used columns, all at the right format and ready to use
    """
    X = pd.DataFrame.copy(raw)

    # Drop unused features
    X = X.drop(['Name', 'Ticket', 'Cabin'], axis=1).set_index('PassengerId')
    if 'Survived' in X.columns:
        X = X.drop('Survived', axis=1)

    # Fill missing Embarked with a new letter, "X"
    X['Embarked'] = X['Embarked'].fillna('X')

    # Create dummy columns
    aux = pd.get_dummies(X[['Embarked']])

    # Add dummy columns to X_train
    X = X.drop(['Embarked'], 1).join(aux)

    # Clean a bit
    if 'Embarked_X' in X.columns:
        X = X.drop(['Embarked_X'], 1)

    # Scale int variables to [-1, 1]
    X.Pclass = X.Pclass - 2
    X.Sex = X.Sex.apply(lambda x: 1 if x == 'male' else -1)
    X.Embarked_C = 2 * (X.Embarked_C - 0.5)
    X.Embarked_Q = 2 * (X.Embarked_Q - 0.5)
    X.Embarked_S = 2 * (X.Embarked_S - 0.5)

    return X


def get_scalable(array):
    """
    Function designed to be the basis of a sklearn transformer extracting scalable variables out of the dataset
    :param array: input array (since output of imputer is no longer a dataset but an array)
    :return: scalable columns of the array
    """
    return array[:, [2, 3, 4, 5]]


def get_unscalable(array):
    """
    Function designed to be the basis of a sklearn transformer extracting unscalable variables out of the dataset
    :param array: input array (since output of imputer is no longer a dataset but an array)
    :return: unscalable columns of the array
    """
    return array[:, [0, 1, 6, 7, 8]]


def prepare_pipeline():
    """
    Creation of the whole pipeline, used both in the training and prediction phase, for appropriate imputing, scaling,
    training and predicting.
    :return: sklearn pipeline
    """
    get_scalable_ft = FunctionTransformer(get_scalable, validate=False)
    get_unscalable_ft = FunctionTransformer(get_unscalable, validate=False)

    imputer = Imputer(strategy='mean', axis=0)
    scaler = StandardScaler()
    model = SVC()

    scaler_pipeline = make_pipeline(get_scalable_ft, scaler)
    scaler_union = make_union(scaler_pipeline, get_unscalable_ft)

    main_pipe = make_pipeline(imputer, scaler_union, model)

    return main_pipe
