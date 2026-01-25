import sys
import atheris

with atheris.instrument_imports():
     from django.utils.html import Urlizer



def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    word = fdp.ConsumeUnicodeNoSurrogates(200)
    safe_input = fdp.ConsumeBool()
    autoescape = fdp.ConsumeBool()
    nofollow = fdp.ConsumeBool()
    trim_url_limit = fdp.ConsumeIntInRange(0, 200)

    Urlizer().handle_word(
        word,
        safe_input=safe_input,
        autoescape=autoescape,
        nofollow=nofollow,
        trim_url_limit=trim_url_limit,
    )


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
