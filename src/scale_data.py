
# DATA SCALING


from sklearn.preprocessing import StandardScaler

def create_scaler_1(X):

    # This function creates a scaler X

    features_to_scale = X[['SibSp', 'Parch', 'Fare']]
    scaler = StandardScaler()
    scaler.fit(features_to_scale)

    return scaler

def create_scaler_2(X):

    scaler = StandardScaler()
    age = X.Age.reshape(-1, 1)
    scaler.fit(age)

    return scaler


def apply_scaler_1(scaler, X):

    # This function applies scaler to X

    X.Pclass = X.Pclass-2
    X.Sex = X.Sex.apply(lambda x: 1 if x == 'male' else -1)

    X.Embarked_C = 2*(X.Embarked_C-0.5)
    X.Embarked_Q = 2*(X.Embarked_Q-0.5)
    X.Embarked_S = 2*(X.Embarked_S-0.5)

    aux = ['SibSp', 'Parch', 'Fare']

    X[aux] = scaler.transform(X[aux])

    return X


def apply_scaler_2(scaler, X):

    age = X.Age.reshape(-1, 1)
    X.Age = scaler.transform(age)

    return X
