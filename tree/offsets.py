"""Rank candidate starts on exact agreement and evidence coverage."""
from fractions import Fraction
from .observations import signs, widths
from .reference import consensus


def evaluate(doc):
    ref = consensus(doc)
    target = widths(doc['undated_widths_um'])
    series = tuple(signs(target))
    first,last = doc['start_range']
    needed = doc['min_pairs']
    if any(type(x) is not int for x in (first,last,needed)) or not 1 <= first <= last <= 9999 or last + len(series) > 9999 or last-first > 1_000 or not 1 <= needed <= len(series):
        raise ValueError('candidate_bounds')
    eligible, all_rows = [], []
    for candidate in range(first,last+1):
        pairs = []
        matches = 0
        for idx, observed in enumerate(series,1):
            expected = ref.get(candidate+idx)
            if observed is None or not expected or expected['state'] != 'consensus':
                continue
            matches += observed == expected['direction']
            pairs.append({'year':candidate+idx,'transition_index':idx,'observed':observed,'reference':expected['direction'],'voters':expected['votes'][expected['direction']]})
        count = len(pairs)
        row = {'start_year':candidate,'pair_count':count,'matches':matches,'agreement':str(Fraction(matches,count)) if count else None}
        all_rows.append(row)
        if count >= needed:
            eligible.append(((Fraction(matches,count),count), row, pairs))
    if not eligible:
        return {'state':'not_enough_overlap','candidates':all_rows}, target
    highest = max(rank for rank,_,_ in eligible)
    best = [{**row,'pairs':pairs} for rank,row,pairs in eligible if rank==highest]
    return {'state':'unique' if len(best)==1 else 'tie','leaders':best,'candidates':all_rows}, target


def shortlist(doc):
    return evaluate(doc)[0]
