# This file is neccesary to standardize the XBRL format. Because the nature of XBRL changes, this is very dynamic
# https://raw.githubusercontent.com/rdaher/PySec/master/pysec/xbrl_fundamentals.py
# Class Manager
import re


class XBRL_Mapper:
    def __init__(self, f, t=0):
        self.facts = f
        self.t = t

    def r(self, v, mul, u='USD'):
        t = self.t
        if t == 0:
            t = 'FY'
        else:
            t = 'Q'
        if mul:
            val = {}
            v = v['units'][u]
            if len(v) == 0:
                pass
            for i in v:
                if t in i['fp']:
                    if i['val'] is None:
                        val[i['fy']] = 0
                    if i['val']:
                        val[i['fy']] = i['val']
            return val
        else:
            v = v['units'][u]
            if len(v) == 0:
                return 0
            v = v[::-1]
            for i in v:
                if i['fp'] == t:
                    if i['val'] is None:
                        return 0
                    if i['val']:
                        return i['val']
        return 0

    def get_v(self, v, m):
        for val in v:
            if val in self.facts.keys():
                if (self.r(self.facts[val], m)):
                    return self.r(self.facts[val], m)
        return 0


class BalanceSheet(XBRL_Mapper):
    def __init__(self, facts, mul, t=0):
        super().__init__(facts, t)
        self.facts = facts
        self._assets_v = ['Assets']
        self._current_assets_v = ['AssetsCurrent']
        self._non_current_assets_v = ['AssetsNoncurrent']
        self._liabilities_and_equity_v = ['LiabilitiesAndStockholdersEquity',
                                          'LiabilitiesAndPartnersCapital']
        self._liabilities_v = ['Liabilities']
        self._current_liabilities_v = ['LiabilitiesCurrent']
        self._non_current_liabilities_v = ['LiabilitiesNoncurrent']
        self._commitments_and_contingencies_v = ['CommitmentsAndContingencies']
        self._temporary_equity_v = ['TemporaryEquityRedemptionValue',
                                    'RedeemablePreferredStockCarryingAmount',
                                    'TemporaryEquityCarryingAmount',
                                    'TemporaryEquityValueExcludingAdditionalPaidInCapital',
                                    'TemporaryEquityCarryingAmountAttributableToParent',
                                    'RedeemableNoncontrollingInterestEquityFairValue']

        self._redeemable_noncontrolling_interest_v = [
            'RedeemableNoncontrollingInterestEquityCarryingAmount']
        self._equity_v = ['StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',
                          'StockholdersEquity',
                          'PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest',
                          'PartnersCapital',
                          'CommonStockholdersEquity',
                          'MemberEquity',
                          'AssetsNet']
        self._equity_attributable_to_noncontrolling_interest_v = ['MinorityInterest',
                                                                  'PartnersCapitalAttributableToNoncontrollingInterest']
        self._equity_attributable_to_parent_v = ['StockholdersEquity']

        self._assets = self.get_v(self._assets_v, mul)
        self._current_assets = self.get_v(self._current_assets_v, mul)
        self._non_current_assets = self.get_v(self._non_current_assets_v, mul)
        self._liabilities_and_equity = self.get_v(
            self._liabilities_and_equity_v, mul)
        self._liabilities = self.get_v(self._liabilities_v, mul)
        self._current_liabilities = self.get_v(
            self._current_liabilities_v, mul)
        self._non_current_liabilities = self.get_v(
            self._non_current_liabilities_v, mul)
        self._commitments_and_contingencies = self.get_v(
            self._commitments_and_contingencies_v, mul)
        self._temporary_equity = self.get_v(self._temporary_equity_v, mul)
        self._redeemable_noncontrolling_interest = self.get_v(
            self._redeemable_noncontrolling_interest_v, mul)
        self._equity = self.get_v(self._equity_v, mul)
        self._equity_attributable_to_noncontrolling_interest = self.get_v(
            self._equity_attributable_to_noncontrolling_interest_v, mul)
        self._equity_attributable_to_parent = self.get_v(
            self._equity_attributable_to_parent_v, mul)
        # self.adjust_fields()

    def adjust_fields(self):
        if self._non_current_assets == 0:
            self._non_current_assets = self._assets - self._current_assets
        if self._non_current_liabilities == 0:
            self._non_current_liabilities = self._liabilities - self._current_liabilities
        self._temporary_equity += self._redeemable_noncontrolling_interest
        if self._assets == 0:
            self._assets = self._current_assets + self._non_current_assets
        if self._assets == 0:
            self._assets = self._liabilities_and_equity
        if self._liabilities == 0:
            self._liabilities = self._current_liabilities + self._non_current_liabilities
        if self._liabilities == 0:
            self._liabilities = self._assets - self._equity
        if self._equity == 0:
            self._equity = self._assets - self._liabilities

    def attrs(self):
        return {
            'assets': self._assets,
            'currentAssets': self._current_assets,
            'nonCurrentAssets': self._non_current_assets,
            'liabilitiesAndEquity': self._liabilities_and_equity,
            'liabilities': self._liabilities,
            'currentLiabilities': self._current_liabilities,
            'nonCurrentLiabilities': self._non_current_liabilities,
            'commitmentsAndContingencies': self._commitments_and_contingencies,
            'temporaryEquity': self._temporary_equity,
            'redeemableNoncontrollingInterest': self._redeemable_noncontrolling_interest,
            'equity': self._equity,
            'equityAttributableToNoncontrollingInterest': self._equity_attributable_to_noncontrolling_interest,
            'equityAttributableToParent': self._equity_attributable_to_parent
        }


