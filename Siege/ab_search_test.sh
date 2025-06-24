#!/bin/bash

# Ustaw jeden, reprezentatywny URL do testowania
TEST_URL="http://127.0.0.1:8000/api/property/search/?city=Warszawa&region=Mazowieckie&maxP=330"

# Ustaw czas trwania każdego testu w sekundach
TIME_LIMIT=60

# Ustaw poziomy współbieżności (ilość jednoczesnych klientów)
# Możesz ustawić nawet na 2000, aby zobaczyć, w którym momencie system przestaje być stabilny
START_CONCURRENCY=200
STOP_CONCURRENCY=4000
STEP=200

# Utwórz katalog na logi z testów AB
mkdir -p logs_ab

echo "==============================================="
echo " Rozpoczynam testy wydajności GET za pomocą AB "
echo " URL: $TEST_URL"
echo " Czas trwania każdego testu: ${TIME_LIMIT}s"
echo "==============================================="
echo ""

# Pętla testująca różne poziomy współbieżności
for n in $(seq $START_CONCURRENCY $STEP $STOP_CONCURRENCY); do
    echo "=== TEST AB przy -c $n (współbieżność) przez -t $TIME_LIMIT sekund ==="

    # Pamiętaj, aby w tym terminalu podnieść limit otwartych plików!
    # ulimit -n 4096

    # Uruchomienie Apache Benchmark i zapisanie wyniku do pliku logu
    ab -t $TIME_LIMIT -c "$n" "$TEST_URL" > "logs_ab/log_search_ab_${n}.log" 2>&1

    # Sprawdzamy, czy w logu nie ma informacji o błędach
    echo "Wyniki zapisane w: logs_ab/log_search_ab_${n}.log"
    # Wyświetlamy kluczowe metryki
    grep "Requests per second" "logs_ab/log_search_ab_${n}.log"
    grep "Failed requests" "logs_ab/log_search_ab_${n}.log"

    echo "Czekam 5 sekund przed następnym testem..."
    sleep 5
    echo ""
done

echo "Wszystkie testy AB zakończone."