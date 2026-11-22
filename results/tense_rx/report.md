# tense_rx · tense top-up, context + one-CAPS rewrite, no tags (26)


## ERROR
```
Traceback (most recent call last):
  File "/usr/local/lib/python3.13/dist-packages/librosa/core/audio.py", line 176, in load
    y, sr_native = __soundfile_load(path, offset, duration, dtype)
                   ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/librosa/core/audio.py", line 209, in __soundfile_load
    context = sf.SoundFile(path)
  File "/usr/local/lib/python3.13/dist-packages/soundfile.py", line 708, in __init__
    self._file = self._open(file, mode_int, closefd)
                 ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/soundfile.py", line 1296, in _open
    raise LibsndfileError(err, prefix=f"Error opening {self.name!r}: ")
soundfile.LibsndfileError: Error opening 'ctx_tense.mp3': System error.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/kaggle/src/script.py", line 100, in <module>
    CTXI = {m: turn(c['text']) + [128261, 128257] + encode(c['file']) + [128258, 128262] for m, c in CTX.items()}; log(f"context tokens: { {m: len(v) for m, v in CTXI.items()} }")
                                                    ~~~~~~^^^^^^^^^^^
  File "/kaggle/src/script.py", line 53, in encode
    y, _ = librosa.load(path, sr=24000)
           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/librosa/core/audio.py", line 184, in load
    y, sr_native = __audioread_load(path, offset, duration, dtype)
                   ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/decorator/__init__.py", line 247, in fun
    return caller(func, *(extras + args), **kw)
  File "/usr/local/lib/python3.13/dist-packages/librosa/util/decorators.py", line 63, in __wrapper
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.13/dist-packages/librosa/core/audio.py", line 240, in __audioread_load
    reader = audioread.audio_open(path)
  File "/usr/local/lib/python3.13/dist-packages/audioread/__init__.py", line 126, in audio_open
    return BackendClass(path)
  File "/usr/local/lib/python3.13/dist-packages/audioread/rawread.py", line 59, in __init__
    self._fh = open(filename, 'rb')
               ~~~~^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'ctx_tense.mp3'

```

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe praat-parselmouth cmudict num2words
[  1.2 min] device cuda:0/cuda:1
```