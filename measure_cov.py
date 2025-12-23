from django.utils.regex_helper import normalize
import sys, os

for filename in os.listdir(sys.argv[1]):
    with open(os.path.join(sys.argv[1], filename), "rb") as f:
        s = f.read().decode("utf-8", errors="ignore")
        try:
            normalize(s)
        except Exception:
            pass
