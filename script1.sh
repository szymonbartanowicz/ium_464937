#!/bin/bash
pip install kaggle
kaggle datasets download -d open-powerlifting/powerlifting-database
unzip -o powerlifting-database.zip
DATASET_FILE="openpowerlifting.csv"
column_names=$(head -n 1 $DATASET_FILE)
echo "Truncated rows: ${1}"
head -n $1 $DATASET_FILE > cutoff_$DATASET_FILE
echo "$column_names" > temp && cat cutoff_$DATASET_FILE >> temp && mv temp cutoff_$DATASET_FILE
total_lines=$(tail -n +2 cutoff_$DATASET_FILE | wc -l)
train_lines=$((total_lines * 90 / 100))
dev_lines=$((total_lines * 10 / 100))
test_lines=$((total_lines - train_lines - dev_lines))
shuf cutoff_$DATASET_FILE -o shuffled.csv
head -n $train_lines shuffled.csv > train.csv
tail -n $((dev_lines + test_lines)) shuffled.csv | head -n $dev_lines > dev.csv
tail -n $test_lines shuffled.csv > test.csv
mkdir -p data
echo "$column_names" | cat - train.csv > temp && mv temp train.csv
echo "$column_names" | cat - dev.csv > temp && mv temp dev.csv
echo "$column_names" | cat - test.csv > temp && mv temp test.csv
mv train.csv dev.csv test.csv data/
