"""Build evidence-backed annual votes from observed width directions."""
from .observations import signs, widths


def consensus(doc):
    refs = doc['references']
    quorum = doc['quorum']
    if not isinstance(refs,dict) or not 1 <= len(refs) <= 30 or any(not k.strip() for k in refs):
        raise ValueError('reference_ids')
    if type(quorum) is not int or not 1 <= quorum <= len(refs):
        raise ValueError('quorum')
    by_year = {}
    for ref,row in sorted(refs.items()):
        first = row['start_year']
        values = widths(row['widths_um'])
        if type(first) is not int or not 1 <= first <= 9999 or first+len(values)-1 > 9999:
            raise ValueError('reference_start_year')
        for year,sign in enumerate(signs(values), first+1):
            bucket = by_year.setdefault(year, {-1:[],0:[],1:[]})
            if sign is not None:
                bucket[sign].append(ref)
    out = {}
    for year, votes in sorted(by_year.items()):
        best = max(len(v) for v in votes.values())
        leaders = [key for key,value in votes.items() if len(value)==best]
        voters = sum(map(len,votes.values()))
        state = 'too_few' if voters < quorum else ('split' if len(leaders) > 1 else 'consensus')
        out[year] = {'state':state,'direction':leaders[0] if state=='consensus' else None,'votes':votes}
    return out
