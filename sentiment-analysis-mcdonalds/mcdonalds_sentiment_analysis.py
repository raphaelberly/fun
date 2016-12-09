"""
MCDONALD'S SENTIMENT ANALYSIS

This script performs a sentiment analysis using CountVectorizer and a Logistic Regression model.

The model is trained using data from files mcdonalds.csv

The objective of this script is to rank learn to rank comments from the database in order to get those which are the
most related to a complaint about rudeness of the service.

"""


import pandas as pd
import numpy as np

from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.base import clone


def prepare_data(path):
    """
    Reads raw data and removes lines with empty "policies_violated" feature
    :param path: path to the raw data file
    :return: pandas dataframe with "rude" target column, and "confidence_mean" column
    """
    raw = pd.read_csv(path).dropna(subset=['policies_violated'], how='any')
    raw['rude'] = raw.policies_violated.str.contains('RudeService').astype(int)
    raw['confidence_list'] = raw['policies_violated:confidence'].str.split('\n')
    raw['confidence_mean'] = raw.confidence_list.apply(lambda x: np.mean([float(i) for i in x]))
    return raw


def estimate_performance(vect, clf):
    """
    Given raw data, a vectorizer and a classifier, provides an estimate of the ROC AUC performance, through
    cross-validation
    :param raw: raw data to be used ()
    :param vect: vectorizer to be used
    :param clf: classifier to be used
    :return: estimate of the ROC AUC performance (mean of obtained ROC AUC scores)
    """
    raw = prepare_data('data/mcdonalds.csv')

    # prepare the learning datasets
    X = raw[raw.confidence_mean >= 0.75].review
    y = raw.rude[raw.confidence_mean >= 0.75]

    # prepare the pipeline
    pipe = make_pipeline(vect, clf)
    scores = cross_val_score(pipe, X, y, scoring='roc_auc', cv=5)

    # return the average over the 5 iterations
    return np.mean(scores)


def main(vect, clf):
    """
    Main function of the script. Prepares the data, trains the model, computes predictions and outputs them in a CSV
    file, and also assesses the model through cross-validation and provides with an estimate of its performance.
    :param vect: sklearn vectorizer to be used
    :param clf: sklearn classifier to be used
    :return: None
    """
    print('\nPreparing datasets...')
    raw = prepare_data('data/mcdonalds.csv')
    raw = raw[raw.confidence_mean >= 0.75]

    X_train, y_train = raw.review, raw.rude
    new_comments = pd.read_csv('data/mcdonalds_new.csv').review

    X_train_dtm = vect.fit_transform(X_train)
    new_comments_dtm = vect.transform(new_comments)

    print('Training model...')
    clf.fit(X_train_dtm, y_train)
    y_pred_proba = clf.predict_proba(new_comments_dtm)[:, 1]

    print('Computing predictions...')
    result = pd.DataFrame({'review': new_comments, 'prediction': y_pred_proba})
    result = result.sort_values('prediction', ascending=False)
    result.to_csv('data/output.csv', index=False)

    print('\nROC AUC estimate: {0:.4f}'.format(estimate_performance(clone(vect), clone(clf))))
    print('Predictions for new data saved in data/output.csv')


if __name__ == '__main__':

    # Run main file
    main(vect=CountVectorizer(max_df=0.3), clf=MNB())
