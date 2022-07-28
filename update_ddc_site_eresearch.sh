#!/bin/bash

# Process several directories and output Markdown docs.
# Then create a static website of those docs using the 
# static website generator MkDocs and upload the site.
#
# Usage: 
# Make sure you are in this repo directory then run:
#   ./update_ddc_site.sh

# Create directory docs if it does not exist.
if [ ! -d docs ]; then mkdir docs; fi

# Catalog the README.yaml files in the following directories.
# sudo is needed here to search some directories under /shared.
sudo true
./ddc.py /shared                            > docs/shared.md
./ddc.py /shared/eresearch                  > docs/shared_eresearch.md
./ddc.py /shared/eresearch/pbs_job_examples > docs/shared_eresearch_pbs_job_examples.md
./ddc.py /shared/opt                        > docs/shared_opt.md
./ddc.py /shared/c3                         > docs/shared_c3.md

# Build the website.
source /shared/homes/mlake/virtualenvs/mkdocs3/bin/activate
mkdocs build --config-file mkdocs_eresearch.yml

# If you wish to use --delete do not use "site/*" use "site/". Man rsync for why.
rsync -r --delete site/ /var/www/html_ddc/ 

