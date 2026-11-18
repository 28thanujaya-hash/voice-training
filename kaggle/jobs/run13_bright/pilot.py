# Run 13 · bright, no context (user 18 Nov: bright as before; tags chosen per line by situation). 12 bright lines x 3 arms x 3 takes:
#   C = the same line with "!" / "?!" turned into "." / "?" (her normal reading of it; the baseline for rel_* and the pairs)
#   B = the bright line as written, no tag
#   T = the bright line with the tag Claude picked for its most common situation (lines with no fitting tag are skipped)
LINES = {'bright': ['m3xb02', 'm3xb24', 'm3b38', 'm4g19b', 'm4g18b', 'm3b42', 'm3b70', 'm3b54', 'm3b30', 'm3b57', 'm3b31', 'm3b63']}
REF = {'artic': 4.2075, 'lufs': -27.388, 'f0_med': 10.970500000000001, 'f0_sd': 2.0309999999999997, 'h1h2': 7.1315, 'slope': -0.7204999999999999, 'int_drop': -3.503, 'final_drop': -1.3359999999999999}
TAGS = {'m3xb02': '<chuckle>',   # And the winner is… you!  (playful announcement)
        'm3xb24': '<chuckle>',   # Sam actually cooked?!  (amused disbelief)
        'm3b38': '<gasp>',       # Wow, you remembered! Thank you!  (touched surprise)
        'm4g18b': '<laugh>',     # My brother is getting married!  (delighted news)
        'm3b42': '<gasp>',       # Oh, how wonderful! When did you find out?  (surprise)
        'm3b70': '<chuckle>',    # Thank you! You really didn't have to do that!  (touched, a little shy)
        'm3b54': '<gasp>',       # ...there's a rainbow over the sea!  (wonder)
        'm3b30': '<chuckle>',    # Thenuka's getting so big! ...  (fond)
        'm3b57': '<laugh>'}      # ...I'm going to sleep for two days!  (playful)
        # no tag: m4g19b going home, m3b31 driving test, m3b63 Batman film (plain excitement)
def normal(t): return t.replace("?!", "?").replace("!", ".")
ARMS = {'bright': {'C': 'normal', 'B': 'bright', 'T': 'tag'}}
TAKES = 3
