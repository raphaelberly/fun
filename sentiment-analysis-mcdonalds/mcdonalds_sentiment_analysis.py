# MCDONALD'S SENTIMENT ANALYSIS USING
#
#
# This script performs a sentiment analysis using CountVectorizer and a Multinomial Naive Bayes model.
#
# The model is trained using data from files mcdonalds.csv
#
# The objective of this script is to rank learn to rank comments from the database in order to get those which are the
# most related to a complaint about rudeness of the service.
#

import pandas as pd
import numpy as np

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn import metrics
from sklearn.base import clone


def prepare_train_data(path):

    # read raw data and remove lines with empty "policies_violated" feature
    raw = pd.read_csv(path).dropna(subset=['policies_violated'], how='any')
    raw['rude'] = raw.policies_violated.str.contains('RudeService').astype(int)
    raw['confidence_list'] = raw['policies_violated:confidence'].str.split('\n')
    raw['confidence_mean'] = raw.confidence_list.apply(lambda x: np.mean([float(i) for i in x]))
    return raw


def estimate_performance(vect, clf):

    raw = prepare_train_data('data/mcdonalds.csv')

    # prepare the cross-validation datasets
    X_train, X_test, y_train, y_test = train_test_split(raw, raw.rude, random_state=1)

    y_train = y_train[X_train.confidence_mean >= 0.75]
    X_train = X_train[X_train.confidence_mean >= 0.75].review
    X_test = X_test.review

    # prepare the document-term matrices
    X_train_dtm = vect.fit_transform(X_train)
    X_test_dtm = vect.transform(X_test)

    # fit and predict
    clf.fit(X_train_dtm, y_train)
    y_pred_proba = clf.predict_proba(X_test_dtm)[:, 1]

    # compute the ROC AUC to assess performance
    return metrics.roc_auc_score(y_test, y_pred_proba)


# MAIN FUNCTION OF THE SCRIPT

def main(vect, clf):

    print('\nPreparing datasets...')
    raw = prepare_train_data('data/mcdonalds.csv')
    raw = raw[raw.confidence_mean >= 0.75]

    X_train, y_train = raw.review, raw.rude
    new_comments = pd.read_csv('data/mcdonalds_new.csv').review

    X_train_dtm = vect.fit_transform(X_train)
    new_comments_dtm = vect.transform(new_comments)

    print('Training model...')
    clf.fit(X_train_dtm, y_train)
    y_pred_proba = clf.predict_proba(new_comments_dtm)[:, 1]

    print('Computing predictions...')
    result = pd.DataFrame({'review': new_comments, 'prediction': y_pred_proba}).sort_values('prediction', ascending=False)
    pd.set_option('display.max_colwidth', 100)
    result.to_csv('data/output.csv', index=False)

    print('\nROC AUC estimation: {0:.4f}'.format(estimate_performance(clone(vect), clone(clf))))

    print('\nAll done. Predictions saved in data/output.csv')


# IF RUN AS A SCRIPT

if __name__ == '__main__':

    main(vect=CountVectorizer(max_df=0.3), clf=MNB())
