# Process raw edgar data | Optimized

from term_map import Terms


def term_generator(terms, facts):
    output = {}
    for term in terms:
        for sub_term in terms[term]:
            if sub_term in facts and sub_term not in output:
                if 'USD' in facts[sub_term]['units']:
                    unit = 'USD'
                else:
                    unit = facts[sub_term]['units'].keys()[0]
                output[term] = facts[sub_term]['units'][unit]

    return output


def fp_generator(period):
    if period == 'annual':
        return 'FY'
    elif period == 'quarterly':
        return 'Q'


def fp_key_generator(term, datapoint, period, output):
    if period == "annual":
        output[term][datapoint['fy']] = datapoint['val']
    elif period == "quarterly":
        output[term][str(datapoint['fy'])+datapoint['fp']
                     ] = datapoint['val']


def period_generator(statement, period):
    output = {}
    fp = fp_generator(period)
    for term in statement:
        output[term] = {}
        for datapoint in statement[term]:
            if fp in datapoint['fp']:
                fp_key_generator(term, datapoint, period, output)

    return output


class Parser(Terms):
    def __init__(self, facts, form='us-gaap'):
        super().__init__()
        self.facts_raw = facts[form]

        self.balance_sheet_raw = term_generator(
            self.balance_sheet_terms, self.facts_raw)

        self.income_statement_raw = term_generator(
            self.income_statement_terms, self.facts_raw)

        self.cash_flow_raw = term_generator(
            self.cash_flow_terms, self.facts_raw)

    def periodical(self, period):
        bs = period_generator(self.balance_sheet_raw, period)
        is_ = period_generator(self.income_statement_raw, period)
        cf = period_generator(self.cash_flow_raw, period)
        return bs, is_, cf
