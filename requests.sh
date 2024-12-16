#!/bin/bash

# URL сервиса
URL="http://127.0.0.1:8000/text-moderation"

# Пример значений для параметров
TEXTS=("Hello, world!" "FastAPI is great" "Kafka and Redis integration" "Test message" "Another text message")
USER_IDS=(101 102 103 104 105)
MEM_IDS=(1 2 3 4 5)

# Цикл для отправки запросов
for i in {1..500}; do
  TEXT=${TEXTS[$RANDOM % ${#TEXTS[@]}]}    # Выбор случайного текста
  USER_ID=${USER_IDS[$RANDOM % ${#USER_IDS[@]}]}  # Случайный user_id
  MEM_ID=${MEM_IDS[$RANDOM % ${#MEM_IDS[@]}]}     # Случайный mem_id

  # Отправка POST-запроса
  curl -X POST $URL \
       -H "Content-Type: application/json" \
       -d "{\"text\": \"$TEXT\", \"user_id\": $USER_ID, \"mem_id\": $MEM_ID}" \
       -s -o /dev/null -w "Request $i: %{http_code}\n"

  echo "Sent: text=$TEXT, user_id=$USER_ID, mem_id=$MEM_ID"
done

