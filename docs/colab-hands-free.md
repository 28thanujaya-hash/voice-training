# Keeping a free Colab GPU running with no browser tab open

How the voice-training project ran jobs on Colab's free T4 with nobody watching the screen. Written 20 Nov 2026.

## The problem

Free Colab runs code only while a browser tab is open and active. If the tab closes, the phone sleeps, or Colab thinks nobody is there, the runtime is disconnected and the work is lost. We wanted jobs to run while the user was away, started by Claude.

## The idea in one line

Replace the browser tab with a GitHub Actions machine that talks to Colab through **Google's Colab command-line tool (Colab CLI)**. It keeps the connection busy the whole time, the way an open tab would.

## The pieces

| Piece | File (voice-training repo) | What it does |
| --- | --- | --- |
| Sign-in | GitHub secret `COLAB_TOKEN` | The Colab CLI's sign-in file (JSON). Lets a machine act as the user's Colab account. A backup copy is in the user's Google Drive, named "colab-cli-token.json (Claude's Colab sign-in — do not share)". |
| One job | `.github/workflows/colab.yml` | Runs one job on Colab, from start to finish |
| Several jobs | `.github/workflows/colab_chain.yml` | Runs a list of jobs one after another and saves each as soon as it ends |
| Code sent to Colab | `.github/colab/cell.py` | Runs on the Colab machine: fetches the repo, runs the job, prints every line live, zips the results |
| Keep-alive | `.github/colab/keepalive.py` | Every 60 s, pings Colab's "keep-alive" address, as an open tab does |
| By-hand option | `kaggle/jobs/colab_run.ipynb` | A notebook the user can open and press "Run all", saving to Drive |

## What happens, step by step

1. **Claude starts it:** Claude asks GitHub to run the workflow (`gh api …/actions/workflows/colab_chain.yml/dispatches`). GitHub lends a free Linux machine for up to 6 hours.
2. **Sign in:** that machine installs the Colab CLI (`pip install google-colab-cli`) and writes the `COLAB_TOKEN` secret to `~/.config/colab-cli/token.json`.
3. **Ask for a GPU:** `colab new -s <job> --gpu T4`. If Colab says "Service Unavailable" (free limit reached), it waits 5 minutes and asks again, up to `alloc_tries` times.
4. **Keep the screen "on" in two ways at once:**
   - **Live output:** `colab exec -s <job> -f cell.py` keeps a connection open and streams every line the job prints. To Colab, someone is actively watching.
   - **Keep-alive ping:** `keepalive.py` runs alongside. Every 60 seconds it calls `https://colab.research.google.com/tun/m/<endpoint>/keep-alive/` with the account's sign-in. This is the same signal an open browser tab sends. If one method hiccups, the other still holds the session.
5. **Collect:** when the job ends, `cell.py` zips the results. The workflow downloads the zip (`colab download`), unpacks it into `results/<job>/` and commits it to the repo. If the zip is over 60 MB, the big audio files are left out.
6. **Give the GPU back:** `colab stop -s <job>`. This runs even when something failed, so the account isn't left holding a GPU.

The chain version repeats steps 3–6 for each job in the list. Before starting, it waits for any other Colab run to finish, because free Colab allows only one GPU at a time per account.

## What did not work

- **Running the Colab CLI from Claude's own workspace:** the session was silently cut after about 6 minutes. Running it from GitHub Actions solved this.
- **Retrying every 5 minutes for hours:** wasted GitHub time and never got a GPU while Colab was locked. Rule now: one round of tries, then report.

## Limits we learned

- One free Colab GPU at a time per account. A Kaggle GPU can run alongside it.
- After about 3½ hours of GPU use, Colab answers "Service Unavailable" and stays locked for up to about 24 hours. There is no visible quota or published reset time.
- A GitHub Actions job lasts at most 6 hours, so very long work is split into several jobs.
- Using a second Google account to get more GPUs breaks Colab's rules, so we don't.
- Speed seen: about 9 voice takes per minute on a T4.

## To reuse this in another project

1. Make the Colab CLI sign-in once on a computer, then save its token file as a GitHub secret named `COLAB_TOKEN`.
2. Copy `colab.yml` (or `colab_chain.yml`), `.github/colab/cell.py` and `.github/colab/keepalive.py`.
3. In `cell.py`, change the repo address and the command to run. Keep two habits: print output live (`python -u`), and write results to one folder that gets zipped.
4. Start it from GitHub (Actions tab → the workflow → Run workflow) or by the API.

## Safety

The `COLAB_TOKEN` secret gives full access to the Google account's Colab. Keep it only in GitHub secrets and the private Drive backup. Never paste it into a chat or commit it to the repo.
