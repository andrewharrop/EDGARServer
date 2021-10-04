class CompanyTest:
    def __init__(self, tls=100):
        self.tls = int(tls*0.05)
        self.tickers = open('ttl.txt', 'r').read().split('\n')[::self.tls]

    def unit_test(self, C, *args):
        tl = [[] for _ in range(len(args))]
        for ticker in self.tickers:
            print(f'\n\nBreakdown for {ticker}\n')
            c = C(ticker)
            for a in range(len(args)):
                f = getattr(c, args[a])
                tl[a].append(f)
                print(
                    f'{args[a]} nonzero rate: {(1-([f[i] for i in f].count(0))/len(f))}')
        tll = len(tl)
        ranges = []
        counts = [[]]
        for a in range(tll):
            ranges.append(len(tl[a])*tll)
            c = 0
