### machine learning part

import pandas as pd
import numpy as np
import os
import data_processing_functions
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree


def Bayes_classifier(x_train, y_train, x_test) -> str:
    mnb = MultinomialNB(alpha=1.0e-10)
    mnb.fit(x_train, y_train)
    return mnb.predict(x_test)


def ml_on_status(id) -> str:  # Using Multinomial Naive Bayes to predict status
    status = pd.read_csv('.\\data.csv')
    x = status["in_prod_name"]
    y_main = status["category"]
    y_3 = status["3"]
    y_5 = status["5"]
    y_12 = status["12"]

    output = ""
    vec = CountVectorizer()
    x_train = vec.fit_transform(x)  # Transforming the input as word vector

    y_train = y_main
    # Using mutinomial naive bayes, alpha is Laplace smoothing parameter
    mnb = MultinomialNB(alpha=1.0e-10)
    mnb.fit(x_train, y_train)  # Training model
    # 7 states represent 7 different main status sequence
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

    if Bayes_classifier(x_train, y_3, vec.transform([id])) == 1:
        output += "3-4-"
    if Bayes_classifier(x_train, y_5, vec.transform([id])) == 1:
        output += "5-6-"
    if Bayes_classifier(x_train, y_12, vec.transform([id])) == 1:
        output += "12-13-"

    return output


def ml_on_machine_size(input: tuple):   # Using decision tree to predict specific machine
    order = pd.read_csv(".\\order.csv")
    order = order[["in_prod_name", "d_size", "l_size", "mac_cd1", "mac_cd2"]]

    l = list(order["l_size"].astype(int))  # l_size
    d = list(order["d_size"])  # d_size
    mac1 = list(order["mac_cd1"].fillna("0"))  # making NaN into category "0"
    mac2 = list(order["mac_cd2"].fillna("0"))

    x_train = []
    for i in range(0, len(l)):
        x_train.append((l[i], d[i]))

    machine_dictionary = data_processing_functions.txt_to_dictionary(
        "machine_type_dic")

    x1_new, x2_new, mac1_new, mac2_new = [], [], [], []  # Machine learning training set
    for i in range(0, len(x_train)):  # pre-processing training set
        x1_new.append(x_train[i])
        if mac1[i] in machine_dictionary["mac1_low"]:
            mac1_new.append("1")
        elif mac1[i] in machine_dictionary["mac1_medium"]:
            mac1_new.append("2")
        elif mac1[i] in machine_dictionary["mac1_high"]:
            mac1_new.append("3")
        elif mac1[i] == "0":
            mac1_new.append("0")
        else:
            x1_new.pop()
            continue
        x2_new.append(x_train[i])
        if mac2[i] in machine_dictionary["mac2_low"]:
            mac2_new.append("1")
        elif mac2[i] in machine_dictionary["mac2_medium"]:
            mac2_new.append("2")
        elif mac2[i] in machine_dictionary["mac2_high"]:
            mac2_new.append("3")
        elif mac2[i] == "0":
            mac2_new.append("0")
        else:
            x2_new.pop()
            continue

    #method = RandomForestClassifier()    ###   Random forest algorithm also performs well in this problem
    method = tree.DecisionTreeClassifier(criterion = "entropy",max_depth = 100, splitter ="random")
    method_cd1 = method.fit(x1_new, mac1_new)
    method_cd2 = method.fit(x2_new, mac2_new)
    cd1 = method_cd1.predict([input])
    cd2 = method_cd2.predict([input])
    return [cd1, cd2] ### cd1 and cd2 are columns "AF" and "AG" in order table 
