# Pings the Colab tunnel every 60 s while the job runs, as an open browser tab would (belt and braces next to the live exec).
import json, os, sys, time, requests
from colab_cli.auth import get_credentials
from google.auth.transport.requests import Request
name = sys.argv[1]
creds = get_credentials(os.path.expanduser("~/.colab-cli-oauth-config.json"), provider="oauth2")
while True:
    try:
        ep = json.load(open(os.path.expanduser("~/.config/colab-cli/sessions.json")))[name]["endpoint"]
        if not creds.valid: creds.refresh(Request())
        r = requests.get(f"https://colab.research.google.com/tun/m/{ep}/keep-alive/", timeout=10,
                         headers={"Authorization": f"Bearer {creds.token}", "X-Colab-Tunnel": "Google"})
        print(time.strftime("%H:%M"), "keep-alive", r.status_code, flush=True)
    except requests.exceptions.ReadTimeout: print(time.strftime("%H:%M"), "keep-alive (timeout = ok)", flush=True)
    except Exception as e: print(time.strftime("%H:%M"), "keep-alive error:", str(e)[:120], flush=True)
    time.sleep(60)
