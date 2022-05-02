#!/bin/bash

input="example.md"
output="example.html"

# This requires pandoc which is installed on the HPC.
# It also requires a styles.css to be in this directory.

# This will produce a fragment only i.e. no HTML head or footer.
#pandoc --css=styles.css $input > $output

# This will produce a standalone i.e. full HTML doc with head and footer as it uses the -s option.
# It will require the separate styles.css file.
#pandoc --css=styles.css --standalone $input > $output

# This will produce a standalone HTML doc with head and footer.
# The --self-contained option will insert the styles into the head of the HTML.
# Hence it will not require the separate styles.css file to be present.
pandoc --css=styles.css --self-contained $input > $output

# Copy to our document root.
#cp $output /var/www/html/

