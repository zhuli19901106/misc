#!/usr/bin/env bash
echo "Running three demos of Jaccard similarity, using python scripting, hadoop and spark."
COUNT_DOWN=5
for((i=$COUNT_DOWN;i>0;--i))
do
    echo -n $i" "
    sleep 1
done
echo ""

echo "Running python demo."
cd solution-using-only-python
./run-me.sh &> log
cd ..

echo "Running hadoop demo."
cd solution-using-hadoop
./run-me.sh &> log
cd ..

echo "Running spark demo."
cd solution-using-spark
./run-me.sh &> log
cd ..

