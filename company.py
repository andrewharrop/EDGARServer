
from data_mapper import FinancialData
from regression import Regression


class Company(FinancialData):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.ticker = ticker

        self.annual_bs = self.annual_balance_sheet
        self.annual_is = self.annual_income_statement
        self.annual_cf = self.annual_cash_flow

        self.annual_bs_df = self.annual_balance_sheet_frame
        self.annual_is_df = self.annual_income_statement_frame
        self.annual_cf_df = self.annual_cash_flow_frame

        self.quarterly_bs = self.quarterly_balance_sheet
        self.quarterly_is = self.quarterly_income_statement
        self.quarterly_cf = self.quarterly_cash_flow

        self.quarterly_bs_df = self.quarterly_balance_sheet_frame
        self.quarterly_is_df = self.quarterly_income_statement_frame
        self.quarterly_cf_df = self.quarterly_cash_flow_frame

        self.quarterly_merged_df = self.quarterly_merge
        self.annual_merged_df = self.annual_merge

    def logistic_regression(self):
        covariate = (self.quarterly_merged_df.drop('avg', 1)).values
        response = (self.quarterly_merged_df['avg']).values

        regression = Regression(covariate, response)
        regression.logistic_regression()
        actual = regression.y_test
        predicted = regression.prediction
        classes = regression.model.classes_
        regression.logistic_performance(actual, predicted, classes)


test = Company('aapl')
test.logistic_regression()
