
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

    def logistic_regression(self, verbose=1):
        covariate = (self.quarterly_merged_df.drop('avg', 1)).values
        response = (self.quarterly_merged_df['avg']).values

        regression = Regression(covariate, response)
        regression.logistic_regression()
        actual = regression.y_test
        predicted = regression.prediction
        classes = regression.model.classes_
        tp, tn, fp, fn = regression.logistic_performance(
            actual, predicted, classes, verbose=verbose)

        return tp, tn, fp, fn


def logistic_regression_series(series, v=0):

    total_tp = 0
    total_tn = 0
    total_fp = 0
    total_fn = 0

    for ticker in series:

        company = Company(ticker)
        tp, tn, fp, fn = company.logistic_regression(0)

        total_tp += tp
        total_tn += tn
        total_fp += fp
        total_fn += fn

    print('Total TP:', total_tp)
    print('Total TN:', total_tn)
    print('Total FP:', total_fp)
    print('Total FN:', total_fn)


# tickers = ['aapl', 'amzn', 'f', 'tsla', 'aapl']
# logistic_regression_series(tickers)
