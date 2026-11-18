# Claude's per-line tag choices for the full F run (19 Nov). Guideline: one tag at most; none on teaching lines;
# low: <sigh> by default, none on caring questions/offers, pleading lines and shocked "?!" lines;
# bright: gasp = surprise/discovery, chuckle = happy/fond/teasing, laugh = big delight; mostly before the line,
# a few placed mid-line where a natural break is (that tag sound stays in the clip).
LOW_NONE = ["m3l09","m3l38","m3l41","m3l46","m3xl04","m3xl09","m3xl60","m3xl63","m3xl67","m3xl68",
            "m3xl25","m3xl26","m3xl27","m3xl28","m3xl29","m3xl30","m3xl31","m3xl32","m3xl33","m3xl34","m3xl71"]
G,C,LA = "<gasp>","<chuckle>","<laugh>"
BRIGHT = {
 "m3b01":LA,"m3b02":C,"m3b03":C,"m3b04":LA,"m3b05":G,"m3b06":G,"m3b07":G,"m3b08":G,"m3b09":LA,"m3b10":G,
 "m3b14":C,"m3b15":C,"m3b16":G,"m3b17":G,"m3b19":C,"m3b20":LA,"m3b21":C,"m3b23":C,"m3b24":G,"m3b25":LA,
 "m3b26":LA,"m3b27":C,"m3b28":C,"m3b29":LA,"m3b30":C,"m3b32":LA,"m3b33":C,"m3b34":C,"m3b35":LA,"m3b36":C,
 "m3b37":G,"m3b38":G,"m3b39":C,"m3b40":C,"m3b41":G,"m3b42":G,"m3b43":LA,"m3b44":G,"m3b52":C,"m3b53":LA,
 "m3b54":G,"m3b55":LA,"m3b56":C,"m3b57":LA,"m3b58":C,"m3b59":C,"m3b60":C,"m3b61":LA,"m3b62":C,"m3b64":LA,
 "m3b65":LA,"m3b66":G,"m3b68":G,"m3b69":C,"m3b70":C,"m3b72":C,"m3b73":LA,"m3b74":G,
 "m3xb01":G,"m3xb02":C,"m3xb03":LA,"m3xb04":G,"m3xb05":C,"m3xb06":G,"m3xb08":LA,"m3xb09":G,"m3xb10":G,"m3xb11":G,
 "m3xb12":C,"m3xb13":G,"m3xb14":G,"m3xb15":C,"m3xb16":G,"m3xb17":G,"m3xb18":G,"m3xb19":G,"m3xb20":G,"m3xb21":G,
 "m3xb22":G,"m3xb23":G,"m3xb24":C,"m3xb25":LA,"m3xb26":C,"m3xb27":C,"m3xb28":LA,"m3xb29":C,"m3xb30":LA,"m3xb31":C,
 "m3xb32":C,"m3xb33":G,"m3xb34":LA,"m3xb35":LA,"m3xb36":G,"m3xb37":C,"m3xb38":LA,"m3xb39":G,"m3xb40":G,"m3xb41":G,
 "m3xb42":C,"m3xb43":C,"m3xb44":G,"m3xb45":C,"m3xb46":LA,"m3xb47":G,"m3xb48":G,"m3xb49":G,
 "m4g11b":C,"m4g12b":C,"m4g13b":G,"m4g14b":G,"m4g15b":G,"m4g16b":C,"m4g17b":G,"m4g18b":LA,"m4g20b":LA}
# mid-line placements (full actor text)
BRIGHT_MID = {
 "m3b18":"Okay, Marvel wasn't bad. <chuckle> Don't tell Sam I said that!",
 "m3b67":"Okay, I'll say it: <chuckle> that film was actually really good!",
 "m3b71":"Then, just as we reached the top, the clouds opened, <gasp> and we saw everything!",
 "m3b75":"Three trains, two buses, and finally, <gasp> there it was — the sea!",
 "m3t09":"Batman doesn't need a flying suit. He's just smart. <chuckle> Stop laughing!",
 "m3xb07":"Close your eyes… <chuckle> okay, now open them!"}
# no tag (teaching praise; plain excitement as in run13): m3b11-13, m3b31, m3b45-51, m3b63, m4g19b
NORMAL_CHUCKLE = ["m3n28","m3n42","m3n48","m3n62","m3n69"]   # dry jokes
def bright_end(t):
    s = t.rstrip()
    if s.endswith(("!", "?!", '!"')): return s
    if s.endswith("?"): return s + "!"
    if s.endswith(".") or s.endswith("…"): return s[:-1] + "!"
    return s + "!"
