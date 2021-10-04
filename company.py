from edgar import Company as EComp
import json

from xbrl_mapper import BalanceSheet
from xbrl_mapper import IncomeStatement
from xbrl_mapper import CashFlow

from yfin import YCompany

from ratios import Construct

from testing import CompanyTest


class Company(EComp):
    def __init__(self, cik, m=False):
        self.t = cik
        super().__init__(cik)
        self._facts = self.facts()
        self._gaap_facts = self._facts['facts']['us-gaap']

        self._balance_sheet = BalanceSheet(
            self._gaap_facts, m)
        self._income_statement = IncomeStatement(
            self._gaap_facts, m)
        self._cash_flow = CashFlow(
            self._gaap_facts, m)
        self.balance_sheet = self._balance_sheet.attrs()
        self.income_statement = self._income_statement.attrs()
        self.cash_flow = self._cash_flow.attrs()

    def market_data(self):
        c = YCompany(self.t)
        return c.price_history(), c.market_cap()

    def parser_quality(self):
        b = len(self.balance_sheet)
        i = len(self.income_statement)
        c = len(self.cash_flow)
        bsc = [self.balance_sheet[x] for x in self.balance_sheet].count(0)
        isc = [self.income_statement[x]
               for x in self.income_statement].count(0)
        cfc = [self.cash_flow[x] for x in self.cash_flow].count(0)
        return [(bsc + isc + cfc) / (b+i+c), bsc/b, isc/i, cfc/c]


# Algorithmic fitting
class CompanyFrames(Company):
    def __init__(self, cik, m=False):
        super().__init__(cik, m=m)
        self.hist, self.cap = self.market_data()
        self.fy_prices = self.fy_price_parser()
        self.price_deltas = self.deltas()

    def deltas(self):
        yoy_delta = {}
        s = int(min(self.fy_prices))
        for i in range(len(self.fy_prices)-1):
            delta = (self.fy_prices[str(s+1)] -
                     self.fy_prices[str(s)])/self.fy_prices[str(s)]
            s += 1
            yoy_delta[str(s)] = delta
        return yoy_delta

    def fy_price_parser(self):
        yrs = {}
        n = 1
        for _, row in self.hist.iterrows():
            avg = row['avg']
            yr = (str(row.name)[:4])
            if yr in yrs:
                n += 1
                yrs[yr] = ((yrs[yr]*(n-1))+avg)/n
            else:
                n = 1
                yrs[yr] = avg
        return yrs
