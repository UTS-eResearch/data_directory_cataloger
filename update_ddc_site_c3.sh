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
./ddc.py /shared/c3             > docs/c3.md
./ddc.py /shared/c3/apps        > docs/apps.md
./ddc.py /shared/c3/archives    > docs/archives.md
./ddc.py /shared/c3/bio_db      > docs/bio_db.md
./ddc.py /shared/c3/instruments > docs/instruments.md
#./ddc.py /shared/c3/projects    > docs/projects.md

# Build the website.
source /home/c3_admin/virtualenvs/mkdocs/bin/activate
mkdocs build --config-file mkdocs_c3.yml

# If you wish to use --delete do not use "site/*" use "site/". Man rsync for why.
rsync -r --delete site/ /var/www/c3/ 

