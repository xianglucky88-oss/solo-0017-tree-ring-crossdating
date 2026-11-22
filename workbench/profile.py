from tree.dating import dated_series as dated_widths
from tree.reference import consensus as reference_votes
from tree.offsets import shortlist as candidate_offsets
from tree.core_influence import assess as core_influence
from tree.vote_gaps import qualify as vote_gaps
from tree.year_proof import prove as year_proof

PRODUCT = '0017-tree-ring-crossdating'
TITLE = '木芯年轮定年工作台'
WORK_LABEL = '编年数据 / 转折票源'
THEME = 'tree'
DEFAULT_DATASET = 'chronology-core'
PORT = 8817

OPERATIONS = {
    'dated-widths': ('定年入档', dated_widths),
    'reference-votes': ('参考票源', reference_votes),
    'candidate-offsets': ('候选起年', candidate_offsets),
    'core-influence': ('逐芯留出复核', core_influence),
    'vote-gaps': ('无共识年份', vote_gaps),
    'year-proof': ('逐年票源证据', year_proof),
}
REQUIRED = ('dated-widths', 'reference-votes', 'candidate-offsets')
