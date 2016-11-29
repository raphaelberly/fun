## Natural Language Processing in Python

**Author:** [Raphael Berly](https://www.linkedin.com/in/raphaelberly), data scientist at [Erento](https://www.erento.com/info/jobs/).

### Overview

This repository gathers some python NLP projects, on several different examples.

Hereby a list of the scripts implemented:

* [Spam Filter: SMS](#spam-filter-sms)
* [Sentiment Analysis: McDonald's](#sentiment-analysis-mcdonalds)

-----

### SPAM Filter: SMS

This project aims at implementing several methods for SPAM-filtering in Python, on a dataset containing SMS data. It is developed in the script *sms_spam_filter.py*

It uses a [dataset](https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv) of 5,572 labelled SMS, and a Multinomial Naive Bayes model for classification.

An overall accuracy of around 99% is reached, with a false positive rate of around 0.4%.

Methods for getting the "top ten spam/ham words" involved in the Naive Bayes prediction process are also included in this script.


-----

### Sentiment Analysis: McDonald's

This project aims at implementing a Sentiment Analysis in Python, on a dataset containing McDonald's reviews. It is developed in the file *mcdonalds-sentiment-analysis.py*

It uses the dataset *data/mcdonalds.csv* of 1,525 labelled McDonald's reviews in the US. Those reviews were posted on the website and labelled manually. For each review, there is a list of keywords detailing the type of the complaint (BadFood, ScaryMcDs, Cost, Filthy, MissingFood, OrderProblem, RudeService, SlowService, na).

**The objective of this project is to provide the likelihood that a complaint is referring to rude service.** McDonald's could then use this project to build a "rudeness dashboard" for their staff, so that employees can spend a few minutes each day examining the most relevant recent comments.

The method implemented here uses a Multinomial Naive Bayes model for classification. An AUC (Area Under Curve) of over 78% is reached (cross-validation score).

The file *data/mcdonalds_new.csv* contains 10 other reviews, on which the user can test the trained model. A method is provided for that matter.