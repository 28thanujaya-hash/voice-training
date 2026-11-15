# TextPrep (training side) — must match the app's TextPrep (Paradee.kt); 15 Nov: CAPS emphasis rule added.
# 1) times "7:45" -> "7 45"; 2) Sri Lankan names -> fixed sounds; 3) a CAPS word (2+ letters, not "I") -> its lowercase
#    pronunciation spoken alone (stressed) with the emphasis arrow ↗ in front: "the RED one" -> "the [RED](/↗ɹˈɛd/) one".
#    ↗ is in Kokoro's/Paradee's symbol table but never produced by misaki, so it is free to mean "lean on this word".
import re, subprocess
NAMES = {"Thenuka": "tˈɛnʊkə", "Kavi": "kˈʌvi", "Nimal": "nˈɪməl", "Priya": "pɹˈiə", "Galle": "ɡˈɑl", "kottu": "kˈOtu",
         "Peradeniya": "pˌɛɹədˈɛnijə",
         # provisional, not yet in the app list
         "Paati": "pˈɑti", "Paati's": "pˈɑtiz", "Madurai": "mˈɑdʊɹI", "Chennai": "ʧɛnˈI", "Jaffna": "ʤˈɑfnə"}
CAPS = re.compile(r"(?<![\w'\[])([A-Z][A-Z']*[A-Z])(?![\w'])")
def _times(t):
    def tm(m):
        h, mm = m.group(1), m.group(2)
        return f"{h} o'clock" if mm == "00" else (f"{h} oh {mm[1]}" if mm[0] == "0" else f"{h} {mm}")
    return re.sub(r"\b(\d{1,2}):(\d{2})\b", tm, t)
def _names(t):
    names = sorted(NAMES, key=len, reverse=True)
    return re.sub(r"\b(" + "|".join(map(re.escape, names)) + r")(?![\w'])", lambda m: f"[{m.group(1)}](/{NAMES[m.group(1)]}/)", t)
def g2p_raw(lines, cli, lex):
    p = subprocess.run([cli, "--lex", lex], input="\n".join(lines) + "\n", capture_output=True, text=True, check=True)
    return [l.replace(" | ", " ") for l in p.stdout.rstrip("\n").split("\n")]
def prepare_all(texts, cli, lex):
    """texts -> (prepared texts, phoneme strings). CAPS words resolved with one extra g2p pass."""
    caps = sorted({w for t in texts for w in CAPS.findall(t)})
    ph = dict(zip(caps, g2p_raw([f"[{w.lower()}](+2)" for w in caps], cli, lex))) if caps else {}
    prep = [_names(CAPS.sub(lambda m: f"[{m.group(1)}](/↗{ph[m.group(1)].strip('.,!? ')}/)", _times(t))) for t in texts]
    return prep, g2p_raw(prep, cli, lex)
