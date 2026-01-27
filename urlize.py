import sys
import atheris

with atheris.instrument_imports():
     from django.utils.html import urlize



def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    word = fdp.ConsumeUnicodeNoSurrogates(200)
    autoescape = fdp.ConsumeBool()
    nofollow = fdp.ConsumeBool()
    trim_url_limit = fdp.ConsumeIntInRange(0, 200)

    urlize(
        word,
        trim_url_limit=trim_url_limit,
        nofollow=nofollow,
        autoescape=autoescape
        

    )


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
