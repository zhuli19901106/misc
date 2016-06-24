#!/usr/bin/env bash

# Do some cleanup first
rm -rf $INPUT1 $INPUT2 $OUTPUT

echo "Generatng random dataset 1 with $N records."
time ./generate-random-dataset.py $N >$INPUT1
echo "Generatng random dataset 2 with $N records."
time ./generate-random-dataset.py $N >$INPUT2
echo "Running spark job."
time spark-submit jaccard-similarity.py $INPUT1 $INPUT2 $THRESHOLD >$OUTPUT
# Don't know why the merged output file is marked as "executable".
echo "The final result is in \"$OUTPUT\"."

