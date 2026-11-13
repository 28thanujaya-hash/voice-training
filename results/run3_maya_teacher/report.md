# Run 3 · Maya pilot (voice v0.1) · stage 2: Kokoro teacher + G2

| step | result | note |
|---|---|---|
| words → sounds (misaki-g2p) | ✅ | 291 lines |
| recipe + Kokoro base ready | ✅ | torch 2.11.0+cu130 |
| Kokoro stage 1 (acoustic) | ✅ | 10 epochs, 71.1 min |
| ERROR | ❌ |  |

```
Traceback (most recent call last):
  File "/kaggle/src/script.py", line 96, in <module>
    t = time.time(); sh(f"python train_second.py --config_path {K}/configs/run3.yml", cwd=S, tail=25)
                     ~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/kaggle/src/script.py", line 23, in sh
    if p.returncode: raise RuntimeError(f"failed ({p.returncode}): {c[:120]}\n" + "\n".join(out[-tail:]))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: failed (1): python train_second.py --config_path /kaggle/tmp/kt/configs/run3.yml
    return forward_call(*args, **kwargs)
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/parallel/data_parallel.py", line 197, in forward
    outputs = self.parallel_apply(replicas, inputs, module_kwargs)
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/parallel/data_parallel.py", line 214, in parallel_apply
    return parallel_apply(
        replicas, inputs, kwargs, self.device_ids[: len(replicas)]
    )
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/parallel/parallel_apply.py", line 144, in parallel_apply
    output.reraise()
    ~~~~~~~~~~~~~~^^
  File "/usr/local/lib/python3.13/dist-packages/torch/_utils.py", line 785, in reraise
    raise exception
torch.OutOfMemoryError: Caught OutOfMemoryError in replica 0 on device 0.
Original Traceback (most recent call last):
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/parallel/parallel_apply.py", line 114, in _worker
    output = module(*input, **kwargs)
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/modules/module.py", line 1779, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/modules/module.py", line 1790, in _call_impl
    return forward_call(*args, **kwargs)
  File "/kaggle/tmp/kt/StyleTTS2/losses.py", line 210, in forward
    floss += torch.mean(torch.abs(er - eg))
                        ~~~~~~~~~^^^^^^^^^
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 MiB. GPU 0 has a total capacity of 14.56 GiB of which 2.81 MiB is free. Including non-PyTorch memory, this process has 14.56 GiB memory in use. Of the allocated memory 13.36 GiB is allocated by PyTorch, and 598.01 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)

```

RESULT: FAIL

## Log
```
[  0.0 min] kept clips: 291 from /kaggle/input/notebooks/thusharajayawardane/se-run3-maya-rejudge
[  0.0 min] $ git clone -q --depth 1 --filter=blob:none --sparse https://github.com/elizaOS/llama.cpp -b eliza/develop-pin-ea8b3f2 llm && cd llm && git sparse-checkout set to
[  0.0 min] $ cmake -S /kaggle/tmp/llm/tools/misaki-g2p -B /kaggle/tmp/mb -DMISAKI_G2P_ESPEAK=OFF -DMISAKI_G2P_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -G 'Unix Makefiles' 
[  0.2 min] $ python /kaggle/tmp/llm/tools/misaki-g2p/convert_misaki_lexicon.py --fetch /kaggle/tmp/lexc -o /kaggle/tmp/misaki-en-us.lex
[  0.3 min] STEP words → sounds (misaki-g2p): OK 291 lines
[  0.3 min] $ git clone -q --recurse-submodules --shallow-submodules --depth 1 https://github.com/semidark/kikiri-tts kt
[  0.5 min] $ pip install -q munch einops einops-exts nltk pydub click tensorboard accelerate Cython loguru soundfile jiwer funasr modelscope
[  0.9 min] $ git clone -q https://github.com/resemble-ai/monotonic_align.git && cd monotonic_align && pip install -q .
[  1.8 min] $ pip install -q 'torchaudio==2.11.0' 2>&1 | tail -1 || true
[  1.9 min] STEP recipe + Kokoro base ready: OK torch 2.11.0+cu130
[  2.3 min] $ python train_first.py --config_path /kaggle/tmp/kt/configs/run3.yml
[ 73.3 min] STEP Kokoro stage 1 (acoustic): OK 10 epochs, 71.1 min
[ 73.3 min] $ python train_second.py --config_path /kaggle/tmp/kt/configs/run3.yml
[278.3 min] STEP ERROR: FAILED 
```
