#!/bin/bash

for i in {1..25}; do
  mkdir "day_$i"
  cp template.py "day_$i/part_1.py"
  cp template.py "day_$i/part_2.py"
  touch "day_$i/__init__.py" "day_$i/part_1.txt" "day_$i/part_1_practice.txt" "day_$i/part_2.txt" "day_$i/part_2_practice.txt" "day_$i/README.md"
done
