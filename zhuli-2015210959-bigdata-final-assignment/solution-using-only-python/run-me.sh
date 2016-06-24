#!/usr/bin/env bash
#Here is an example, the parameters here can be modified as you see fit.
source ./env.sh

echo "Running single-thread example:"
time ./run-an-example.sh
echo "Running multithread example:"
time ./run-an-example-multithread.sh

