# Term Container | Optimized

class Terms:
    def __init__(self):

        self.balance_sheet_terms = {
            'assets': ['Assets'],
            'currentAssets': ['AssetsCurrent'],
            'nonCurrentAssets': ['AssetsNoncurrent'],
            'liabilitiesAndEquity': ['LiabilitiesAndStockholdersEquity',
                                     'LiabilitiesAndPartnersCapital'],
            'liabilities': ['Liabilities'],
            'currentLiabilities': ['LiabilitiesCurrent'],
            'nonCurrentLiabilities': ['LiabilitiesNoncurrent'],
            'commitmentsAndContingencies': ['CommitmentsAndContingencies'],
            'temporaryEquity': ['TemporaryEquityRedemptionValue',
                                'RedeemablePreferredStockCarryingAmount',
                                'TemporaryEquityCarryingAmount',
                                'TemporaryEquityValueExcludingAdditionalPaidInCapital',
                                'TemporaryEquityCarryingAmountAttributableToParent',
                                'RedeemableNoncontrollingInterestEquityFairValue'],
            'redeemableNoncontrollingInterest': ['RedeemableNoncontrollingInterestEquityCarryingAmount'],
            'equity': ['StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',
                       'StockholdersEquity',
                       'PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest',
                       'PartnersCapital',
                       'CommonStockholdersEquity',
                       'MemberEquity',
                       'AssetsNet'],
            'equityAttributableToNoncontrollingInterest': ['MinorityInterest',
                                                           'PartnersCapitalAttributableToNoncontrollingInterest'],
            'equityAttributableToParent': ['StockholdersEquity']
        }

        self.income_statement_terms = {
            'revenue': ['Revenues',
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
                        'RegulatedAndUnregulatedOperatingRevenue'],
            'cost_of_revenue': ['CostOfRevenue',
                                'CostOfServices',
                                'CostOfGoodsSold',
                                'CostOfGoodsAndServicesSold'],
            'gross_profit': ['GrossProfit'],
            'operating_expenses': ['OperatingExpenses',
                                   'OperatingCostsAndExpenses'],
            'costs_and_expenses': ['CostsAndExpenses'],
            'other_operating_income': ['OtherOperatingIncome'],
            'operating_income': ['OperatingIncomeLoss'],
            'non_operating_income': ['NonoperatingIncomeExpense'],
            'interest_and_debt_expense': ['InterestAndDebtExpense'],
            'income_before_equity_investments': [
                'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments'],
            'income_from_equity_investments': [
                'IncomeLossFromEquityMethodInvestments'],
            'income_before_tax': ['IncomeBeforeTax',
                                  'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments'],
            'income_tax_expense': ['IncomeTaxExpense'],
            'income_tax': ['IncomeTax'],
            'net_income': ['NetIncomeLoss',
                           'ProfitLoss',
                           'NetIncomeLossAvailableToCommonStockholdersBasic',
                           'IncomeLossFromContinuingOperations',
                           'IncomeLossAttributableToParent',
                           'IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest'],
            'net_income_available_to_common_stockholders_basic': [
                'NetIncomeLossAvailableToCommonStockholdersBasic'],
            'dividends': ['PreferredStockDividendsAndOtherAdjustments'],
            'comprehensive_income': ['ComprehensiveIncomeNetOfTaxIncludingPortionAttributableToNoncontrollingInterest',
                                     'ComprehensiveIncomeNetOfTax',  'ComprehensiveIncome']
        }

        self.cash_flow_terms = {
            'net_cash_flow': ['CashAndCashEquivalentsPeriodIncreaseDecrease',
                              'CashPeriodIncreaseDecrease',
                              'NetCashProvidedByUsedInContinuingOperations'],
            'net_cash_flow_operating': ['NetCashProvidedByUsedInOperatingActivities'],
            'net_cash_flow_investing': ['NetCashProvidedByUsedInInvestingActivities'],
            'net_cash_flow_financing': ['NetCashProvidedByUsedInFinancingActivities'],
            'net_cash_flow_operating_continuing': [
                'NetCashProvidedByUsedInOperatingActivitiesContinuingOperations'],
            'net_cash_flow_investing_continuing': [
                'NetCashProvidedByUsedInInvestingActivitiesContinuingOperations'],
            'net_cash_flow_financing_continuing': [
                'NetCashProvidedByUsedInFinancingActivitiesContinuingOperations'],
            'net_cash_flow_operating_discontined': [
                'CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations'],
            'net_cash_flow_investing_discontined': [
                'CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations'],
            'net_cash_flow_financing_discontined': [
                'CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations'],
            'net_cash_flow_discontinued': [
                'NetCashProvidedByUsedInDiscontinuedOperations'],
            'exchange_rate_adjustment': [
                'EffectOfExchangeRateOnCashAndCashEquivalents',
                'EffectOfExchangeRateOnCashAndCashEquivalentsContinuingOperations']
        }
