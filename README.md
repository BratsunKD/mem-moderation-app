# text-moderation-app

Что надо сделать:

1) Проброс результатов web по запросу
2) Добавить модель(простенький берт) 
3) Добавить графану + провести нагрузочное тестирование


### поднять сервис

```
docker-compose build
```

```
docker-compose up
```

### запросы

Отправить текст на модерацию 
```
curl -X POST http://127.0.0.1:8000/text-moderation/ \
-H "Content-Type: application/json" \
-d '{"text": "some text", "user_id": 123, "mem_id": 3}'
```

получить результат модерации
```
curl -X POST http://127.0.0.1:8000/get-result/ \
-H "Content-Type: application/json" \
-d '{"text": "some text", "user_id": 123, "mem_id": 3}'
```

### kafka

Посмотреть список топиков(запускаем внутри контейнера с kafka)
```
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Посмотреть список топиков(запускаем внутри контейнера с kafka)
```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic input_text --from-beginning
```

```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic prediction --from-beginning
```
