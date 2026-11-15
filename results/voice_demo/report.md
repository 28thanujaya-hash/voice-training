# Voice demo: one sentence per expression

Sounds given to the teacher:

- plain: `ˌI jˈuʒəwəli tˈAk ðə bˈʌs tə klˈæs ɪn ðə mˈɔɹnɪŋ.`
- ?: `dˈɪd ju fˈɪnəʃ jʊɹ hˈOmwˌɜɹk bəfˈɔɹ dˈɪnəɹ?`
- !: `wˌi wˈʌn ðə mˈæʧ lˈæst nˈIt!`
- …: `ˌI wˈATᵻd fɔɹ hˌɪm ˈɔl ˈivnɪŋ… bˌʌt hi nˈɛvəɹ kˈAm.`
- —: `lˈɪsᵊn tə mˌi — ju kənˈɑt lˈiv ðə dˈɔɹ ˈOpᵊn.`
- ?!: `jˌu ˈAt ðə hˈOl kˈAk bI jəɹsˈɛlf?!`
- CAPS: `ˌI sˈɛd ðə ɹˈɛd bˈæɡ, nˌɑt ðə blˈu wˈʌn.`
- CAPS with ↗: `ˌI sˈɛd ðə ↗ɹˈɛd bˈæɡ, nˌɑt ðə blˈu wˈʌn.`

RESULT: OK

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac soundfile librosa
[  2.4 min] Orpheus done
[  2.4 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-check
[  2.5 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix M
[  2.6 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  2.7 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  2.8 min] $ pip install -q munch einops einops-exts nltk pydub accelerate loguru
[  2.9 min] $ pip install -q 'torchaudio==2.11.0' || true
[  3.2 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input
[  3.7 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input
[  3.8 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input
[  3.9 min] $ python scripts/extract_voicepack.py --model /kaggle/input/notebooks/thusharajayawardane/se-run3-s2-p1/s2_part1.pth --style-encoder-model /kaggle/input
[  4.1 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[  4.3 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/d.wav -b:a 96k /kaggle/working/voice_demo.mp3
```
