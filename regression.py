from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from tabulate import tabulate
import numpy as np

import warnings


class Regression:
    def __init__(self, X, y, test_size=0.2, random_state=1):
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.prediction = None

        self.split_data()

    def split_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state)

    def linear_regression(self):
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)
        self.prediction = self.model.predict(self.X_test)

    def logistic_regression(self,):
        self.model = LogisticRegression()
        self.y_train = [1 if x > 0 else 0 for x in self.y_train]
        self.y_test = [1 if x > 0 else 0 for x in self.y_test]

        self.model.fit(self.X_train, self.y_train)
        self.prediction = self.model.predict(self.X_test)

    def logistic_performance(self, pred, actual, classes, verbose=0):
        warnings.filterwarnings('ignore')

        tp = sum(np.logical_and(pred == classes[1], actual == classes[1]))
        tn = sum(np.logical_and(pred == classes[0], actual == classes[0]))
        fp = sum(np.logical_and(pred == classes[1], actual == classes[0]))
        fn = sum(np.logical_and(pred == classes[0], actual == classes[1]))
        nt = []
        if verbose == 1:
            nt.append(["True Positives", tp])
            nt.append(["True Negatives", tn])
            nt.append(["False Positives", fp])
            nt.append(["False Negatives", fn])
            print(tabulate(nt, headers=["Type", "Count"]))
            print('\n')
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        sensitivity = recall
        specificity = tn / (tn + fp)
        if verbose == 1:
            nt.append(["-------", "-------"])
            nt.append(["Accuracy", round(accuracy, 3)])
            nt.append(["Precision", round(precision, 3)])
            nt.append(["Recall", round(recall, 3)])
            nt.append(["Sensitivity", round(sensitivity, 3)])
            nt.append(["Specificity", round(specificity, 3)])
            print('\n')
            print(tabulate(nt, headers=["Type", "Count"]))
            print('\n')

        return tp, tn, fp, fn
