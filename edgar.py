# Wrapper for edgar api | Optimized
from requests import get
from json import loads
from json import dumps
from CIK_mapper import CIK_map

api_headers = {
    'User-Agent': 'FreeRange Data andrewhar05@gmail.com',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'data.sec.gov',
}


class Company:
    def __init__(self, cik):
        if cik.isdecimal():
            self.cik = cik
        else:
            self.cik = str(CIK_map(cik)["CIK"])
            self.cik = ("0" * (10-len(self.cik))) + self.cik

    def submissions(self):
        return get('https://data.sec.gov/submissions/CIK{}.json'.format(
            self.cik), headers=api_headers).json()

    def facts(self):
        return get('https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'.format(
            self.cik), headers=api_headers).json()

    def concepts(self, taxonomy, tag):
        return get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/{}/{}.json'.format(
            self.cik, taxonomy, tag), headers=api_headers).json()


def frame(taxonomy, tag, unit, period):
    return get('https://data.sec.gov/api/xbrl/frames/CIK{}/{}/{}.json'.format(
        taxonomy, tag, unit, period), headers=api_headers).json()
