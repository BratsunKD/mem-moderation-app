# meme-moderation-app

Что надо сделать: 

1) Поднять редис 
2) Добавить сервис которые берет предсказания из топика и записывает в редис
3) Этот же сервис как прослойка для редиса(?)
4) Добавить модель(простенький берт) 
5) Добавить графану + провести нагрузочное тестирование



```
docker-compose build
```

```
docker-compose up
```

```
curl -X POST http://127.0.0.1:8000/text-moderation \
-H "Content-Type: application/json" \
-d '{"text": "Hello, world!", "user_id": 123}'
```

Посмотреть список топиков(запускаем внутри контейнера с kafka)
```
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Список сообщений на конкретном топике:
```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic input_text --from-beginning
```

```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic prediction --from-beginning
```