# Run 1 · stage 2: Kokoro retraining (smoke run)

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 17 lines; e.g. So, how was your weekend? Did you do anything fun? → sˌO, hˌW wʌz jʊɹ wˈikˌɛnd? dˈɪd ju dˈu ˈɛniθˌɪŋ fˈʌn? |
| recipe + tools installed | ✅ |  |
| Kokoro base weights converted | ✅ |  |
| Kokoro stage 1 (acoustic) | ✅ | 1.9 min, GPU peak 0.0 GB |
| Kokoro stage 2 (prosody + adversarial) | ✅ | 2.2 min |
| voicepacks (Sam, Maya) | ✅ |  |
| retrained Kokoro speaks (Sam, Maya) | ✅ |  |

## What the retrained Kokoro said (Whisper)

- sam: “Hey! How was your day? Did you watch the match?” → heard “Hey, how was your day? Did you watch the match?” (3.5 s)
- sam: “Oh no… I'm so sorry. That's really sad.” → heard “Oh no. I'm so sorry. That's really sad.” (3.6 s)
- maya: “Hmm, interesting. Tell me more about it.” → heard “Hmm, interesting. Tell me more about it.” (2.8 s)
- maya: “Wait, really? I didn't know that!” → heard “Wait, really? I didn't know that.” (2.6 s)

RESULT: PASS

## Log
```
[  0.0 min] stage-1 clips: 17 kept, from /kaggle/input/notebooks/thusharajayawardane/se-run1-record
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.0 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.2 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.2 min] STEP words → sounds (misaki-g2p): OK 17 lines; e.g. So, how was your weekend? Did you do anything fun? → sˌO, hˌW wʌz jʊɹ wˈikˌɛnd? dˈɪd ju dˈu ˈɛniθˌɪŋ fˈʌn?
[  0.2 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.4 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile
[  0.5 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.2 min] torch 2.11.0+cu130, GPUs 2
[  1.2 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.2 min] STEP recipe + tools installed: OK 
[  1.3 min] STEP Kokoro base weights converted: OK 
[  1.3 min] $ python train_first.py --config_path /kaggle/tmp/kt/configs/run1.yml
[  3.2 min] STEP Kokoro stage 1 (acoustic): OK 1.9 min, GPU peak 0.0 GB
[  3.2 min] $ python train_second.py --config_path /kaggle/tmp/kt/configs/run1.yml
[  5.4 min] STEP Kokoro stage 2 (prosody + adversarial): OK 2.2 min
[  5.4 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run1/epoch_2nd_00001.pth --style-encoder-model /kaggle/tmp/logs/run1/epoch_1st_00001.pth --audio-di
[  5.6 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/run1/epoch_2nd_00001.pth --style-encoder-model /kaggle/tmp/logs/run1/epoch_1st_00001.pth --audio-di
[  5.7 min] STEP voicepacks (Sam, Maya): OK 
[  5.8 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[  6.3 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/l.wav -b:a 64k /kaggle/working/run1_kokoro_listen.mp3
[  6.3 min] STEP retrained Kokoro speaks (Sam, Maya): OK 
```
