#!/bin/bash

# This requires pandoc which is installed on the HPC.
# It also requires a styles.css to be in this directory.

#pandoc -s --css=styles.css --self-contained test.md > test.html
pandoc --css=styles.css --self-contained test.md > test.html

