"""Validate observed widths and preserve missing years in direction series."""


def widths(values):
    if not isinstance(values,list) or not 2 <= len(values) <= 400:
        raise ValueError('core_length')
    if any(x is not None and (type(x) is not int or not 1 <= x <= 1_000_000) for x in values):
        raise ValueError('width_um')
    return values


def signs(values):
    for a,b in zip(values,values[1:]):
        yield None if a is None or b is None else (b>a)-(b<a)
