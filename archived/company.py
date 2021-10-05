from edgar import Company as EComp
import json

from xbrl_mapper import BalanceSheet
from xbrl_mapper import IncomeStatement
from xbrl_mapper import CashFlow

from yfin import YCompany

from ratios import Construct

#from testing import CompanyTest


class Company(EComp):
    def __init__(self, cik, m=False, term=0):
        self.t = cik
        super().__init__(cik)
        self._facts = self.facts()
        self._gaap_facts = self._facts['facts']['us-gaap']

        self._balance_sheet = BalanceSheet(
            self._gaap_facts, m, term)
        self._income_statement = IncomeStatement(
            self._gaap_facts, m, term)
        self._cash_flow = CashFlow(
            self._gaap_facts, m, term)

        self._y = YCompany(self.t)

        #self._test = CompanyTest(self)
        self.balance_sheet = self._balance_sheet.attrs()
        self.income_statement = self._income_statement.attrs()
        self.cash_flow = self._cash_flow.attrs()

    def market_data(self, width):
        c = YCompany(self.t)
        if width == 0:
            return c.price_history(), c.market_cap()
        elif width == 1:
            return c.tmo_price_history(), c.market_cap()

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
    def __init__(self, cik, m=False, w=0, term=0):
        super().__init__(cik, m=m, term=term)
        self.hist, self.cap = self.market_data(w)
        self.fy_prices = self.fx_price_parser(w)
        self.price_deltas = self.deltas(w)

    def deltas(self, w):
        if w == 0:
            yoy_delta = {}
            s = int(min(self.fy_prices))

            for i in range(len(self.fy_prices)-1):
                delta = (self.fy_prices[str(s+1)] -
                         self.fy_prices[str(s)])/self.fy_prices[str(s)]
                s += 1
                yoy_delta[str(s)] = delta
            return yoy_delta
        else:
            q_delta = {}
            s = (min(self.fy_prices))
            keys = list(self.fy_prices.keys())
            for i in range(len(self.fy_prices)-1):
                delta = (self.fy_prices[keys[i+1]] -
                         self.fy_prices[keys[i]])/self.fy_prices[keys[i]]
                s = self.fy_prices
                q_delta[keys[i]] = delta
            return q_delta

    def fx_price_parser(self, w):
        if w == 0:
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
        elif w == 1:
            mos = {}
            n = 1
            for _, row in self.hist.iterrows():
                avg = row['avg']

                mo = (str(row.name)[5:7])
                q = 0
                if mo in ['01', '02', '03']:
                    q = 1
                elif mo in ['04', '05', '06']:
                    q = 2
                elif mo in ['07', '08', '09']:
                    q = 3
                elif mo in ['10', '11', '12']:
                    q = 4
                v = (str(row.name)[:4]) + f"q{q}"

                mos[v] = avg
            return mos


#test = CompanyFrames('aapl', w=1)
