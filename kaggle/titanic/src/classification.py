
# CLASSIFICATION OF DATA

import pandas as pd
from scipy import stats
from sklearn.grid_search import RandomizedSearchCV


def make_prediction(pipe, X_train, y_train, X_test):
    """
    Assesses the model with n_iter different sets of parameters through cross-validation, choose the best one, train
    it on the train data and predicts on the test data.
    :param pipe: main pipeline, output of prepare_pipeline()
    :param X_train: training dataset, output of prepare_dataset(raw_train)
    :param y_train: target column of the training set
    :param X_test: testing dataset, output of prepare_dataset(raw_test)
    :return: pandas dataframe with two features: PassengerId and Survived (prediction for the test set)
    """
    param_grid = {'svc__C': stats.uniform(loc=0, scale=10),
                  'svc__decision_function_shape': [None, 'ovo', 'ovr'],
                  'svc__shrinking': [True, False]
                  }
    rand = RandomizedSearchCV(pipe, param_grid, cv=5, scoring='accuracy', n_iter=100)

    # We fit to the train sets
    rand.fit(X_train, y_train)
    print('Estimated accuracy: {:.1f} %'.format(rand.best_score_*100))

    output = pd.DataFrame({'PassengerId': X_test.index, 'Survived': rand.predict(X_test)})

    return output
