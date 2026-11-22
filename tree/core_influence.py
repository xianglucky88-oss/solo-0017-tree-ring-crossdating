"""Measure how removing a single dated reference changes the recommendation."""
from .offsets import shortlist


def _decision(result):
    return {'state': result['state'], 'starts': [row['start_year'] for row in result.get('leaders', [])]}


def assess(doc):
    baseline = _decision(shortlist(doc))
    rows = []
    for core in sorted(doc['references']):
        remaining = {k: v for k, v in doc['references'].items() if k != core}
        if len(remaining) < doc['quorum']:
            outcome = {'state': 'quorum_unreachable', 'starts': []}
        else:
            outcome = _decision(shortlist({**doc, 'references': remaining}))
        rows.append({'excluded': core, **outcome, 'changed': outcome != baseline})
    return {'baseline': baseline, 'rows': rows, 'changed_count': sum(r['changed'] for r in rows)}
