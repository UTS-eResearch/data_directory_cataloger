#!/bin/bash

# This takes the example.md Markdown document and converts it to a HTML page.
# This requires pandoc. It also requires a styles.css to be in this directory.

input="example.md"
output="example.html"
site="$HOME/public_html/ddc/"

# This will produce a standalone HTML doc.
# The --self-contained option will insert the styles into the head of the doc.
# Hence it will not require the separate styles.css file to be present.
pandoc --css=styles.css --self-contained $input > $output

# Copy to our document root.
if [ -d $site ]; then 
    cp $output $site
else
    echo "Unable to copy $output to $site as this directory was not found."
fi

