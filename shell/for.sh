#!/bin/bash

j=$1
for ((i = 1; i <= j; i++)); do
  touch file$i && echo file $i is ok
done

for i in {0..9}; do
  echo $i
done
