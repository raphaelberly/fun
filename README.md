## Sentiment Analysis in Python

**Author:** [Raphael Berly](https://www.linkedin.com/in/raphaelberly), data scientist at [Erento](https://www.erento.com/info/jobs/).

### Overview

This project aims at implementing several methods for sentiment analysis in Python, on different examples.

Hereby a list of the different scripts implemented:

* [McDonald's Sentiment Analysis: Multinomial Naive Bayes](#mcdonald-s-sentiment-analysis-multinomial-naive-bayes)

-----

### McDonald's Sentiment Analysis: Multinomial Naive Bayes

This part is developed in the file *mcdonalds-sentiment-analysis.py*

It uses the dataset *data/mcdonalds.csv* of 1,525 labelled McDonald's reviews in the US. Those reviews were posted on the website and labelled manually. For each review, there is a list of keywords detailing the type of the complaint (BadFood, ScaryMcDs, Cost, Filthy, MissingFood, OrderProblem, RudeService, SlowService, na).

**The objective of this project is to provide the likelihood that a complaint is referring to rude service.** McDonald's could then use this project to build a "rudeness dashboard" for their staff, so that employees can spend a few minutes each day examining the most relevant recent comments.

The method used here was presented by [Data School](http://www.dataschool.io/), in the Master Course "Machine Learning with text".  It uses a Multinomial Naive Bayes model for classification.

An AUC (Area Under Curve) of over 78% is reached (cross-validation score).

The file *data/mcdonalds_new.csv* contains 10 other reviews, on which the user can test the trained model. A method is provided for that matter.