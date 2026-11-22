"""Build an annual measurement inventory without borrowing dates from unresolved cores."""
from .observations import widths
from .relative_dating import place


def inventory(doc):
    query = doc['calendar_inventory']
    first, last = query['years']
    minimum = query['min_observed']
    if (any(type(n) is not int for n in (first, last, minimum))
            or not 1 <= first <= last <= 9999 or last-first >= 400 or not 1 <= minimum <= 12):
        raise ValueError('inventory_bounds')
    positioning = place(doc)
    observed = {year: [] for year in range(first, last+1)}
    missing = {year: [] for year in observed}
    withheld = {}
    for component in positioning['components']:
        if component['state'] != 'dated':
            withheld.update((name, component['state']) for name in component['relative_offsets'])
            continue
        for key, start in component['start_years'].items():
            core = widths(doc['relative_cores'][key]['undated_widths_um'])
            for year in range(max(first, start), min(last+1, start+len(core))):
                index = year-start
                destination = missing if core[index] is None else observed
                destination[year].append({'core': key, 'index': index, 'width_um': core[index]})
    rows = [{'year': year, 'state': ('supported' if len(entries) >= minimum else
                                    'insufficient' if entries else 'unobserved'),
             'observations': sorted(entries, key=lambda row: row['core']),
             'missing_slots': sorted(missing[year], key=lambda row: row['core'])}
            for year, entries in observed.items()]
    return {'state': 'supported' if all(row['state'] == 'supported' for row in rows) else 'partial',
            'years': rows, 'withheld_cores': withheld}
