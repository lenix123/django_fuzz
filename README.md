# Требования для fuzzNormalize
Linux/WSL + python3.11 + coverage (для сбора покрытия)

docker build --tag=django .

## Запуск
```
python3.11 -m pip install requirements.txt

coverage run --source=django fuzzNormilize.py test_corpus/ (тут креши сохранятся)

coverage run --source=django fuzzNormilize.py test_corpus/ -atheris_runs=$(( 1 + $(ls test_corpus | wc -l) ))  (тут не сохранятся креши )

coverage html -d $SRC/out
```
## Покрытие (не в контейнере)
```
docker cp django:/src/out ./

```
В папке htmlcov файл index.html

## Креши
```
docker cp django:/src/crash* ./


Данная функция используется при обработке URL, а точнее паттернов URL. ПА заключается в том, что если подменить регулярное выражение в паттерне и передать его в приложение - высока вероятность краша.
Так же, в различных CMS, которые могут и разрабатываются на DJANGO, предоставляют возможность создания своих паттернов URL, например для вебхуков, соответсввенно неправильная регулярка = падение.
Помимо этого, URL могут храниться в БД и в случае компроментации БД, злоумышленнику ничего не стоить подменить через UPDATE некоторые URL, что в свою очередь повлечет падение.
Если URL и маршруты грузятся из файла конфигурации, то злоумышленник, как и в случае с БД, может подменить данные и вызвать сбой.



# Требования для fuzzXML

Linux/WSL + python3.11 + coverage (для сбора покрытия)

docker build --tag=django .

## Запуск
```
python3.11 -m pip install requirements.txt

coverage run --source=django fuzzXML.py  (тут креши сохранятся)
 
coverage html -d $SRC/out

## Креши
```
docker cp django:/src/crash* ./

## Покрытие (не в контейнере)
```
docker cp django:/src/out ./

```
В папке htmlcov файл index.html

По этой обертке у меня странные чувства - покрытие не увеличивавается почему-то. Мне честно пришлось прибегнуть к помощи нейронок при составлении начального корпуса (ну тяжко выдумывать XML из головы) и при настройке DJANGO, ваще не въезжаю какие аппсы там ему нужны чтоб спокойно запуститься. Мне кажется я что то явно сделал не так.