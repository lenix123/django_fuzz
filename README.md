# Fuzzing django v6.0

## Определение ПА

В качестве ПА django v6.0 выбрали функции:
1. `django.utils.regex_helper.normalize()` ([исходники]https://github.com/django/django/blob/main/django/utils/regex_helper.py) 
Данная функция используется при обработке URL, а точнее паттернов URL. ПА заключается в том, что если подменить регулярное выражение в паттерне и передать его в приложение - высока вероятность краша.
Так же, в различных CMS, которые могут и разрабатываются на DJANGO, предоставляют возможность создания своих паттернов URL, например для вебхуков, соответсввенно неправильная регулярка = падение.
Помимо этого, паттерны URL могут храниться в БД и в случае компроментации БД, злоумышленнику ничего не стоить подменить через UPDATE некоторые URL паттерны, что в свою очередь повлечет падение.
Если паттерны URL и маршруты грузятся из файла конфигурации, то злоумышленник, как и в случае с БД, может подменить данные и вызвать сбой.

2. `django.core.serializers.xml_serializer._handle_object()` ([исходники]https://github.com/django/django/blob/main/django/core/serializers/xml_serializer.py). Функция обрабатывает XML-объекты, которые могут загружаться из БД, конфигов, вручную пользователем или администратором, что в любом случае при компроменатации любого из ресурсов поступления XML файлов может привести к падению приложения/

## Подготовка окружения

Linux/WSL + python3.11 + coverage (для сбора покрытия)
```
docker build --tag=django .
```
```
docker run -it django
```

## Запуск фаззинга

### normalize()
```
coverage run --source=django fuzzNormilize.py ./corpus_norm/ (тут креши сохранятся)

coverage run --source=django fuzzNormilize.py ./corpus_norm/ -atheris_runs=$(( 1 + $(ls corpus_norm | wc -l) ))  (тут не сохранятся креши )

coverage html -d $SRC/out_normalize
```
#### Покрытие (не в контейнере)
```
docker cp django:/src/out_normalize ./
```
В папке htmlcov файл index.html

# СБРОС ПОКРЫТИЯ
```
rm -f .coverage
```


### _handle_object()
```

coverage run --source=django fuzzXML.py  ./corpus_xml

coverage run --source=django fuzzXML.py ./corpus_xml/ -atheris_runs=$(( 1 + $(ls corpus_xml | wc -l) ))  (тут не сохранятся креши )
 
coverage html -d $SRC/out_xml
```
#### Покрытие (не в контейнере)
```
docker cp django:/src/out_xml ./
```
В папке htmlcov файл index.html
