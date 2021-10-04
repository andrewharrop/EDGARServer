# Best to use a venv or something like conda here, especially on M1 chips


from math import nan
from re import A
from company import CompanyFrames
from tabulate import tabulate
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import warnings
# Determine the correlation between returns and all covariates

warnings.filterwarnings('ignore')


def logistic_performance(pred, actual, classes, v=0):
    tp = sum(np.logical_and(pred == classes[1], actual == classes[1]))
    tn = sum(np.logical_and(pred == classes[0], actual == classes[0]))
    fp = sum(np.logical_and(pred == classes[1], actual == classes[0]))
    fn = sum(np.logical_and(pred == classes[0], actual == classes[1]))
    nt = []
    if v == 1:
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
    vt = []
    if v == 1:
        vt.append(["Accuracy", round(accuracy, 3)])
        vt.append(["Precision", round(precision, 3)])
        vt.append(["Recall", round(recall, 3)])
        vt.append(["Sensitivity", round(sensitivity, 3)])
        vt.append(["Specificity", round(specificity, 3)])
        print(tabulate(vt, headers=["Type", "Value"]))
        print('\n')

    return tp, tn, fp, fn


class LinearRegressionSetup:
    def __init__(self, cik):
        self.company = CompanyFrames(cik, True)
        self.balance_sheet = self.company.balance_sheet
        self.income_statement = self.company.income_statement
        self.cash_flow = self.company.cash_flow
        self.price_data = self.company.fy_prices
        self.price_deltas = self.company.price_deltas
        self.valid_lreg_data = {}
        self.sk_cleaner(self.balance_sheet, self.valid_lreg_data)
        self.sk_cleaner(self.income_statement, self.valid_lreg_data)
        self.sk_cleaner(self.cash_flow, self.valid_lreg_data)
        self.regframe = self.sk_converter(self.valid_lreg_data)

    def sk_cleaner(self, sheet, agdict):
        k = sheet.keys()
        for key in k:
            entry = sheet[key]
            if isinstance(entry, dict):
                agdict[key] = entry

    def sk_converter(self, fsheet):
        yrange = {}
        yrange2 = {}

        keys = fsheet.keys()
        for entry in fsheet:
            for y in fsheet[entry]:
                if y not in yrange:
                    yrange[y] = {}
                    yrange2[y] = {}

                yrange[y][entry] = fsheet[entry][y]
        for y in yrange:
            yrange2[y]['price'] = self.price_data[str(y)]
            yrange2[y]['pricedelta'] = self.price_deltas[str(y)]

        df = pd.DataFrame(yrange)
        df = df.transpose()
        df2 = pd.DataFrame(yrange2)
        df2 = df2.transpose()
        return df, df2


class LinearRegression(LinearRegressionSetup):
    def __init__(self, cik):
        super().__init__(cik)
        self.regcov, self.regobs = self.regframe

        self.regcov = self.regcov.dropna(axis='columns')

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.regcov.values, self.regobs['pricedelta'].values, test_size=0.2, random_state=42)
        self.y_train_d = [1 if x > 0 else 0 for x in self.y_train]
        self.y_test_d = [1 if x > 0 else 0 for x in self.y_test]

    # v: verbosity -> {1,2}
    def binary_returns(self, v=0):
        BRreg = LogisticRegression()
        BRfit = BRreg.fit(self.X_train, self.y_train_d)
        BRcoef = BRfit.coef_[0]
        cname = list(self.regcov)
        print('\n')
        vt = []
        if v > 0:
            for c in range(len(cname)):
                if v == 1:
                    vt.append(
                        [cname[c], round(BRcoef[c]*(1/abs(np.average(BRcoef))), 3)])
                if v == 2:
                    vt.append(
                        [cname[c], BRcoef[c]])
            print(tabulate(vt, headers=['Covariate', 'Coefficient']))
        print('\n')
        BRpred = BRfit.predict(self.X_test)
        truePos, trueNeg, falsePos, falseNeg = logistic_performance(
            BRpred, self.y_test_d, BRfit.classes_, v)
        return truePos, trueNeg, falsePos, falseNeg
