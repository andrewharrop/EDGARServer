# collect the data | Some messy methods

from yfin import YCompany
from edgar import Company
from edgar_parser import Parser
import pandas as pd


class FinancialData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.yfin = YCompany(ticker)
        self.edgar = Company(ticker)
        self.edgar_facts_meta = self.edgar.facts()
        self.edgar_facts = self.edgar_facts_meta['facts']
        self.yfin_annual = self.yfin.price_history(term='y')
        self.yfin_quarter = self.yfin.price_history(term='q')

        # Adjust the price data to match edgar
        self.adj_quarterly_frame = self.quarter_numerical_convert(
            self.yfin_quarter)
        self.adj_annual_frame = self.annual_numerical_convert(self.yfin_annual)

        # Grab the financial statements
        self.quarterly_balance_sheet, self.quarterly_income_statement, self.quarterly_cash_flow = self.periodicals(
            'quarterly')
        self.annual_balance_sheet, self.annual_income_statement, self.annual_cash_flow = self.periodicals(
            'annual')

        # Convert quarterlies into central frames
        self.quarterly_balance_sheet_frame = self.edgar_frame(
            self.quarterly_balance_sheet, self.adj_quarterly_frame)
        self.quarterly_income_statement_frame = self.edgar_frame(
            self.quarterly_income_statement, self.adj_quarterly_frame)
        self.quarterly_cash_flow_frame = self.edgar_frame(
            self.quarterly_cash_flow, self.adj_quarterly_frame)

        # Convert annuals into central frames
        self.annual_balance_sheet_frame = self.edgar_frame(
            self.annual_balance_sheet, self.adj_annual_frame)
        self.annual_income_statement_frame = self.edgar_frame(
            self.annual_income_statement, self.adj_annual_frame)
        self.annual_cash_flow_frame = self.edgar_frame(
            self.annual_cash_flow, self.adj_annual_frame)

        # Merge the frames
        self.quarterly_merge = pd.merge(
            self.quarterly_balance_sheet_frame, self.quarterly_income_statement_frame, on='date')
        self.quarterly_merge = pd.merge(
            self.quarterly_merge, self.quarterly_cash_flow_frame, on='date')

        self.annual_merge = pd.merge(
            self.annual_balance_sheet_frame, self.annual_income_statement_frame, on='date')
        self.annual_merge = pd.merge(
            self.annual_merge, self.annual_cash_flow_frame, on='date')

    def periodicals(self, period):
        self.parser = Parser(self.edgar_facts)
        return self.parser.periodical(period)

    def edgar_frame(self, statement, prices):
        frame = pd.DataFrame(statement).dropna(axis=1)
        frame['date'] = frame.index
        return pd.merge(frame, prices, on='date').set_index('date')

    def quarter_numerical_convert(self, frame):
        new_frame = []
        for index, row in frame.iterrows():
            i = str(index)
            year = i[:4]
            month = i[5:7]
            if month in ['01', '02', '03']:
                quarter = 'Q1'
            elif month in ['04', '05', '06']:
                quarter = 'Q2'
            elif month in ['07', '08', '09']:
                quarter = 'Q3'
            elif month in ['10', '11', '12']:
                quarter = 'Q4'
            new_frame.append([year+quarter, row['avg']])
        return pd.DataFrame(new_frame, columns=['date', 'avg'])

    def annual_numerical_convert(self, frame):
        new_frame = []
        for index, row in frame.iterrows():
            new_frame.append([int(str(index)[:4]), row['avg']])
        return pd.DataFrame(new_frame, columns=['date', 'avg'])


# test = FinancialData('aapl')
# print(test.periodicals('quarterly'))
# print(test.periodicals('annual'))
