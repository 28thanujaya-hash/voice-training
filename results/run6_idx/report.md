# Run 6 · IndexTTS-2.5 diagnostic (12 sentences × 4 moods × 3 takes)

clips made 144 of 144 · words exact 133

| mood | clips | words exact |
|---|---|---|
| normal | 36 | 34 |
| bright | 36 | 33 |
| low | 36 | 32 |
| tense | 36 | 34 |

RESULT: DONE

## Log
```
[  0.0 min] reference /kaggle/input/notebooks/thusharajayawardane/se-run5-rec-a/takes/m3n42_r2.wav
[  0.0 min] $ git clone -q https://github.com/index-tts/index-tts.git /kaggle/tmp/index-tts
[  0.1 min] $ pip install -q -U uv huggingface_hub
[  0.2 min] $ uv sync
[  2.4 min] $ hf download IndexTeam/IndexTTS-2.5 --local-dir=checkpoints
[ 23.7 min] generation 144 clips in 20.7 min, exit 0
[ 23.7 min] module indextts.infer_v2_5
[ 23.7 min] init params: ['self', 'cfg_path', 'model_dir', 'use_bf16', 'device', 'use_cuda_kernel', 'use_deepspeed', 'use_accel', 'use_torch_compile', 'use_qwen_emo']
[ 23.7 min] infer params: ['spk_audio_prompt', 'text', 'output_path', 'lang', 'emo_audio_prompt', 'emo_alpha', 'emo_vector', 'use_emo_text', 'emo_text', 'use_random', 'interval_silence', 'verbose', 'max_text_tokens_per_segment', 'stream_return', 'more_segment_before', 'duration_factor', 'text_normalization', 'g
[ 23.7 min] $ pip install -q 'transformers==4.57.6' jiwer soundfile librosa
```
