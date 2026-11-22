"""Explain whether a reference year lacks votes or has conflicting directions."""
from .reference import consensus


def qualify(doc):
    notes = []
    for year, record in consensus(doc).items():
        if record['state'] == 'consensus':
            continue
        counts = {direction: len(cores) for direction, cores in record['votes'].items()}
        absent = sorted(set(doc['references']) - {core for cores in record['votes'].values() for core in cores})
        notes.append({'year': year, 'state': record['state'], 'missing_cores': absent,
                      'counts': counts, 'votes': record['votes'], 'quorum_deficit': max(0, doc['quorum']-sum(counts.values()))})
    return {'years': notes, 'quorum': doc['quorum']}
