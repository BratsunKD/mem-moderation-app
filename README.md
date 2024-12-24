# text-moderation-app

Система автоматической модерации текста

### 


### Запуск приложение

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
