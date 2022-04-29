#!/bin/bash

# Process several directories and output Markdown docs.
# Then create a static website of those docs using the 
# static website generator MkDocs and upload the site.
#
# Usage: 
# Make sure you are in this repo directory then run:
#   ./update_ddc_site.sh

# Catalog the README.yaml files in the following directories.
sudo true
./ddc.py /shared                            > docs/shared.md
./ddc.py /shared/eresearch                  > docs/shared_eresearch.md
./ddc.py /shared/eresearch/pbs_job_examples > docs/shared_eresearch_pbs_job_examples.md
./ddc.py /shared/opt/                       > docs/shared_opt.md

# Build the website.
source ~/virtualenvs/mkdocs3/bin/activate
mkdocs build

# If you wish to use --delete do not use "site/*" use "site/". Man rsync for why.
rsync -r --delete site/ /var/www/html_ddc/ 

