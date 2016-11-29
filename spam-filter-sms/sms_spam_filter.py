# SMS SPAM-FILTERING WITH SCIKIT-LEARN
#
#
# This script is a simple spam-filter using CountVectorizer and a Multinomial Naive Bayes model.
#
# The model is trained using a SMS database posted by Kevin Markham (Data School, founder) at the following link:
# https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv
#

import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn import metrics


# Import the data and output X and y

def import_data():

    url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv'
    data = pd.read_table(url, header=None, names=['label', 'message'])

    # convert label to a numerical variable
    data['label_num'] = data.label.map({'ham': 0, 'spam': 1})

    X = data.message
    y = data.label_num

    return X,y


# Prepare document-term matrices (vectorize text data)

def prepare_dtm(X_train, X_test):

    vect = CountVectorizer()
    vect.fit(X_train)
    X_train_dtm = vect.transform(X_train)
    X_test_dtm = vect.transform(X_test)

    return X_train_dtm, X_test_dtm, vect


# Build the Multinomial Naive Bayes model

def build_mnb_model(X_train_dtm, y_train):
    mnb = MNB()
    mnb.fit(X_train_dtm, y_train)
    return mnb


# Computing "spamminess" of each token

def create_spamminess_dataframe(vectorizer, mnb):

    X_train_tokens = vectorizer.get_feature_names()

    ham_token_count = mnb.feature_count_[0, :]
    spam_token_count = mnb.feature_count_[1, :]

    tokens = pd.DataFrame({'token':X_train_tokens, 'ham':ham_token_count, 'spam':spam_token_count}).set_index('token')

    # convert the ham and spam counts into frequencies (to resolve the possible unbalance between classes)
    tokens['ham'] = (tokens.ham + 1) / mnb.class_count_[0]  # add one for avoiding future divisions by 0
    tokens['spam'] = (tokens.spam + 1) / mnb.class_count_[1]

    tokens['spam_ratio'] = tokens.spam / tokens.ham

    return tokens


# Get the spam ratio of a particular word

def get_spam_ratio(word, tokens):

    return tokens.loc[word, 'spam_ratio']


# Get the top ten spam words
def top_spam_tokens(tokens, nb):
    return list(tokens.sort_values('spam_ratio', ascending=False).head(nb).index)


# Get the top ten ham tokens
def top_ham_tokens(tokens, nb):
    return list(tokens.sort_values('spam_ratio', ascending=True).head(nb).index)


# MAIN FUNCTION OF THE SCRIPT

def main():

    print('\nPreparing data...')
    X, y = import_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    X_train_dtm, X_test_dtm, vectorizer = prepare_dtm(X_train, X_test)

    print('Building model...')
    mnb = build_mnb_model(X_train_dtm, y_train)

    print('\nResults:')
    y_pred = mnb.predict(X_test_dtm)
    y_pred_prob = mnb.predict_proba(X_test_dtm)[:, 1]
    print('Overall Accuracy: {0:.2f} %'.format(metrics.accuracy_score(y_test, y_pred)*100))
    print('Area Under Curve: {0:.4f}'.format(metrics.roc_auc_score(y_test, y_pred_prob)))
    print('Confusion matrix:\n{}'.format(metrics.confusion_matrix(y_test, y_pred)))

    tokens = create_spamminess_dataframe(vectorizer, mnb)

    print('\nTop 10 spam words', top_spam_tokens(tokens, 10))
    print('Top 10 ham words', top_ham_tokens(tokens, 10))


# IF RUN AS A SCRIPT

if __name__ == '__main__':

    main()
