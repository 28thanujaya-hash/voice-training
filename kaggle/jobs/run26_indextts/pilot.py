# run26 (21 Nov): IndexTTS2 speaking in tara's voice (copied from one neutral tara take, m3n34_T_3), same 8 never-passing low lines, 4 takes.
# N = no emotion; SAD = emo_vector sad 0.8; MEL = melancholic 0.8; EA = emotion copied from a CREMA-D sad clip (judge sad 0.999), emo_alpha 0.9.
LINES = ['m3l50', 'm3l10', 'm3l22', 'm3l23', 'm3l49', 'm3l56', 'm3l66', 'm3l32']
TEXT = {'m3l50': "Priya's gone home for the weekend, so the flat's empty.", 'm3l10': 'Some nights the flat feels very quiet… and I miss Jaffna.', 'm3l22': "Appa says she's sleeping a lot… and she's not eating much.", 'm3l23': 'I looked at the bus times to Jaffna three times today.', 'm3l49': "It's been raining for three days, and I haven't seen the sun once.", 'm3l56': 'Nobody remembered my birthday this year… except Priya.', 'm3l66': 'I watched an old film tonight… the one Paati liked.', 'm3l32': "Arun asked when I'm coming home… and I didn't have an answer."}
ARMS = {'N': {}, 'SAD': {'emo_vector': [0, 0, 0.8, 0, 0, 0, 0, 0]}, 'MEL': {'emo_vector': [0, 0, 0, 0, 0, 0.8, 0, 0]}, 'EA': {'emo_audio_prompt': 'emo_sad.wav', 'emo_alpha': 0.9}}
TAKES = 4
