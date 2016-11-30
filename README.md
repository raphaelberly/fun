# Kaggle Competitions

**Author:** [Raphael Berly](https://www.linkedin.com/in/raphaelberly), data scientist at [Erento](https://www.erento.com/info/jobs/).

### Overview

This repository gathers my work on several Kaggle competitions I participated to.

Hereby a list of the different competitions:

* [Titanic](#titanic)
* [Stack Overflow](#stack-overflow)


-----

### Titanic

This public kaggle competition, which is hosted [here](https://www.kaggle.com/c/titanic), aims at predicting the survival of passengers from Titanic. A dataset containing 891 observations and 10 features is provided for training.

A logistic regression was used for prediction, and of overall accuracy of 79.9% was reached with the submission on Kaggle (top 17%).

-----

### Stack Overflow

This private competition was hosted on Kaggle by [Data School](http://www.dataschool.io) as part of the **Machine Learning with Text in Python** eight-week training session.

The objective was to predict the status (Open or Close) of a post, based on its content and metadata.

The approach which was chosen was model stacking:

* Step 1: feature engineering to create new numerical features out of the data, and train a model on the most relevant ones
* Step 2: vectorize text data from the post, and train a model on the resulting document-term matrix
* Step 3: combine the predictions of both models to get an overall prediction

A log loss of 0.46369, giving me the 3rd position on this competition.
