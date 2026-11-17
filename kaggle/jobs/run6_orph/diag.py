# 12-sentence mood diagnostic (GPT review 17 Nov; sentences and lead-ins approved by the mentor 17 Nov 13:01).
# Same text in all 4 moods; no "!" or "…" in the sentences; no overlap with training/validation/test.
SENTS = [("d01", "The bus was late again this morning."), ("d02", "My cousin moved to Kandy last year."),
         ("d03", "We had rice and curry for lunch."), ("d04", "The shop closes at six on Sundays."),
         ("d05", "I got my exam results today."), ("d06", "He sold his old bike to a friend."),
         ("d07", "Did you see the message I sent?"), ("d08", "Is your sister visiting this weekend?"),
         ("d09", "Did you buy a new phone?"), ("d10", "Do you remember what he said?"),
         ("d11", "We have to be there by eight."), ("d12", "So that's what happened.")]
MOODS = ["normal", "bright", "low", "tense"]
LEAD = {"normal": "Okay, so, here's what happened today. Nothing special.",
        "bright": "Oh, I'm so happy, I have great news to tell you!",
        "low": "I'm just tired… today was a really disappointing day.",
        "tense": "No. Listen carefully. This is serious, and I mean it."}
