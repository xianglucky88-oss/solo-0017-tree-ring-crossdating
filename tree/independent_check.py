"""Compare a uniquely dated specimen with a separately labelled repeat reading."""
from .dating import dated_series
from .observations import widths


def verify(doc):
    witness = doc['witness_reading']
    key, start, limit, minimum = (witness[k] for k in ('id', 'start_year', 'max_delta_um', 'min_pairs'))
    sequence = widths(witness['widths_um'])
    if not isinstance(key, str) or not key.strip() or len(key) > 80 or key in doc['references']:
        raise ValueError('witness_identity')
    if type(start) is not int or not 1 <= start <= 9999 - len(sequence) + 1:
        raise ValueError('witness_start')
    if type(limit) is not int or not 0 <= limit <= 1_000_000:
        raise ValueError('witness_max_delta')
    if type(minimum) is not int or not 1 <= minimum <= len(sequence):
        raise ValueError('witness_min_pairs')
    dated = dated_series(doc)
    if dated['state'] != 'dated':
        return {'state': 'unplaced', 'placement': dated, 'witness': key, 'rows': []}
    rows, observed, conflicts = [], 0, 0
    for row in dated['dated_widths']:
        year, target = row['year'], row['width_um']
        i = year - start
        repeat = sequence[i] if 0 <= i < len(sequence) else None
        delta = abs(repeat - target) if target is not None and repeat is not None else None
        if delta is None:
            state = 'missing' if 0 <= i < len(sequence) else 'outside_witness'
        else:
            observed += 1
            conflicts += delta > limit
            state = 'conflict' if delta > limit else 'consistent'
        rows.append({'year': year, 'core_index': row['core_index'], 'target_um': target,
                     'witness_um': repeat, 'delta_um': delta, 'state': state})
    return {'state': 'conflict' if conflicts else ('insufficient' if observed < minimum else 'confirmed'),
            'witness': key, 'start_year': dated['start_year'], 'comparable': observed, 'rows': rows}
