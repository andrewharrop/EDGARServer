class Construct:
    def __init__(self, balance_sheet, income_statement, cash_flow):
        self.balance_sheet = balance_sheet
        self.income_statement = income_statement
        self.cash_flow = cash_flow

    def profit_margin(self):
        if self.income_statement['revenue'] != 0:
            return self.income_statement['netIncome']/self.income_statement['revenue']
        return 0

    def ROA(self):
        if self.balance_sheet['assets']:
            return self.income_statement['netIncome']/self.balance_sheet['assets']
        return 0

    def ROE(self):
        if self.balance_sheet['equity']:
            return self.income_statement['netIncome']/self.balance_sheet['equity']
        return 0
