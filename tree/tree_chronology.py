"""Produce a chronology where each observed physical tree contributes once per year."""
from collections import defaultdict
from fractions import Fraction

from .calendar_inventory import inventory


def summarize(doc):
    plan = doc['tree_chronology']
    parents, minimum = plan['parents'], plan['min_trees']
    if (not isinstance(parents, dict) or set(parents) != set(doc['relative_cores'])
            or any(not isinstance(name, str) or not name.strip() or len(name) > 80 for name in parents.values())):
        raise ValueError('chronology_parent_mapping')
    if type(minimum) is not int or not 1 <= minimum <= 12:
        raise ValueError('chronology_tree_count')
    available = inventory(doc)
    rows = []
    for row in available['years']:
        groups = defaultdict(list)
        for observation in row['observations']:
            groups[parents[observation['core']]].append(observation)
        trees, values = {}, []
        for name, readings in sorted(groups.items()):
            mean = Fraction(sum(r['width_um'] for r in readings), len(readings))
            values.append(mean)
            trees[name] = {'mean_um': str(mean), 'measurements': readings}
        sufficient = len(values) >= minimum
        rows.append({'year': row['year'], 'state': 'supported' if sufficient else 'insufficient_trees',
                     'mean_um': str(sum(values)/len(values)) if sufficient else None, 'trees': trees})
    return {'state': 'supported' if all(row['state'] == 'supported' for row in rows) else 'partial',
            'min_trees': minimum, 'years': rows, 'withheld_cores': available['withheld_cores']}
