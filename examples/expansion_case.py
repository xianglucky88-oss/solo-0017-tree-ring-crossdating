OPERATION = 'relative-dating'
OPTIONAL_FIELD = 'relative_cores'


def perturb(doc):
    doc['relative_links'][0]['shift_years'] = 0


def verify(before, after):
    assert before['links'][0]['pairs'] == [[1, 0, 0], [2, 1, 0]]
    assert before['local_reference_leaders']['b'] == [1940, 1942]
    component, = before['components']
    assert component['state'] == 'dated' and component['start_years'] == {'a': 1941, 'b': 1942}
    assert after['links'][0]['state'] == 'measurement_conflict'
    a, b = after['components']
    assert a['start_years'] == {'a': 1941}
    assert b['state'] == 'ambiguous' and b['start_years'] == {}


def edge_cases(doc):
    from tree.relative_dating import place

    same = {'undated_widths_um': [10, 10, 10], 'start_range': [1940, 1944], 'min_pairs': 2}
    # The reassembled component has several possible starts but no credited reference vote.
    cores = {key: {**same, 'start_range': [1900, 1904]} for key in ('a', 'b', 'c')}
    links = [dict(left=a, right=b, shift_years=shift, min_pairs=2, max_delta_um=0)
             for a, b, shift in [('a', 'b', 1), ('b', 'c', 1), ('a', 'c', 1)]]
    result = place({**doc, 'relative_cores': cores, 'relative_links': links})
    assert all(row['state'] == 'supported' for row in result['links'])
    component, = result['components']
    assert component['state'] == 'cycle_conflict' and component['start_years'] == {}
    assert component['conflicting_link_indices']
    repaired = place({**doc, 'relative_cores': cores, 'relative_links': links[:2]})
    repaired_component, = repaired['components']
    assert repaired_component['state'] == 'unanchored' and not repaired_component['start_years']
    assert repaired_component['candidate_root_years'] == [1900, 1901, 1902]
