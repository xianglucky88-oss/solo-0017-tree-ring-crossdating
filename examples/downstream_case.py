OPERATION = 'calendar-inventory'
OPTIONAL_FIELD = 'calendar_inventory'


def perturb(doc):
    doc['relative_links'][0]['shift_years'] = 0


def verify(before, after):
    assert before['state'] == 'supported' and not before['withheld_cores']
    assert before['years'][0]['observations'] == [
        {'core': 'a', 'index': 1, 'width_um': 17}, {'core': 'b', 'index': 0, 'width_um': 17}]
    assert after['state'] == 'partial' and after['withheld_cores'] == {'b': 'ambiguous'}
    assert [row['state'] for row in after['years']] == ['insufficient', 'insufficient']
