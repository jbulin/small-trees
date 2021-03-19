#!/bin/bash
echo "Computing core triads of size $1."
mkdir -p ./data
python python/small-trees.py core-triads $1 $2
