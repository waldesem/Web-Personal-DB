#!/bin/bash
REQUESTS=1000
URL="http://localhost:5000/test"

start_time=$(date +%s.%N)  # Измеряем время с микросекундами

for i in $(seq 1 $REQUESTS); do
  curl -s $URL > /dev/null &
done

wait
end_time=$(date +%s.%N)

duration=$(echo "$end_time - $start_time" | bc)  # Рассчитываем точное время
rps=$(echo "scale=2; $REQUESTS / $duration" | bc)  # Делим с учётом дробей

echo "Total requests: $REQUESTS"
echo "Duration: $duration seconds"
echo "RPS: $rps"
