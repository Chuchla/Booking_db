#!/bin/bash


get_file="test_search.txt"
post_prop_file="urls_property_create.txt"
post_rev_file="urls_review_create.txt"


start=100
stop=100
step=100


mkdir -p logs

for n in $(seq $start $step $stop); do
    echo "=== TEST GET (public) przy -c $n ==="
    siege -f "$get_file" -c"$n" -t60S \
          --log="logs/log_search_${n}.log" \
          --benchmark
    sleep 5

    echo "=== TEST POST property/create przy -c $n ==="
    siege -f "$post_prop_file" -c"$n" -t60S \
          -H "Authorization: Token 817df68dfba4f541d7ff119a812241c6da3cf673" \
          -H "Content-Type: application/json" \
          --log="logs/log_property_create_${n}.log" \
          --benchmark
    sleep 5

    echo "=== TEST POST review/create przy -c $n ==="
    siege -f "$post_rev_file" -c"$n" -t60S \
          -H "Authorization: Token 817df68dfba4f541d7ff119a812241c6da3cf673" \
          -H "Content-Type: application/json" \
          --log="logs/log_review_create_${n}.log" \
          --benchmark
    sleep 5

    echo ""
done

