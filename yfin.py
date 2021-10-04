# Wrapper for yfinance to get price data, used for return quantification
import yfinance as yf


class YCompany:
    def __init__(self, ticker):
        self.ticker = ticker
        self.comp = yf.Ticker(ticker)
        self.info = self.comp.info

    def price_current(self):
        return self.info['regularMarketPrice']

    def price_history(self):
        fr = self.comp.history(period='max', )
        fr['avg'] = fr[['Open', 'Close']].mean(axis=1)
        return fr[['Open', 'Close', 'avg']]

    def market_cap(self):
        return self.info['marketCap']

    def periodic_price_averages(self):
        fr = self.comp.history(period='max', interval='3mo')
        d = [p for p in fr[['Open', 'Close']].mean(
            axis=1) if isinstance(p, float)]
        dr = []
        c = 0
        s = 0
        for i in range(len(d)):
            c += d[i]
            s += 1
            if i % 4 == 0:
                dr.append(c/4)
                c = 0
                s = 0
        if s % 4 != 0:
            dr = dr[:-1]
            dr.append(c/s)
        return dr

    def _test(self):
        print(self.info)
        print(self.price_current())
        print(self.price_history())
        print(self.market_cap())
        print(self.periodic_price_averages())
