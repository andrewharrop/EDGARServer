# Wrapper for yfinance to get price data | Optimized
import yfinance as yf


class YCompany:
    def __init__(self, ticker):
        self.ticker = ticker
        self.comp = yf.Ticker(ticker)
        self.info = self.comp.info

    def price_current(self):
        return self.info['regularMarketPrice']

    def price_history(self, term='y'):
        if term == 'y':
            fr = self.comp.history(period='max', )
            fr['avg'] = fr[['Open', 'Close']].mean(axis=1)
            return fr[['Open', 'Close', 'avg']]
        if term == 'q':
            fr = self.comp.history(period='max', interval='3mo')
            fr['avg'] = fr[['Open', 'Close']].mean(axis=1)
            return fr[['Open', 'Close', 'avg']].dropna()

    def market_cap(self):
        return self.info['marketCap']

    def _test(self):
        print(self.info)
        print(self.price_current())
        print(self.price_history())
        print(self.market_cap())


# test = YCompany('AAPL')
