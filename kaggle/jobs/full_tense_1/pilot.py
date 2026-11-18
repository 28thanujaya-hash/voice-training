# Full run · F tense, batch 1/4 (user 19 Nov 00:53: tense = context "Give it back!" only, no tag; 4 takes; all marked by ear)
LINES = {'tense': ['m3t01', 'm3t02', 'm3t03', 'm3t04', 'm3t05', 'm3t06', 'm3t07', 'm3t08', 'm3t10', 'm3t11', 'm3t12', 'm3t14', 'm3t15', 'm3t16', 'm3t17', 'm3t18', 'm3t19', 'm3t20', 'm3t21', 'm3t22', 'm3t23', 'm3t24', 'm3t25', 'm3t26', 'm3t27', 'm3t28', 'm3t29', 'm3t30', 'm3t31', 'm3t32', 'm3t33', 'm3t34', 'm3t35', 'm3t36', 'm3t37', 'm3t38', 'm3t39', 'm3t40', 'm3t41', 'm3t42', 'm3t43']}
REF = {'artic': 4.2075, 'lufs': -27.388, 'f0_med': 10.970500000000001, 'f0_sd': 2.0309999999999997, 'h1h2': 7.1315, 'slope': -0.7204999999999999, 'int_drop': -3.503, 'final_drop': -1.3359999999999999}
CTX = {'tense': {"file": "ctx_tense.mp3", "text": "Give it back!"}}
ARMS = {'tense': {'T': (True, None, False)}}   # (context?, tag, "!" ending?)
def excl(t): return t
TAKES = 4
