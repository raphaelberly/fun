"""
SMS SPAM-FILTERING WITH SCIKIT-LEARN

This project aims at implementing several methods for SPAM-filtering in Python, on a dataset containing SMS data. It
uses a dataset of 5,572 labelled SMS, and a Multinomial Naive Bayes model for classification.

More information about the research phase and the choices made can be found in the notebook Notebook.ipynb
"""


import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn import metrics


def import_data():
    """
    This function imports the raw data from its online source and creates two pandas series X and y containing the text
    observations and the target labels for learning
    :return: tuple (X, y) containing the text observations and the target labels for learning
    """
    url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv'
    data = pd.read_table(url, header=None, names=['label', 'message'])

    # convert label to a numerical variable
    data['target'] = data.label.map({'ham': 0, 'spam': 1})

    X = data.message
    y = data.target

    return X, y


def prepare_dtm(X_train, X_test):
    """
    Prepares document-term matrices (vectorizes text data) out of X_train and X_test
    :param X_train: pandas series containing train text observations
    :param X_test: pandas series containing test text observations
    :return: tuple (X_train_dtm, X_test_dtm, vect): the two document-term matrices created and the vectorizer object
    """
    vect = CountVectorizer(max_df=0.4, max_features=4000)
    vect.fit(X_train)
    X_train_dtm = vect.transform(X_train)
    X_test_dtm = vect.transform(X_test)

    return X_train_dtm, X_test_dtm, vect


def build_mnb_model(X_train_dtm, y_train):
    """
    Builds the Multinomial Naive Bayes model
    :param X_train_dtm: training document-term matrix
    :param y_train: training target labels
    :return: fitted Multinomial Naive Bayes model
    """
    mnb = MNB()
    mnb.fit(X_train_dtm, y_train)
    return mnb


def create_spamminess_dataframe(vectorizer, mnb):
    """
    Computes "spamminess" of each token and outputs a pandas dataframe containing this information
    :param vectorizer: fitted vectorizer object
    :param mnb: fitted MNB model (since it has the feature_count_ attribute, which will be used)
    :return: tokens: pandas dataframe with two features: "ham" and "spam", containing respectively the counts of each
    observation in ham and spam.
    """
    X_train_tokens = vectorizer.get_feature_names()

    ham_token_count = mnb.feature_count_[0, :]
    spam_token_count = mnb.feature_count_[1, :]

    tokens = pd.DataFrame({'token': X_train_tokens, 'ham': ham_token_count, 'spam': spam_token_count}).set_index('token')

    # convert the ham and spam counts into frequencies (to resolve the possible unbalance between classes)
    tokens['ham'] = (tokens.ham + 1) / mnb.class_count_[0]  # add one for avoiding future divisions by 0
    tokens['spam'] = (tokens.spam + 1) / mnb.class_count_[1]

    tokens['spam_ratio'] = tokens.spam / tokens.ham

    return tokens


def get_spam_ratio(word, tokens):
    """
    Gets the spam ratio (also calles "spamminess") of a particular word
    :param word: string, word to get the spam ratio of
    :param tokens: spamminess dataframe (output of create_spamminess_dataframe)
    :return: spam ratio of the chosen word
    """
    return tokens.loc[word, 'spam_ratio']


# Get the top ten spam words
def top_spam_tokens(tokens, nb):
    """
    Gets the list of the nb most spammy words
    :param tokens: spamminess dataframe (output of create_spamminess_dataframe)
    :param nb: number of items to put in the list
    :return: top ten spam words list
    """
    return list(tokens.sort_values('spam_ratio', ascending=False).head(nb).index)


# Get the top ten ham tokens
def top_ham_tokens(tokens, nb):
    """
    Gets the list of the nb most hammy words
    :param tokens: spamminess dataframe (output of create_spamminess_dataframe)
    :param nb: number of items to put in the list
    :return: top ten ham words list
    """
    return list(tokens.sort_values('spam_ratio', ascending=True).head(nb).index)


# MAIN FUNCTION OF THE SCRIPT

def main():
    """
    Main function of the script. Prepares the data, builds the model, applies it to the testing set, and prints some
    accuracy measures. Also provides the list of top ten spam and ham words.
    :return: None
    """
    print('\nPreparing data...')
    X, y = import_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
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


if __name__ == '__main__':

    # IF RUN AS A SCRIPT
    main()
