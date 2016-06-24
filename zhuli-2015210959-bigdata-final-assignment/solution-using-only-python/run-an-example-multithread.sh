#!/usr/bin/env bash

# Do some cleanup first
rm $INPUT1 $INPUT2 $OUTPUT_MULTITHREAD

echo "Generating random dataset 1 with $N records."
./generate-random-dataset.py $N >$INPUT1
echo "Generating random dataset 1 with $N records."
./generate-random-dataset.py $N >$INPUT2
echo "Computing their pairwise Jaccard similarity."
./jaccard-similarity-multithread.py $INPUT1 $INPUT2 $THRESHOLD >$OUTPUT_MULTITHREAD
echo "The final result is in the file \"$OUTPUT_MULTITHREAD\"."

