# Run 5 · re-record with lead-ins: normal, bright


RESULT: ERROR
```
rward
    hidden_states = decoder_layer(
        hidden_states,
    ...<5 lines>...
        **kwargs,
    )
  File "/usr/local/lib/python3.13/dist-packages/transformers/modeling_layers.py", line 94, in __call__
    return super().__call__(*args, **kwargs)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/modules/module.py", line 1779, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/modules/module.py", line 1790, in _call_impl
    return forward_call(*args, **kwargs)
  File "/usr/local/lib/python3.13/dist-packages/transformers/utils/deprecation.py", line 172, in wrapped_func
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.13/dist-packages/transformers/models/llama/modeling_llama.py", line 294, in forward
    hidden_states, _ = self.self_attn(
                       ~~~~~~~~~~~~~~^
        hidden_states=hidden_states,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        **kwargs,
        ^^^^^^^^^
    )
    ^
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/modules/module.py", line 1779, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/dist-packages/torch/nn/modules/module.py", line 1790, in _call_impl
    return forward_call(*args, **kwargs)
  File "/usr/local/lib/python3.13/dist-packages/transformers/utils/deprecation.py", line 172, in wrapped_func
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.13/dist-packages/transformers/models/llama/modeling_llama.py", line 252, in forward
    attn_output, attn_weights = attention_interface(
                                ~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<6 lines>...
        **kwargs,
        ^^^^^^^^^
    )
    ^
  File "/usr/local/lib/python3.13/dist-packages/transformers/integrations/sdpa_attention.py", line 68, in sdpa_attention_forward
    value = repeat_kv(value, module.num_key_value_groups)
  File "/usr/local/lib/python3.13/dist-packages/transformers/integrations/sdpa_attention.py", line 27, in repeat_kv
    return hidden_states.reshape(batch, num_key_value_heads * n_rep, slen, head_dim)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 282.00 MiB. GPU 0 has a total capacity of 14.56 GiB of which 280.81 MiB is free. Including non-PyTorch memory, this process has 14.29 GiB memory in use. Of the allocated memory 11.70 GiB is allocated by PyTorch, and 2.46 GiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)

```

## Log
```
[  0.0 min] $ pip install -q 'transformers==4.57.6' snac jiwer pyloudnorm soundfile librosa torchcrepe
[  1.1 min] 306 lines: normal 172, bright 134
```
