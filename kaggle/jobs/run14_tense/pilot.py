# Run 14 · tense: does <gasp> (or a "!" ending) raise her pitch on outraged lines? (user 18 Nov 17:09 "try one")
# 12 outraged/indignant tense lines, all with the approved tense context "Give it back!" (run7_five tense_01):
#   C = no context, as written (plain baseline for rel_* and the pairs) · X = context, as written (the tense recipe)
#   XG = context + <gasp> before the line · XE = context, last "." -> "!" and "?" -> "?!"
LINES = {'tense': ['m3t53', 'm3t54', 'm3t16', 'm3t58', 'm3t18', 'm3t42', 'm3t72', 'm3t44', 'm3t50', 'm3t68', 'm3t47', 'm3t22']}
REF = {'artic': 4.2075, 'lufs': -27.388, 'f0_med': 10.970500000000001, 'f0_sd': 2.0309999999999997, 'h1h2': 7.1315, 'slope': -0.7204999999999999, 'int_drop': -3.503, 'final_drop': -1.3359999999999999}
CTX = {'tense': {"file": "ctx_tense.mp3", "text": "Give it back!"}}
# Arms: (context?, tag, "!" ending?)
ARMS = {'tense': {'C': (False, None, False), 'X': (True, None, False), 'XG': (True, '<gasp>', False), 'XE': (True, None, True)}}
def excl(t):
    t = t.rstrip()
    if t.endswith("?"): return t + "!"
    if t.endswith("."): return t[:-1] + "!"
    return t
TAKES = 3
