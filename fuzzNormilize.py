import atheris
import sys
import os
import time
from django.utils.regex_helper import normalize

atheris.instrument_all()

CRASH_DIR = "crashes"
os.makedirs(CRASH_DIR, exist_ok=True)

MAX_CRASHES = 300
CRASH_COUNTER = 0

def save_crash(s):
    ts = str(time.time()).replace('.', '')
    fname = os.path.join(CRASH_DIR, f"crash-{ts}.txt")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(s)
    print("CRASH SAVED:", fname)

def TestOneInput(data):
    global CRASH_COUNTER
    if CRASH_COUNTER >= MAX_CRASHES:
        sys.exit(0)

    try:
        s = data.decode("utf-8", errors="ignore")
    except Exception:
        return

    try:
        normalize(s)
    except (ValueError, NotImplementedError):
        return
    except Exception:
        save_crash(s)
        CRASH_COUNTER += 1
        return

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
