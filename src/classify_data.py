
# CLASSIFICATION OF DATA

from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.cross_validation import cross_val_score

import pandas as pd
import numpy as np

def make_prediction(X_train, y_train, X_test):

    score = cross_val_score(SVC(), X_train, y_train)
    print('Estimated precision: ', np.mean(score))

    clf = SVC()
    clf.fit(X_train, y_train)

    y_pred = pd.DataFrame({'Survived': clf.predict(X_test)}, index=X_test.index)

    return y_pred

