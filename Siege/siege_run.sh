#!/bin/bash


get_file="test_search.txt"
post_prop_file="urls_property_create.txt"
post_rev_file="urls_review_create.txt"


start=200
stop=2000
step=200


mkdir -p logs

for n in $(seq $start $step $stop); do
    echo "=== TEST GET (public) przy -c $n ==="
    siege -f "$get_file" -c"$n" -t60S \
          --log="logs/log_search_${n}.log" \
          --benchmark
    sleep 5

    echo "=== TEST POST property/create przy -c $n ==="
    siege -f "$post_prop_file" -c"$n" -t60S \
          -H "Authorization: Token b639e41441c31dd4c9dfb67995c0645cab18e3bd" \
          -H "Content-Type: application/json" \
          --log="logs/log_property_create_${n}.log" \
          --benchmark
    sleep 5

    echo "=== TEST POST review/create przy -c $n ==="
    siege -f "$post_rev_file" -c"$n" -t60S \
          -H "Authorization: Token b639e41441c31dd4c9dfb67995c0645cab18e3bd" \
          -H "Content-Type: application/json" \
          --log="logs/log_review_create_${n}.log" \
          --benchmark
    sleep 5

    echo ""
done

