#!/bin/bash
echo "Liczba linijek dla train:" >> stats.txt
wc -l data/train.csv >> stats.txt
echo "Liczba linijek dla test:" >> stats.txt
wc -l data/test.csv >> stats.txt
echo "Liczba linijek dla dev:" >> stats.txt
wc -l data/dev.csv >> stats.txt
mkdir -p data
mv stats.txt data/
