# Voice training

The M & F voice model for the Spoken English app: an Orpheus actor records the acting, a Kokoro teacher learns it, a Paradee student copies the teacher so it runs offline on the phone.

- `kaggle/jobs/<job>/` — one folder per run; `run.py` is what runs (on Kaggle, or in Colab via `colab.ipynb` where there is one)
- `results/<job>/` — reports, listening packs and logs collected from each run
- `.github/workflows/kaggle.yml` — start or collect a Kaggle job (secrets: `KAGGLE_USERNAME`, `KAGGLE_API_TOKEN`)

Moved from `spoken-english` on 18 Nov 2026 with full history; the app and the voice pack stay there.
