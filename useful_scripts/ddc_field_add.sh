#!/bin/bash

# Add a line to all README.yaml files in the immediate subdirectories.
# Usage:
# 1. Change to the directory above the immediate subdirectories.
# 2. Run this script: full_path_to/ddc_add_field.sh

# Set the variable "add" to the "name: value" line that you wish to add.
# Do not forget the colon. Example:
#   add="Earliest possible disposal date: 2024"
add='Minimum Retention Period: 2 years'

files=$(find . -mindepth 2 -maxdepth 2 -name README.yaml)
for f in $files; do
    grep "$add" $f > /dev/null
    if [ $? -eq 0 ]; then
        # This file already contains this line.
        continue
    fi
    echo "Added to $f"
    echo "$add" >> $f
done

