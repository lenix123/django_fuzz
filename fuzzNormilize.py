import atheris
import sys
from django.utils.regex_helper import normalize

atheris.instrument_func(normalize)


def TestOneInput(data):
    try:
        s = data.decode("utf-8", errors="ignore")
    except Exception:
        return
    try:
        normalize(s)
    except (ValueError, NotImplementedError):
        return
    except Exception:
        print("crash with input - "+ s)


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
