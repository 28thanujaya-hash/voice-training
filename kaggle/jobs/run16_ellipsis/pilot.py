# run16 (19 Nov): 5 bright lines where "…" cuts the sentence in half. A = as written (full run), K = payoff in CAPS + gasp, R = "…" removed + gasp; 4 takes. Script changes need the mentor's OK before use.
LINES = {'bright': ['m3xb47', 'm3xb48', 'm3xb42', 'm3xb02', 'm3xb40']}
REF = {'artic': 4.2075, 'lufs': -27.388, 'f0_med': 10.970500000000001, 'f0_sd': 2.0309999999999997, 'h1h2': 7.1315, 'slope': -0.7204999999999999, 'int_drop': -3.503, 'final_drop': -1.3359999999999999}
CTX = {}
ARMS = {'bright': {'A': (False, None, False), 'K': (False, None, False), 'R': (False, None, False)}}   # texts per (line, arm) in TXT
TXT = {('m3xb47', 'A'): "<gasp> It's… perfect!", ('m3xb47', 'K'): "<gasp> It's… PERFECT!", ('m3xb47', 'R'): "<gasp> It's perfect!", ('m3xb48', 'A'): '<gasp> You did… all of this?!', ('m3xb48', 'K'): '<gasp> You did… all of THIS?!', ('m3xb48', 'R'): '<gasp> You did all of this?!', ('m3xb42', 'A'): '<chuckle> And now… the best part!', ('m3xb42', 'K'): '<gasp> And now… the BEST part!', ('m3xb42', 'R'): '<gasp> And now, the best part!', ('m3xb02', 'A'): '<chuckle> And the winner is… you!', ('m3xb02', 'K'): '<gasp> And the winner is… YOU!', ('m3xb02', 'R'): '<gasp> And the winner is you!', ('m3xb40', 'A'): '<gasp> Is that… a puppy?!', ('m3xb40', 'K'): '<gasp> Is that… a PUPPY?!', ('m3xb40', 'R'): '<gasp> Is that a puppy?!'}   # keyed by (line, arm)
TAKES = 4
