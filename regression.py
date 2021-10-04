# Best to use a venv or something like conda here, especially on M1 chips


from company import CompanyFrames

# Determine the correlation between returns and all covariates


class LinearRegressionFit:
    def __init__(self, cik):
        self.company = CompanyFrames(cik, True)
        self.balance_sheet = self.company.balance_sheet
        self.income_statement = self.company.income_statement
        self.cash_flow = self.company.cash_flow

        self.price_data = self.company.fy_prices
        self.price_deltas = self.company.price_deltas


a = LinearRegressionFit('aapl')
print(a.__dict__.keys())
