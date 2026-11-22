"""Join the dated series back to annual vote sources, marking unused evidence."""
from .dating import dated_series
from .reference import consensus


def prove(doc):
    dated = dated_series(doc)
    if dated['state'] != 'dated':
        return dated
    votes = consensus(doc)
    years = []
    for width in dated['dated_widths']:
        record = votes.get(width['year'])
        comparison = width['comparison']
        used = comparison is not None
        years.append({**width, 'used_for_alignment': used,
                      'reference_status': record['state'] if record else 'no_reference',
                      'all_reference_votes': record['votes'] if record else {}})
    return {'state': 'dated', 'start_year': dated['start_year'], 'years': years}
