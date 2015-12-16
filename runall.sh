#!/bin/bash
datasets=("face" "digit")
algorithms=("perceptron" "mira" "naivebayes")
percents=(10 20 30 40 50 60 70 80 90 100)
i=1000
for d in "${datasets[@]}"
do
    for a in "${algorithms[@]}"
    do
	for p in "${percents[@]}"
	do
	    printf "python main.py --dataset %s --algorithm %s --iterations %s --percent %s\n" "$d" "$a" "$i" "$p"
	    python main.py --dataset $d --algorithm $a --iterations $i --percent $p
	done
    done
done
