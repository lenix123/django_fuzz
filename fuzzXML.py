import atheris
import sys
import django
from django.conf import settings
from xml.dom import minidom
from io import StringIO
from django.core.serializers.xml_serializer import Deserializer as XMLDeserializer
from django.core import serializers
from django.db import models

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
    try:
        xml_str = data.decode("utf-8", errors="ignore")
    except:
        return

    try:
        doc = minidom.parseString(xml_str)
    except:
        return

    objects = doc.getElementsByTagName("object")
    if not objects:
        return

    des = XMLDeserializer(StringIO(xml_str), using="default", ignorenonexistent=False)

    try:
        for obj_node in objects:
            des._handle_object(obj_node)
    except:
        pass

def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, TestOneInput, custom_corpus_dirs=["./corpus_xml"])
    atheris.Fuzz()

if __name__ == "__main__":
    main()
