#!/bin/bash

# Remove a line from all README.yaml files in the immediate subdirectories.
# Usage:
# 1. Copy this script to your own directory and edit the "remove" field to suit.
# 2. Change to the directory above the immediate subdirectories.
# 3. Run this script: full_path_to/ddc_field_remove.sh

# Set the variable "remove" to the field "name" that you wish to be removed,
# The field "value" does not need to be included.
remove='Minimum Retention Period'

# You can modify the maxdepth depth to suit.
# Note: the mindepth is to ensure you don't include the README.yaml
# in this directory.
files=$(find . -mindepth 2 -maxdepth 2 -name README.yaml)
for f in $files; do
    grep "$remove" $f > /dev/null
    if [ $? -eq 0 ]; then
        # The first sed pattern will match on the "remove" string,
        # at the start of the line, and anything following!
        # The second sed pattern will remove the blank line.
        # Also, if you remove the -i you can see what would be done as a dry-run.
        sed -i -e "s/^${remove}.*$//" -e '/^$/d' $f
        echo "Removed from $f"
    fi
done

