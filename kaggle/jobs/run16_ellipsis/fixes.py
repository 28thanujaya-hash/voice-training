# Maya pilot line fixes, approved by the mentor 16 Nov 2026 (claude/line-review-16nov.md). Applied by the next recording job.
# DROP: ids removed from training. MOVE: id -> new mood row (same text). CHANGE: id -> new text (same row).
# ADD: new lines (id, row, text, group, split). Groups G11–G20: same words in all 4 moods.
DROP = ["m3b22",            # G2 bright "I can't believe she said that!"
        "m3l19"]            # G3 low "It's Sunday again…"
CHANGE = {"m3xb37": "See you tomorrow, then!",          # G9 bright (validation)
          "G8:low": "Oh… you're back.",                  # G8 low (topup id resolved by group+row)
          "m3t75": "Three hours late. Because of fog. Again."}
MOVE = {"m3l12": "normal", "m3l13": "normal", "m3l44": "normal", "m3l45": "normal", "m3l47": "normal", "m3l48": "normal",
        "m3t73": "normal", "m3t09": "bright"}
ADD = [("m4l01", "low", "It's Monday again…", "", "train"),
       ("m4l02", "low", "I keep reading her old messages…", "", "train"),
       ("m4l03", "low", "The house feels so empty without him.", "", "train"),
       ("m4l04", "low", "I wanted to tell her, but it was too late.", "", "train"),
       ("m4l05", "low", "Nobody even noticed I was gone.", "", "train"),
       ("m4l06", "low", "I'm just so tired of waiting.", "", "train"),
       ("m4l07", "low", "I don't think she's coming back…", "", "train")]
NEW_GROUPS = ["He called me last night", "They changed the plan", "We got the results", "I saw him at the market",
              "The letter came this morning", "She told me everything", "He finally answered", "My brother is getting married",
              "I'm going home tomorrow", "That was my last exam"]
MARK = {"normal": ".", "bright": "!", "low": "…", "tense": "."}
for i, s in enumerate(NEW_GROUPS, 11):
    for row in ("normal", "bright", "low", "tense"):
        ADD.append((f"m4g{i}{row[0]}", row, s + MARK[row], f"G{i}", "val" if i == 20 else "train"))
KEEP_MORE_TAKES = ["m3t13"]   # G1 tense "So that's IT, then." — acting weak
