"""Propagate physical overlap constraints before assigning calendar start years."""
from .offsets import evaluate


def _links(raw, widths):
    if not isinstance(raw, list) or not 1 <= len(raw) <= 60:
        raise ValueError('relative_link_count')
    seen, reports = set(), []
    for link in raw:
        left, right, shift = (link[k] for k in ('left', 'right', 'shift_years'))
        if left not in widths or right not in widths or left == right or type(shift) is not int or abs(shift) >= 400:
            raise ValueError('relative_link_members')
        key = (*sorted((left, right)), shift if left < right else -shift)
        if key in seen:
            raise ValueError('relative_link_duplicate')
        seen.add(key)
        minimum, limit = link['min_pairs'], link['max_delta_um']
        if (type(minimum) is not int or not 1 <= minimum <= 400
                or type(limit) is not int or not 0 <= limit <= 1_000_000):
            raise ValueError('relative_link_rule')
        a, b = widths[left], widths[right]
        pairs = [(i, i-shift, abs(a[i]-b[i-shift])) for i in range(max(0, shift), min(len(a), len(b)+shift))
                 if a[i] is not None and b[i-shift] is not None]
        state = ('measurement_conflict' if any(row[2] > limit for row in pairs) else
                 'insufficient_overlap' if len(pairs) < minimum else 'supported')
        reports.append({'left': left, 'right': right, 'shift_years': shift, 'state': state, 'pairs': pairs})
    return reports


def place(doc):
    cores = doc['relative_cores']
    if (not isinstance(cores, dict) or not 2 <= len(cores) <= 12
            or any(not name.strip() or len(name) > 80 or name in doc['references'] for name in cores)):
        raise ValueError('relative_cores')
    widths, leaders, permitted = {}, {}, {}
    for key, core in sorted(cores.items()):
        report, widths[key] = evaluate({**doc, **{field: core[field]
                                                  for field in ('undated_widths_um', 'start_range', 'min_pairs')}})
        leaders[key] = [row['start_year'] for row in report.get('leaders', [])]
        permitted[key] = range(core['start_range'][0], core['start_range'][1]+1)
    links = _links(doc['relative_links'], widths)
    edges = {key: [] for key in widths}
    for i, row in enumerate(links):
        if row['state'] == 'supported':
            a, b, shift = (row[k] for k in ('left', 'right', 'shift_years'))
            edges[a].append((b, shift, i))
            edges[b].append((a, -shift, i))

    remaining = set(widths)
    components = []
    while remaining:
        root = min(remaining)
        offsets, todo, mismatched = {root: 0}, [root], set()
        for member in todo:
            for neighbor, delta, i in sorted(edges[member]):
                required = offsets[member]+delta
                if neighbor not in offsets:
                    offsets[neighbor] = required
                    todo.append(neighbor)
                elif offsets[neighbor] != required:
                    mismatched.add(i)
        remaining.difference_update(offsets)
        options = [{year-offset for year in (leaders[key] or permitted[key])} for key, offset in offsets.items()]
        candidates = sorted(set.intersection(*options)) if not mismatched else []
        state = ('cycle_conflict' if mismatched else 'calendar_conflict' if not candidates else
                 'unanchored' if not any(leaders[key] for key in offsets) else
                 'dated' if len(candidates) == 1 else 'ambiguous')
        starts = {key: candidates[0]+offset for key, offset in offsets.items()} if state == 'dated' else {}
        components.append({'root': root, 'state': state, 'relative_offsets': offsets,
                           'candidate_root_years': candidates, 'conflicting_link_indices': sorted(mismatched),
                           'start_years': starts})
    return {'components': components, 'links': links, 'local_reference_leaders': leaders}
