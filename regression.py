# Best to use a venv or something like conda here, especially on M1 chips


from company import CompanyFrames

import numpy as np
from sklearn import linear_model
import pandas as pd
# Determine the correlation between returns and all covariates


class LinearRegressionFit:
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
        self.sk_converter(self.valid_lreg_data)

    def sk_cleaner(self, sheet, agdict):
        k = sheet.keys()
        for key in k:
            entry = sheet[key]
            if isinstance(entry, dict):
                agdict[key] = entry

    def sk_converter(self, fsheet):
        yrange = {}
        keys = fsheet.keys()
        for entry in fsheet:
            for y in fsheet[entry]:
                if y not in yrange:
                    yrange[y] = {}
                yrange[y][entry] = fsheet[entry][y]

        df = pd.DataFrame(yrange)
        df = df.transpose()
        df.to_csv('test.csv')


a = LinearRegressionFit('tsla')
