#!/usr/bin/env bash

# Do some cleanup first
rm -rf $INPUT1 $INPUT2 $INPUT_WLN1 $INPUT_WLN2
hadoop fs -rm -r -f $PAIRS
hadoop fs -rm -r -f $OUTPUT

echo "Generatng random dataset 1 with $N records."
time ./generate-random-dataset.py $N >$INPUT1
echo "Add line numbers for dataset 1."
time ./add-line-number.py $INPUT1 >$INPUT_WLN1
echo "Generatng random dataset 2 with $N records."
time ./generate-random-dataset.py $N >$INPUT2
echo "Add line numbers for dataset 2."
time ./add-line-number.py $INPUT2 >$INPUT_WLN2
echo "Generating pairwise product for the two datasets."
time ./cartesian-product.py $INPUT_WLN1 $INPUT_WLN2> $PAIRS
time hadoop fs -put $PAIRS
echo "Running mapreduce job."
time hadoop jar jaccard-similarity.jar JaccardSimilarity $PAIRS $OUTPUT $THRESHOLD
hadoop fs -getmerge $OUTPUT $OUTPUT
# Don't know why the merged output file is marked as "executable".
chmod -x $OUTPUT
echo "The final result is in \"$OUTPUT\"."

