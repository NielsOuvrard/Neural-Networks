#!/bin/bash

# Define the range of hyperparameters to search
layers=( "64 10 10 1" "64 12 12 1" "64 14 14 1" "64 16 16 1" "64 18 18 1" "64 20 20 1" "64 22 22 1" "64 24 24 1" "64 26 26 1" "64 28 28 1" "64 30 30 1" "64 32 32 1" "64 34 34 1" "64 36 36 1" "64 38 38 1" "64 40 40 1" "64 42 42 1" "64 44 44 1" "64 46 46 1" "64 48 48 1" "64 50 50 1" "64 52 52 1" "64 54 54 1" "64 56 56 1" "64 58 58 1" "64 60 60 1" "64 62 62 1" "64 64 64 1" )

best_accuracy=0


for layer in "${layers[@]}"; do
    echo "Training : $layer"
    ./my_torch --new $layer --train --save save.json all_10.json

    echo "Testing  : $layer"
    ./my_torch --load save.json --predict last_10.json > result.txt

    # Read the result
    result=$(cat result.txt)

    echo "Architecture: $layer, Result: $result"

    # Extract accuracy from the result
    accuracy=$(echo "$result" | awk '{print $NF}')

    # Compare accuracy with the best so far
    if (( $(echo "$accuracy > $best_accuracy" | bc -l) )); then
        best_accuracy=$accuracy
        best_layer=$layer
        best_learning_rate=$learning_rate
        best_epoch=$epoch
    fi
done

# Print the best hyperparameters and accuracy
echo "Best Hyperparameters:"
echo "Hidden Layers: $best_layer"
echo "Learning Rate: $best_learning_rate"
echo "Epochs: $best_epoch"
echo "Best Accuracy: $best_accuracy"
