# text-moderation-app

Система автоматической модерации текста

### архитектура

![system](https://github.com/user-attachments/assets/8c2dced7-3423-4e6a-a278-2b7557d89d0c)


### запуск

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
-d '{"text": "some text", "user_id": 123, "text_id": 3}'
```

получить результат модерации
```
curl -X POST http://127.0.0.1:8000/get-result/ \
-H "Content-Type: application/json" \
-d '{"text": "some text", "user_id": 123, "text_id": 3}'
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
