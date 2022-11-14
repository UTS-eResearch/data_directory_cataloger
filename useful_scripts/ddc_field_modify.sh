#!/bin/bash

# Modify a line in all README.yaml files in the immediate subdirectories.
#
# Usage:
# 1. Copy this script to your own directory and edit the "before" and "after" fields to suit.
# 2. Change to the directory above the immediate subdirectories.
# 3. Run this script: /full_path_to/ddc_field_modify.sh

# Set the variables "before" and "after" to the full field "name: value"
# that you wish to be modified.
before='Earliest possible disposal date: 2024'
after='Earliest possible disposal date: 2026'

# You can modify the maxdepth depth to suit.
# Note: the mindepth is to ensure you don't include the README.yaml
# in this directory.
files=$(find . -mindepth 2 -maxdepth 2 -name README.yaml)
for f in $files; do
    changes=''
    # The sed will match on the "before" string at the start of the line,
    # including any trailing whitespace at the end of that line.
    changes=$(sed -i -e "s/^${before}\s*$/${after}/w /dev/stdout" -e '/^$/d' $f)

    # In the above we used a little know option to sed; using /w you can specify
    # a file that will receive the modified data. Here the file is stdout, which
    # is saved in the variable "changes". If this not empty then the file has
    # been changed.
    if [ "$changes" != "" ]; then
        echo "Changed $f"
    fi
done

