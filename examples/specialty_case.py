from copy import deepcopy

from tree.tree_chronology import summarize


OPERATION = 'tree-chronology'
OPTIONAL_FIELD = 'tree_chronology'


def perturb(doc):
    doc['tree_chronology']['parents']['b'] = doc['tree_chronology']['parents']['a']


def verify(before, after):
    assert before['state'] == 'supported' and [row['mean_um'] for row in before['years']] == ['17', '21']
    assert after['state'] == 'partial' and not after['withheld_cores']
    first = after['years'][0]
    assert first['mean_um'] is None and first['state'] == 'insufficient_trees'
    assert [r['core'] for r in first['trees']['ridge-oak-3']['measurements']] == ['a', 'b']


def edge_cases(doc):
    a = deepcopy(doc)
    a['relative_links'][0]['shift_years'] = 0
    assert summarize(a)['withheld_cores'] == {'b': 'ambiguous'}
    assert all(len(row['trees']) == 1 and row['mean_um'] is None for row in summarize(a)['years'])

    b = deepcopy(doc)
    b['relative_cores']['c'] = {**b['relative_cores']['b'], 'undated_widths_um': [18, 22]}
    b['relative_links'].append({**b['relative_links'][0], 'right': 'c', 'max_delta_um': 1})
    b['tree_chronology']['parents']['c'] = b['tree_chronology']['parents']['a']
    assert [row['mean_um'] for row in summarize(b)['years']] == ['69/4', '85/4']
