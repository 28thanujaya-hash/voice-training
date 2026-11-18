# Run 9 · low only. Same 12 low lines as run 8 and the same clean-normal reference (run7_grey).
LINES = ['m3xl46', 'm3xl42', 'm3xl29', 'm3xl67', 'm3xl25', 'm3xl08', 'm4g19l', 'm3xl57', 'm4l03', 'm3l63', 'm3l10', 'm3l62']
REF = {'artic': 4.2075, 'lufs': -27.388, 'f0_med': 10.970500000000001, 'f0_sd': 2.0309999999999997, 'h1h2': 7.1315, 'slope': -0.7204999999999999, 'int_drop': -3.503, 'final_drop': -1.3359999999999999}
# Context: the mentor-approved low take run7_five low_01 (speed -52%, -4.1 dB, breathiness +10.8 dB), given as a turn she has
# already spoken (its text + its own audio codes), so the model continues in that delivery. It is not generated, unlike a lead-in.
CTX = {"file": "ctx_low_01.mp3", "text": "Oh… you're back."}
# Arms (user OK 18 Nov 08:58: "A plus sigh"): C control, S <sigh> before the line, A approved low clip as context, AS both.
ARMS = {"C": dict(ctx=False, sigh=False), "S": dict(ctx=False, sigh=True), "A": dict(ctx=True, sigh=False), "AS": dict(ctx=True, sigh=True)}
