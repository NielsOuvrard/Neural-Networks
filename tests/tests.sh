#!/bin/bash

# Define the range of hyperparameters to search
layers=( "64 10 10 10 10 1" "64 12 12 12 12 1" "64 14 14 14 14 1" "64 16 16 16 16 1" "64 18 18 18 18 1" "64 20 20 20 20 1" "64 22 22 22 22 1" "64 24 24 24 24 1" "64 26 26 26 26 1" "64 28 28 28 28 1" "64 30 30 30 30 1" "64 32 32 32 32 1" "64 34 34 34 34 1" "64 36 36 36 36 1" "64 38 38 38 38 1" "64 40 40 40 40 1" "64 42 42 42 42 1" "64 44 44 44 44 1" "64 46 46 46 46 1" "64 48 48 48 48 1" "64 50 50 50 50 1" "64 52 52 52 52 1" "64 54 54 54 54 1" "64 56 56 56 56 1" "64 58 58 58 58 1" "64 60 60 60 60 1" "64 62 62 62 62 1" "64 64 64 64 64 1" )

best_accuracy=0
csv_file="results.csv"

# Create or overwrite the CSV file with headers
echo "Architecture,Accuracy" > "$csv_file"

best_accuracy=0
best_layer=""
num_iterations=4

for layer in "${layers[@]}"; do
    total_accuracy=0

    for ((i=1; i<=$num_iterations; i++)); do
        echo "Iteration $i - Training : $layer"
        ./my_torch --new $layer --train --save save.json all_10.json

        echo "Iteration $i - Testing  : $layer"
        ./my_torch --load save.json --predict last_10.json > result.txt

        # Read the result
        result=$(cat result.txt)

        echo "Architecture: $layer, Result: $result"

        # Extract accuracy from the result
        accuracy=$(echo "$result" | awk '{print $NF}')
        total_accuracy=$(echo "$total_accuracy + $accuracy" | bc -l)
    done

    # Calculate average accuracy
    average_accuracy=$(echo "$total_accuracy / $num_iterations" | bc -l)

    # Append average result to CSV file
    echo "$layer,$average_accuracy" >> "$csv_file"

    echo "Average Accuracy for $layer: $average_accuracy"
done

# Print the best hyperparameters and accuracy
echo "Best Hyperparameters:"
echo "Hidden Layers: $best_layer"
echo "Best Accuracy: $best_accuracy"
