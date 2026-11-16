# Run 4 · step A: tense-only fine-tune (predictor only, LR 1e-5) from a re-run of teacher B

Training lists: all moods 902 entries; tense only 244 entries


RESULT: ERROR
```
Traceback (most recent call last):
  File "/kaggle/src/script.py", line 70, in <module>
    for a in (a1, a2, a3, a4, a5, a6): assert t0.count(a) == 1, f"anchor missing: {a!r}"
                                              ^^^^^^^^^^^^^^^^
AssertionError: anchor missing: '        model.predictor_encoder = copy.deepcopy(model.style_encoder)\n'

```

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6'
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer librosa torchcrepe scikit-learn
[  0.6 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.3 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
```
