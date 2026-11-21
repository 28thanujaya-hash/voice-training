# run26 · IndexTTS2 in tara's voice, sad settings (recipe in pilot.py)

status PASS here = right words only (judge decides the mood)

```
[  0.0 min] $ ffmpeg -loglevel error -y -i spk_tara.mp3 -ar 24000 -ac 1 spk_tara.wav && ffmpeg -loglevel error -y -i emo_sad.mp3 -ar 24000 -ac 1 emo_sad.wav
[  0.0 min] $ git clone -q --depth 1 https://github.com/index-tts/index-tts.git /tmp/itts && cd /tmp/itts && git lfs pull 2>/dev/null; true
[  0.1 min] $ pip install -q -U uv 'huggingface_hub[cli]'
[  0.2 min] $ uv sync
[  4.0 min] $ python -c "from huggingface_hub import snapshot_download; snapshot_download('IndexTeam/IndexTTS-2', local_dir='/tmp/itts/checkpoints_2')"
[  4.5 min] $ PYTHONPATH=. uv run python gen.py
[ 23.9 min] generation done: 128 ok, 0 failed
[ 23.9 min] $ pip install -q 'transformers==4.57.6' jiwer librosa soundfile
[ 25.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_N_0.wav -b:a 96k /kaggle/working/takes/m3l50_N_0.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_N_1.wav -b:a 96k /kaggle/working/takes/m3l50_N_1.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_N_2.wav -b:a 96k /kaggle/working/takes/m3l50_N_2.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_N_3.wav -b:a 96k /kaggle/working/takes/m3l50_N_3.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_SAD_0.wav -b:a 96k /kaggle/working/takes/m3l50_SAD_0.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_SAD_1.wav -b:a 96k /kaggle/working/takes/m3l50_SAD_1.mp3
[ 25.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_SAD_2.wav -b:a 96k /kaggle/working/takes/m3l50_SAD_2.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_SAD_3.wav -b:a 96k /kaggle/working/takes/m3l50_SAD_3.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_MEL_0.wav -b:a 96k /kaggle/working/takes/m3l50_MEL_0.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_MEL_1.wav -b:a 96k /kaggle/working/takes/m3l50_MEL_1.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_MEL_2.wav -b:a 96k /kaggle/working/takes/m3l50_MEL_2.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_MEL_3.wav -b:a 96k /kaggle/working/takes/m3l50_MEL_3.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_EA_0.wav -b:a 96k /kaggle/working/takes/m3l50_EA_0.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_EA_1.wav -b:a 96k /kaggle/working/takes/m3l50_EA_1.mp3
[ 25.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_EA_2.wav -b:a 96k /kaggle/working/takes/m3l50_EA_2.mp3
[ 25.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l50_EA_3.wav -b:a 96k /kaggle/working/takes/m3l50_EA_3.mp3
[ 25.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_N_0.wav -b:a 96k /kaggle/working/takes/m3l10_N_0.mp3
[ 25.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_N_1.wav -b:a 96k /kaggle/working/takes/m3l10_N_1.mp3
[ 25.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_N_2.wav -b:a 96k /kaggle/working/takes/m3l10_N_2.mp3
[ 25.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_N_3.wav -b:a 96k /kaggle/working/takes/m3l10_N_3.mp3
[ 25.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_SAD_0.wav -b:a 96k /kaggle/working/takes/m3l10_SAD_0.mp3
[ 25.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_SAD_1.wav -b:a 96k /kaggle/working/takes/m3l10_SAD_1.mp3
[ 25.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_SAD_2.wav -b:a 96k /kaggle/working/takes/m3l10_SAD_2.mp3
[ 25.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_SAD_3.wav -b:a 96k /kaggle/working/takes/m3l10_SAD_3.mp3
[ 25.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_MEL_0.wav -b:a 96k /kaggle/working/takes/m3l10_MEL_0.mp3
[ 25.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_MEL_1.wav -b:a 96k /kaggle/working/takes/m3l10_MEL_1.mp3
[ 25.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_MEL_2.wav -b:a 96k /kaggle/working/takes/m3l10_MEL_2.mp3
[ 25.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_MEL_3.wav -b:a 96k /kaggle/working/takes/m3l10_MEL_3.mp3
[ 25.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_EA_0.wav -b:a 96k /kaggle/working/takes/m3l10_EA_0.mp3
[ 25.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_EA_1.wav -b:a 96k /kaggle/working/takes/m3l10_EA_1.mp3
[ 25.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_EA_2.wav -b:a 96k /kaggle/working/takes/m3l10_EA_2.mp3
[ 25.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l10_EA_3.wav -b:a 96k /kaggle/working/takes/m3l10_EA_3.mp3
[ 25.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_N_0.wav -b:a 96k /kaggle/working/takes/m3l22_N_0.mp3
[ 25.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_N_1.wav -b:a 96k /kaggle/working/takes/m3l22_N_1.mp3
[ 25.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_N_2.wav -b:a 96k /kaggle/working/takes/m3l22_N_2.mp3
[ 25.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_N_3.wav -b:a 96k /kaggle/working/takes/m3l22_N_3.mp3
[ 25.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_SAD_0.wav -b:a 96k /kaggle/working/takes/m3l22_SAD_0.mp3
[ 25.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_SAD_1.wav -b:a 96k /kaggle/working/takes/m3l22_SAD_1.mp3
[ 25.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_SAD_2.wav -b:a 96k /kaggle/working/takes/m3l22_SAD_2.mp3
[ 25.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_SAD_3.wav -b:a 96k /kaggle/working/takes/m3l22_SAD_3.mp3
[ 25.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_MEL_0.wav -b:a 96k /kaggle/working/takes/m3l22_MEL_0.mp3
[ 25.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_MEL_1.wav -b:a 96k /kaggle/working/takes/m3l22_MEL_1.mp3
[ 25.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_MEL_2.wav -b:a 96k /kaggle/working/takes/m3l22_MEL_2.mp3
[ 25.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_MEL_3.wav -b:a 96k /kaggle/working/takes/m3l22_MEL_3.mp3
[ 25.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_EA_0.wav -b:a 96k /kaggle/working/takes/m3l22_EA_0.mp3
[ 25.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_EA_1.wav -b:a 96k /kaggle/working/takes/m3l22_EA_1.mp3
[ 25.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_EA_2.wav -b:a 96k /kaggle/working/takes/m3l22_EA_2.mp3
[ 25.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l22_EA_3.wav -b:a 96k /kaggle/working/takes/m3l22_EA_3.mp3
[ 25.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_N_0.wav -b:a 96k /kaggle/working/takes/m3l23_N_0.mp3
[ 25.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_N_1.wav -b:a 96k /kaggle/working/takes/m3l23_N_1.mp3
[ 25.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_N_2.wav -b:a 96k /kaggle/working/takes/m3l23_N_2.mp3
[ 25.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_N_3.wav -b:a 96k /kaggle/working/takes/m3l23_N_3.mp3
[ 25.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_SAD_0.wav -b:a 96k /kaggle/working/takes/m3l23_SAD_0.mp3
[ 25.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_SAD_1.wav -b:a 96k /kaggle/working/takes/m3l23_SAD_1.mp3
[ 25.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_SAD_2.wav -b:a 96k /kaggle/working/takes/m3l23_SAD_2.mp3
[ 25.9 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_SAD_3.wav -b:a 96k /kaggle/working/takes/m3l23_SAD_3.mp3
[ 25.9 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_MEL_0.wav -b:a 96k /kaggle/working/takes/m3l23_MEL_0.mp3
[ 25.9 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_MEL_1.wav -b:a 96k /kaggle/working/takes/m3l23_MEL_1.mp3
[ 25.9 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_MEL_2.wav -b:a 96k /kaggle/working/takes/m3l23_MEL_2.mp3
[ 25.9 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_MEL_3.wav -b:a 96k /kaggle/working/takes/m3l23_MEL_3.mp3
[ 25.9 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_EA_0.wav -b:a 96k /kaggle/working/takes/m3l23_EA_0.mp3
[ 25.9 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_EA_1.wav -b:a 96k /kaggle/working/takes/m3l23_EA_1.mp3
[ 26.0 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_EA_2.wav -b:a 96k /kaggle/working/takes/m3l23_EA_2.mp3
[ 26.0 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l23_EA_3.wav -b:a 96k /kaggle/working/takes/m3l23_EA_3.mp3
[ 26.0 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_N_0.wav -b:a 96k /kaggle/working/takes/m3l49_N_0.mp3
[ 26.0 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_N_1.wav -b:a 96k /kaggle/working/takes/m3l49_N_1.mp3
[ 26.0 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_N_2.wav -b:a 96k /kaggle/working/takes/m3l49_N_2.mp3
[ 26.0 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_N_3.wav -b:a 96k /kaggle/working/takes/m3l49_N_3.mp3
[ 26.0 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_SAD_0.wav -b:a 96k /kaggle/working/takes/m3l49_SAD_0.mp3
[ 26.0 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_SAD_1.wav -b:a 96k /kaggle/working/takes/m3l49_SAD_1.mp3
[ 26.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_SAD_2.wav -b:a 96k /kaggle/working/takes/m3l49_SAD_2.mp3
[ 26.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_SAD_3.wav -b:a 96k /kaggle/working/takes/m3l49_SAD_3.mp3
[ 26.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_MEL_0.wav -b:a 96k /kaggle/working/takes/m3l49_MEL_0.mp3
[ 26.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_MEL_1.wav -b:a 96k /kaggle/working/takes/m3l49_MEL_1.mp3
[ 26.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_MEL_2.wav -b:a 96k /kaggle/working/takes/m3l49_MEL_2.mp3
[ 26.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_MEL_3.wav -b:a 96k /kaggle/working/takes/m3l49_MEL_3.mp3
[ 26.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_EA_0.wav -b:a 96k /kaggle/working/takes/m3l49_EA_0.mp3
[ 26.1 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_EA_1.wav -b:a 96k /kaggle/working/takes/m3l49_EA_1.mp3
[ 26.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_EA_2.wav -b:a 96k /kaggle/working/takes/m3l49_EA_2.mp3
[ 26.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l49_EA_3.wav -b:a 96k /kaggle/working/takes/m3l49_EA_3.mp3
[ 26.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_N_0.wav -b:a 96k /kaggle/working/takes/m3l56_N_0.mp3
[ 26.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_N_1.wav -b:a 96k /kaggle/working/takes/m3l56_N_1.mp3
[ 26.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_N_2.wav -b:a 96k /kaggle/working/takes/m3l56_N_2.mp3
[ 26.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_N_3.wav -b:a 96k /kaggle/working/takes/m3l56_N_3.mp3
[ 26.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_SAD_0.wav -b:a 96k /kaggle/working/takes/m3l56_SAD_0.mp3
[ 26.2 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_SAD_1.wav -b:a 96k /kaggle/working/takes/m3l56_SAD_1.mp3
[ 26.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_SAD_2.wav -b:a 96k /kaggle/working/takes/m3l56_SAD_2.mp3
[ 26.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_SAD_3.wav -b:a 96k /kaggle/working/takes/m3l56_SAD_3.mp3
[ 26.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_MEL_0.wav -b:a 96k /kaggle/working/takes/m3l56_MEL_0.mp3
[ 26.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_MEL_1.wav -b:a 96k /kaggle/working/takes/m3l56_MEL_1.mp3
[ 26.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_MEL_2.wav -b:a 96k /kaggle/working/takes/m3l56_MEL_2.mp3
[ 26.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_MEL_3.wav -b:a 96k /kaggle/working/takes/m3l56_MEL_3.mp3
[ 26.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_EA_0.wav -b:a 96k /kaggle/working/takes/m3l56_EA_0.mp3
[ 26.3 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_EA_1.wav -b:a 96k /kaggle/working/takes/m3l56_EA_1.mp3
[ 26.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_EA_2.wav -b:a 96k /kaggle/working/takes/m3l56_EA_2.mp3
[ 26.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l56_EA_3.wav -b:a 96k /kaggle/working/takes/m3l56_EA_3.mp3
[ 26.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_N_0.wav -b:a 96k /kaggle/working/takes/m3l66_N_0.mp3
[ 26.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_N_1.wav -b:a 96k /kaggle/working/takes/m3l66_N_1.mp3
[ 26.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_N_2.wav -b:a 96k /kaggle/working/takes/m3l66_N_2.mp3
[ 26.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_N_3.wav -b:a 96k /kaggle/working/takes/m3l66_N_3.mp3
[ 26.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_SAD_0.wav -b:a 96k /kaggle/working/takes/m3l66_SAD_0.mp3
[ 26.4 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_SAD_1.wav -b:a 96k /kaggle/working/takes/m3l66_SAD_1.mp3
[ 26.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_SAD_2.wav -b:a 96k /kaggle/working/takes/m3l66_SAD_2.mp3
[ 26.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_SAD_3.wav -b:a 96k /kaggle/working/takes/m3l66_SAD_3.mp3
[ 26.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_MEL_0.wav -b:a 96k /kaggle/working/takes/m3l66_MEL_0.mp3
[ 26.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_MEL_1.wav -b:a 96k /kaggle/working/takes/m3l66_MEL_1.mp3
[ 26.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_MEL_2.wav -b:a 96k /kaggle/working/takes/m3l66_MEL_2.mp3
[ 26.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_MEL_3.wav -b:a 96k /kaggle/working/takes/m3l66_MEL_3.mp3
[ 26.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_EA_0.wav -b:a 96k /kaggle/working/takes/m3l66_EA_0.mp3
[ 26.5 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_EA_1.wav -b:a 96k /kaggle/working/takes/m3l66_EA_1.mp3
[ 26.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_EA_2.wav -b:a 96k /kaggle/working/takes/m3l66_EA_2.mp3
[ 26.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l66_EA_3.wav -b:a 96k /kaggle/working/takes/m3l66_EA_3.mp3
[ 26.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_N_0.wav -b:a 96k /kaggle/working/takes/m3l32_N_0.mp3
[ 26.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_N_1.wav -b:a 96k /kaggle/working/takes/m3l32_N_1.mp3
[ 26.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_N_2.wav -b:a 96k /kaggle/working/takes/m3l32_N_2.mp3
[ 26.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_N_3.wav -b:a 96k /kaggle/working/takes/m3l32_N_3.mp3
[ 26.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_SAD_0.wav -b:a 96k /kaggle/working/takes/m3l32_SAD_0.mp3
[ 26.6 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_SAD_1.wav -b:a 96k /kaggle/working/takes/m3l32_SAD_1.mp3
[ 26.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_SAD_2.wav -b:a 96k /kaggle/working/takes/m3l32_SAD_2.mp3
[ 26.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_SAD_3.wav -b:a 96k /kaggle/working/takes/m3l32_SAD_3.mp3
[ 26.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_MEL_0.wav -b:a 96k /kaggle/working/takes/m3l32_MEL_0.mp3
[ 26.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_MEL_1.wav -b:a 96k /kaggle/working/takes/m3l32_MEL_1.mp3
[ 26.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_MEL_2.wav -b:a 96k /kaggle/working/takes/m3l32_MEL_2.mp3
[ 26.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_MEL_3.wav -b:a 96k /kaggle/working/takes/m3l32_MEL_3.mp3
[ 26.7 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_EA_0.wav -b:a 96k /kaggle/working/takes/m3l32_EA_0.mp3
[ 26.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_EA_1.wav -b:a 96k /kaggle/working/takes/m3l32_EA_1.mp3
[ 26.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_EA_2.wav -b:a 96k /kaggle/working/takes/m3l32_EA_2.mp3
[ 26.8 min] $ ffmpeg -loglevel error -y -i /kaggle/working/raw_m3l32_EA_3.wav -b:a 96k /kaggle/working/takes/m3l32_EA_3.mp3
[ 26.8 min] 128 takes, 75 with right words
```