class IncomeStatement(XBRL_Mapper):
    def __init__(self, facts, mul, t=0):
        super().__init__(facts, t)
        self.facts = facts
        self._revenue_v = ['Revenues',
                           'SalesRevenueNet',
                           'SalesRevenueServicesNet',
                           'RevenuesNetOfInterestExpense',
                           'RegulatedAndUnregulatedOperatingRevenue',
                           'HealthCareOrganizationRevenue',
                           'InterestAndDividendIncomeOperating',
                           'RealEstateRevenueNet',
                           'RevenueMineralSales',
                           'OilAndGasRevenue',
                           'FinancialServicesRevenue',
                           'RegulatedAndUnregulatedOperatingRevenue']

        self._cost_of_revenue_v = [
            'CostOfRevenue',
            'CostOfServices',
            'CostOfGoodsSold',
            'CostOfGoodsAndServicesSold']
        self._gross_profit_v = ['GrossProfit']
        self._operating_expenses_v = [
            'OperatingExpenses',
            'OperatingCostsAndExpenses']
        self._costs_and_expenses_v = ['CostsAndExpenses']
        self._other_operating_income_v = ['OtherOperatingIncome']
        self._operating_income_v = ['OperatingIncomeLoss']

        self._non_operating_income_v = ['NonoperatingIncomeExpense']
        self._interest_and_debt_expense_v = ['InterestAndDebtExpense']
        self._income_before_equity_investments_v = [
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments']
        self._income_from_equity_investments_v = [
            'IncomeLossFromEquityMethodInvestments']
        self._income_before_tax_v = [
            'IncomeBeforeTax', 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments']
        self._income_tax_expense_v = ['IncomeTaxExpense']
        self._income_tax_v = ['IncomeTax']
        self._net_income_v = ['NetIncomeLoss', 'ProfitLoss',
                              'NetIncomeLossAvailableToCommonStockholdersBasic',
                              'IncomeLossFromContinuingOperations', 'IncomeLossAttributableToParent', 'IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest']
        self._net_income_available_to_common_stockholders_basic_v = [
            'NetIncomeLossAvailableToCommonStockholdersBasic']
        self._dividends_v = ['PreferredStockDividendsAndOtherAdjustments']
        self._comprehensive_income_v = ['ComprehensiveIncomeNetOfTaxIncludingPortionAttributableToNoncontrollingInterest',
                                        'ComprehensiveIncomeNetOfTax', 'ComprehensiveIncome']

        self._revenue = self.get_v(self._revenue_v, mul)
        self._cost_of_revenue = self.get_v(self._cost_of_revenue_v, mul)
        self._gross_profit = self.get_v(self._gross_profit_v, mul)
        self._operating_expenses = self.get_v(self._operating_expenses_v, mul)
        self._costs_and_expenses = self.get_v(self._costs_and_expenses_v, mul)
        self._other_operating_income = self.get_v(
            self._other_operating_income_v, mul)
        self._operating_income = self.get_v(self._operating_income_v, mul)
        self._non_operating_income = self.get_v(
            self._non_operating_income_v, mul)
        self._interest_and_debt_expense = self.get_v(
            self._interest_and_debt_expense_v, mul)
        self._income_before_equity_investments = self.get_v(
            self._income_before_equity_investments_v, mul)
        self._income_from_equity_investments = self.get_v(
            self._income_from_equity_investments_v, mul)
        self._income_before_tax = self.get_v(self._income_before_tax_v, mul)
        self._income_tax_expense = self.get_v(self._income_tax_expense_v, mul)
        self._income_tax = self.get_v(self._income_tax_v, mul)
        self._net_income = self.get_v(self._net_income_v, mul)

    def attrs(self):
        return {
            'revenue': self._revenue,
            'costOfRevenue': self._cost_of_revenue,
            'grossProfit': self._gross_profit,
            'operatingExpenses': self._operating_expenses,
            'costsAndExpenses': self._costs_and_expenses,
            'otherOperatingIncome': self._other_operating_income,
            'operatingIncome': self._operating_income,
            'nonOperatingIncome': self._non_operating_income,
            'interestAndDebtExpense': self._interest_and_debt_expense,
            'incomeBeforeEquityInvestments': self._income_before_equity_investments,
            'incomeFromEquityInvestments': self._income_from_equity_investments,
            'incomeBeforeTax': self._income_before_tax,
            'incomeTaxExpense': self._income_tax_expense,
            'incomeTax': self._income_tax,
            'netIncome': self._net_income,
        }


class CashFlow(XBRL_Mapper):
    def __init__(self, facts, mul, t=0):
        super().__init__(facts, t)
        self.facts = facts
        self._net_cash_flow_v = [
            'CashAndCashEquivalentsPeriodIncreaseDecrease', 'CashPeriodIncreaseDecrease', 'NetCashProvidedByUsedInContinuingOperations']
        self._net_cash_flow_operating_v = [
            'NetCashProvidedByUsedInOperatingActivities']
        self._net_cash_flow_investing_v = [
            'NetCashProvidedByUsedInInvestingActivities']
        self._net_cash_flow_financing_v = [
            'NetCashProvidedByUsedInFinancingActivities']
        self._net_cash_flow_operating_continuing_v = [
            'NetCashProvidedByUsedInOperatingActivitiesContinuingOperations']
        self._net_cash_flow_investing_continuing_v = [
            'NetCashProvidedByUsedInInvestingActivitiesContinuingOperations']
        self._net_cash_flow_financing_continuing_v = [
            'NetCashProvidedByUsedInFinancingActivitiesContinuingOperations']
        self._net_cash_flow_operating_discontined_v = [
            'CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations']
        self._net_cash_flow_investing_discontined_v = [
            'CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations']
        self._net_cash_flow_financing_discontined_v = [
            'CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations']
        self._net_cash_flow_discontinued_v = [
            'NetCashProvidedByUsedInDiscontinuedOperations']
        self._exchange_rate_adjustment_v = [
            'EffectOfExchangeRateOnCashAndCashEquivalents', 'EffectOfExchangeRateOnCashAndCashEquivalentsContinuingOperations']

        self._net_cash_flow = self.get_v(self._net_cash_flow_v, mul)
        self._net_cash_flow_operating = self.get_v(
            self._net_cash_flow_operating_v, mul)
        self._net_cash_flow_investing = self.get_v(
            self._net_cash_flow_investing_v, mul)
        self._net_cash_flow_financing = self.get_v(
            self._net_cash_flow_financing_v, mul)
        self._net_cash_flow_operating_continuing = self.get_v(
            self._net_cash_flow_operating_continuing_v, mul)
        self._net_cash_flow_investing_continuing = self.get_v(
            self._net_cash_flow_investing_continuing_v, mul)
        self._net_cash_flow_financing_continuing = self.get_v(
            self._net_cash_flow_financing_continuing_v, mul)
        self._net_cash_flow_operating_discontined = self.get_v(
            self._net_cash_flow_operating_discontined_v, mul)
        self._net_cash_flow_investing_discontined = self.get_v(
            self._net_cash_flow_investing_discontined_v, mul)
        self._net_cash_flow_financing_discontined = self.get_v(
            self._net_cash_flow_financing_discontined_v, mul)
        self._net_cash_flow_discontinued = self.get_v(
            self._net_cash_flow_discontinued_v, mul)
        self._exchange_rate_adjustment = self.get_v(
            self._exchange_rate_adjustment_v, mul)

    def attrs(self):
        return {
            'netCashFlow': self._net_cash_flow,
            'netCashFlowOperating': self._net_cash_flow_operating,
            'netCashFlowInvesting': self._net_cash_flow_investing,
            'netCashFlowFinancing': self._net_cash_flow_financing,
            'netCashFlowOperatingContinuing': self._net_cash_flow_operating_continuing,
            'netCashFlowInvestingContinuing': self._net_cash_flow_investing_continuing,
            'netCashFlowFinancingContinuing': self._net_cash_flow_financing_continuing,
            'netCashFlowOperatingDiscontinued': self._net_cash_flow_operating_discontined,
            'netCashFlowInvestingDiscontinued': self._net_cash_flow_investing_discontined,
            'netCashFlowFinancingDiscontinued': self._net_cash_flow_financing_discontined,
            'netCashFlowDiscontinued': self._net_cash_flow_discontinued,
            'exchangeRateAdjustment': self._exchange_rate_adjustment
        }
