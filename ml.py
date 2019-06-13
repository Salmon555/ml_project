import pandas as pd
import numpy as np
import re
import os
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report


def ml_output(id):  #Using machine learning to predict status
    status = pd.read_csv('.\\data.csv')
    x = status["in_prod_name"]
    y_main = status["category"]
    y_3 = status["3"]
    y_5 = status["5"]
    y_12 = status["12"]

    output = ""
    vec = CountVectorizer()
    x_train = vec.fit_transform(x)  #Transforming the input as word vector

    y_train = y_main
    mnb = MultinomialNB(alpha=1.0e-10)   #Using mutinomial naive bayes, alpha is Laplace smoothing parameter
    mnb.fit(x_train, y_train) #Training model
    state = mnb.predict(vec.transform([id]))
    if state == 0:
        output = output
    elif state == 1:
        output += "200-201-"
    elif state == 2:
        output += "202-203-"
    elif state == 3:
        output += "200-201-202-203-"
    elif state == 4:
        output += "204-205-"
    elif state == 5:
        output += "200-201-204-205-"
    elif state == 6:
        output += "202-203-204-205-"

    y_train = y_3
    mnb.fit(x_train, y_train)
    state = mnb.predict(vec.transform([id]))
    if state == 1:
        output += "3-4-"

    y_train = y_5
    mnb.fit(x_train, y_train)
    state = mnb.predict(vec.transform([id]))
    if state == 1:
        output += "5-6-"

    y_train = y_12
    mnb.fit(x_train, y_train)
    state = mnb.predict(vec.transform([id]))
    if state == 1:
        output += "12-13-"
    return output
