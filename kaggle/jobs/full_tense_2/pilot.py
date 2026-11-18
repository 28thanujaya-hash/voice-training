# Full run · F tense, batch 2/4 (user 19 Nov 00:53: tense = context "Give it back!" only, no tag; 4 takes; all marked by ear)
LINES = {'tense': ['m3t44', 'm3t45', 'm3t46', 'm3t47', 'm3t48', 'm3t49', 'm3t50', 'm3t51', 'm3t52', 'm3t53', 'm3t54', 'm3t55', 'm3t56', 'm3t57', 'm3t58', 'm3t59', 'm3t60', 'm3t61', 'm3t62', 'm3t63', 'm3t64', 'm3t65', 'm3t66', 'm3t67', 'm3t68', 'm3t69', 'm3t70', 'm3t71', 'm3t72', 'm3t74', 'm3t75', 'm3xt01', 'm3xt02', 'm3xt03', 'm3xt04', 'm3xt05', 'm3xt06', 'm3xt07', 'm3xt08', 'm3xt09', 'm3xt10']}
REF = {'artic': 4.2075, 'lufs': -27.388, 'f0_med': 10.970500000000001, 'f0_sd': 2.0309999999999997, 'h1h2': 7.1315, 'slope': -0.7204999999999999, 'int_drop': -3.503, 'final_drop': -1.3359999999999999}
CTX = {'tense': {"file": "ctx_tense.mp3", "text": "Give it back!"}}
ARMS = {'tense': {'T': (True, None, False)}}   # (context?, tag, "!" ending?)
def excl(t): return t
TAKES = 4
