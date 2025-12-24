import atheris
import sys
from django.utils.regex_helper import normalize

atheris.instrument_func(normalize)


def TestOneInput(data):
    s = data.decode("utf-8", errors="ignore")
    try:
        normalize(s)
    except (ValueError, NotImplementedError):
        return
    except Exception:
        raise


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
