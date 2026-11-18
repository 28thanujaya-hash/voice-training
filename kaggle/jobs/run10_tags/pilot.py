# Run 10 · Orpheus sound tags for all three moods (user OK 18 Nov 10:18). Same 12 lines per mood as run 8 and the same
# clean-normal reference (run7_grey). The tag goes before the line; everything before the first word is cut off.
LINES = {'low': ['m3xl46', 'm3xl42', 'm3xl29', 'm3xl67', 'm3xl25', 'm3xl08', 'm4g19l', 'm3xl57', 'm4l03', 'm3l63', 'm3l10', 'm3l62'],
         'bright': ['m3xb02', 'm3xb24', 'm3b38', 'm4g19b', 'm4g18b', 'm3b42', 'm3b70', 'm3b54', 'm3b30', 'm3b57', 'm3b31', 'm3b63'],
         'tense': ['m3t15', 'm3xt54', 'm3xt37', 'm4g12t', 'm3xt12', 'm3xt70', 'm3xt24', 'm3xt34', 'm3t26', 'm3t10', 'm3t69', 'm3t51']}
REF = {'artic': 4.2075, 'lufs': -27.388, 'f0_med': 10.970500000000001, 'f0_sd': 2.0309999999999997, 'h1h2': 7.1315, 'slope': -0.7204999999999999, 'int_drop': -3.503, 'final_drop': -1.3359999999999999}
# Arms per mood: C = plain line (control, and the "normal" in the listening pairs); others = that Orpheus tag before the line.
ARMS = {'low': {'C': None, 'SN': '<sniffle>', 'S': '<sigh>'},
        'bright': {'C': None, 'CH': '<chuckle>', 'LA': '<laugh>', 'GA': '<gasp>'},
        'tense': {'C': None, 'GR': '<groan>'}}
TAKES = 2
