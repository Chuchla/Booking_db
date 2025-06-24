#!/bin/bash


get_file="test_search.txt"
post_prop_file="urls_property_create.txt"
post_rev_file="urls_review_create.txt"


start=100
stop=1000
step=100


mkdir -p logs

for n in $(seq $start $step $stop); do
    echo "=== TEST GET (public) przy -c $n ==="
    siege -f "$get_file" -c"$n" -t60S \
          --log="logs/log_search_${n}.log" \
          --benchmark
    sleep 5

    echo ""
done

