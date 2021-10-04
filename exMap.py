from requests import get
from json import loads
from json import dumps


def CIK_update():
    with open('CompanyCIK.json', 'w') as cj:
        r = loads(get(
            'https://www.sec.gov/files/company_tickers_exchange.json').content.decode())['data']
        c = {co[2]: {'CIK': co[0], 'name': co[1]} for co in r}
        cj.write(dumps(c))
    with open('MFCIK.json', 'w') as mf:
        r = loads(get(
            'https://www.sec.gov/files/company_tickers_mf.json').content.decode())['data']
        c = {co[3]: co[1] for co in r}
        mf.write(dumps(c))


def CIK_map(t, f=False):
    t = t.upper()
    if f:
        with open('MFCIK.json', 'r') as mf:
            try:
                cik = loads(mf.read())[t]
                return cik
            except KeyError:
                return {}
    with open('CompanyCIK.json', 'r') as cj:
        try:
            cik = loads(cj.read())[t]

            return cik
        except KeyError:
            return {}
