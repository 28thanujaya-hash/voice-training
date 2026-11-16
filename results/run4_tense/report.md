# Run 4 · step A: tense-only fine-tune (predictor only, LR 1e-5) from a re-run of teacher B

Training lists: all moods 902 entries; tense only 244 entries

Phase 1 (teacher B re-run, all moods, 1 epoch): 38.4 min → s2B_full.pth (full modules, for future fine-tunes)
Phase 2 (tense only): 3 checkpoints in 14.9 min, rc 0
- ["TRAINABLE {'bert': 0, 'bert_encoder': 0, 'predictor': 16194612, 'decoder': 0, 'text_encoder': 0, 'predictor_encoder': 0, 'style_encoder': 0, 'diffusion': 0, 'text_aligner': 0, 'pitch_extractor': 0, 'mpd': 0, 'msd': 0, 'wd': 0}"]
- load: 10/10 modules clean

## The actor (training clips): normal vs tense

| | pitch level | range | pace | tilt dB |
|---|---|---|---|---|
| actor normal | 12.1 | 7.7 | 2.01 | -11.5 |
| actor tense | 11.6 | 6.9 | 1.94 | -11.0 |

Actor normal vs tense told apart from these 4 measures: 52% (chance 50%; different sentences, so words also differ)

## Teacher on the 30 matched sentences (same words, never trained on)

| voice | pitch level | range | pace | tilt dB | vs B normal: told apart | word error | naturalness | same voice as B normal |
|---|---|---|---|---|---|---|---|---|
| B normal | 11.8 | 7.2 | 2.04 | -12.4 | – | 3.1% | 4.15 | 0.967 |
| B tense | 11.9 | 6.8 | 2.03 | -12.1 | 62% | 1.8% | 4.17 | 0.964 |
| tense e1 | 11.8 | 7.2 | 2.07 | -12.0 | 55% | 4.8% | 4.15 | 0.966 |
| tense e2 | 12.1 | 7.4 | 2.09 | -12.0 | 57% | 2.2% | 4.15 | 0.963 |
| tense e3 | 12.0 | 7.5 | 2.09 | -12.0 | 65% | 1.8% | 4.16 | 0.965 |

Clips: listen/<sentence>_normal_B / _tense_B (teacher B, as before) / _tense_new (tense-only fine-tune):
- mtm01: “We're going back to the café after class.”
- mtm02: “My cousin is coming to stay for a week.”
- mtm03: “The results came out this morning.”

RESULT: DONE

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer librosa torchcrepe scikit-learn
[  0.6 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.4 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  2.2 min] $ python train_b.py --config_path /kaggle/tmp/kt/configs/b.yml  (log: train_b_log.txt)
[ 40.6 min] $ python train_m.py --config_path /kaggle/tmp/kt/configs/m.yml  (log: train_m_log.txt)
[ 55.5 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/b/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1/
[ 55.8 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/b/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1/
[ 55.9 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/m/epoch_2nd_00000.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1/
[ 56.1 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/m/epoch_2nd_00001.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1/
[ 56.2 min] $ python scripts/extract_voicepack.py --model /kaggle/tmp/logs/m/epoch_2nd_00002.pth --style-encoder-model /kaggle/input/notebooks/thusharajayawardane/se-run4-t1/
[ 56.6 min] $ pip install -q --no-deps -e /kaggle/tmp/kt/kokoro
[ 56.9 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[ 56.9 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[ 57.1 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[ 58.6 min] judged B normal
[ 59.1 min] judged B tense
[ 59.5 min] judged tense e1
[ 60.1 min] judged tense e2
[ 60.4 min] judged tense e3
[ 63.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm01_normal_B.mp3
[ 63.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm01_tense_B.mp3
[ 63.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm01_tense_new.mp3
[ 63.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm02_normal_B.mp3
[ 63.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm02_tense_B.mp3
[ 63.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm02_tense_new.mp3
[ 63.0 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm03_normal_B.mp3
[ 63.1 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm03_tense_B.mp3
[ 63.1 min] $ ffmpeg -loglevel error -y -i /kaggle/tmp/c.wav -b:a 64k /kaggle/working/listen/mtm03_tense_new.mp3
```
