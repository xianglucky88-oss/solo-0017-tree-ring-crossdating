"""Materialize dated measurements only where the ranking is unambiguous."""
from .offsets import evaluate


def dated_series(doc):
    result, target = evaluate(doc)
    if result['state'] != 'unique':
        return {'state': result['state'], 'eligible_starts': [row['start_year'] for row in result.get('leaders',[])]}
    best = result['leaders'][0]
    start = best['start_year']
    evidence = {row['transition_index']:row for row in best['pairs']}
    return {'state':'dated', 'start_year':start, 'match_evidence':best['agreement'], 'dated_widths':[
        {'year':start+i,'core_index':i,'width_um':value,'comparison':evidence.get(i)}
        for i,value in enumerate(target)]}
