#!/bin/bash

# Define file paths
MODULES_FILE="./tmp/missing_modules.txt"  # Path to the input file containing module names
RESULT_FILE="./tmp/installation_results.txt"  # Path to the output file for installation results

echo "Installing missing Python packages..."

# Check if the result file exists, create if not
if [ ! -f "$RESULT_FILE" ]; then
    touch "$RESULT_FILE"
fi

# Read each module from the file and try to install it
while read -r module; do
    echo "Installing $module..."
    pip install "$module" >> "$RESULT_FILE" 2>&1
done < "$MODULES_FILE"

echo "Installation of Python packages completed."
echo "Check the results in $RESULT_FILE."