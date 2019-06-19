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
from sklearn.ensemble import RandomForestClassifier


def ml_output(id):  # Using machine learning to predict status
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


def ml_machine_size(input: tuple):
    order = pd.read_csv("D:\\summer_python\\order.csv")
    order = order[["in_prod_name", "d_size", "l_size", "mac_cd1", "mac_cd2"]]

    l = list(order["l_size"].astype(int))
    d = list(order["d_size"])
    mac1 = list(order["mac_cd1"].fillna("0"))
    mac2 = list(order["mac_cd2"].fillna("0"))

    x_train = []
    for i in range(0, len(l)):
        x_train.append((l[i], d[i]))
    mac1_low = ["N00069", "N00106", "N00107", "N00138", "T00050", "T00054"]
    mac1_medium = [
        "N00007",
        "N00008",
        "N00015",
        "N00023",
        "N00024",
        "N00052",
        "N00054",
        "N00084",
        "N00085",
        "N00086",
        "N00087",
        "N00110",
        "N00111"]
    mac1_high = [
        "N00040",
        "N00041",
        "N00056",
        "N00070",
        "N00108",
        "N00109",
        "N00146"]
    mac2_low = ["T00010", "T00041", "T00176"]
    mac2_medium = ["N00090", "T00006", "T00008", "T00037", "T00038", "T00127"]
    mac2_high = ["T00009", "T00033", "T00039", "T00199", "T00200"]

    x1_new, x2_new, mac1_new, mac2_new = [], [], [], []  # Machine learning training set
    for i in range(0, len(x_train)):
        if mac1[i] in mac1_low:
            x1_new.append(x_train[i])
            mac1_new.append("1")
        elif mac1[i] in mac1_medium:
            x1_new.append(x_train[i])
            mac1_new.append("2")
        elif mac1[i] in mac1_high:
            x1_new.append(x_train[i])
            mac1_new.append("3")
        elif mac1[i] == "0":
            x1_new.append(x_train[i])
            mac1_new.append("0")
        else:
            continue
        if mac2[i] in mac2_low:
            x2_new.append(x_train[i])
            mac2_new.append("1")
        elif mac2[i] in mac2_medium:
            x2_new.append(x_train[i])
            mac2_new.append("2")
        elif mac2[i] in mac2_high:
            x2_new.append(x_train[i])
            mac2_new.append("3")
        elif mac2[i] == "0":
            x2_new.append(x_train[i])
            mac2_new.append("0")
        else:
            continue

    method = RandomForestClassifier()
    method_cd1 = method.fit(x1_new, mac1_new)
    method_cd2 = method.fit(x2_new, mac2_new)
    cd1 = method_cd1.predict([input])
    cd2 = method_cd2.predict([input])
    return [cd1, cd2]
