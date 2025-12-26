import atheris
import sys
import django
from django.conf import settings
from xml.dom import minidom
from io import StringIO
import json
import tempfile
import os

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        USE_TZ=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        }
    )
    django.setup()

from django.core.serializers.xml_serializer import Deserializer as XMLDeserializer
from django.core import serializers
from django.db import models


class DummyModel(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField(default=dict)

    class Meta:
        app_label = 'fuzz_app'


apps = django.apps.registry.Apps()
DummyModel._meta.apps = apps
apps.all_models['fuzz_app'] = {'dummymodel': DummyModel}


def patched_get_model(model_identifier):
    if model_identifier == "fuzz_app.dummymodel":
        return DummyModel
    raise serializers.base.DeserializationError("Unknown model")


serializers.xml_serializer._get_model = patched_get_model


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    xml_str = fdp.ConsumeUnicodeNoSurrogates(4096)

    if not xml_str.strip().startswith('<?xml'):
        xml_str = f'<?xml version="1.0" encoding="utf-8"?><django-objects>{xml_str}</django-objects>'

    try:
        doc = minidom.parseString(xml_str)
    except Exception:
        return

    objects = doc.getElementsByTagName("object")
    if not objects:
        return

    des = XMLDeserializer(StringIO(xml_str), using="default", ignorenonexistent=False)

    try:
        for obj_node in objects:
            des._handle_object(obj_node)
    except Exception:
        pass


def main():
    corpus = [
        b'<?xml version="1.0"?><django-objects>'
        b'<object model="fuzz_app.dummymodel" pk="1">'
        b'<field name="name">abc</field>'
        b'<field name="data">{}</field>'
        b'</object></django-objects>',

        b'<?xml version="1.0"?><django-objects>'
        b'<object model="fuzz_app.dummymodel" pk="10">'
        b'<field name="name">x</field>'
        b'<field name="data">{"k": 1}</field>'
        b'</object></django-objects>',

        b'<?xml version="1.0"?><django-objects>'
        b'<object model="fuzz_app.dummymodel">'
        b'<field name="name">test</field>'
        b'<field name="data">"str"</field>'
        b'</object></django-objects>',

        b'<?xml version="1.0"?><django-objects>'
        b'<object model="fuzz_app.dummymodel" pk="zzz">'
        b'<field name="name"></field>'
        b'<field name="data">{"broken": ]}</field>'
        b'</object></django-objects>',

        b'<?xml version="1.0"?><django-objects>'
        b'<object model="fuzz_app.dummymodel" pk="">'
        b'<field name="data"><None/></field>'
        b'<field name="name">null test</field>'
        b'</object></django-objects>',
    ]

    corpus_dir = tempfile.mkdtemp()
    for i, data in enumerate(corpus):
        with open(os.path.join(corpus_dir, f"seed-{i}.xml"), "wb") as f:
            f.write(data)

    atheris.instrument_all()
    atheris.Setup(sys.argv, TestOneInput, custom_corpus_dirs=[corpus_dir])
    atheris.Fuzz()


if __name__ == "__main__":
    main()
