# README

This is the data directory cataloger. The purpose of it is to help manage
numerous directories by having a README.yaml in most directories and which
stores metadata about the contents of that directory. Typical metadata that
you would store might be "Description", "Data Manager" and "Disposal Date".

When the program is run on a top level directory it looks for README.yaml files in
the **immediate** sub-directories. From those README.yaml files it reads the metadata, and
outputs a single Markdown document summarising the metadata in the READMEs.
This Markdown doc can then be easily transformed to a HTML file (e.g. using pandoc)
which will provide a single point of information about the contents of the directories.

Also System Administrators can look in the directory and find the file which
describes the data and who manages it. The README.yaml files can be programatically
searched for metadata such as the data manager or data disposal dates.

## What a README.yaml Looks Like

Example: `/shared/opt/fastqc-0.10.1/README.yaml`

    Title: FastQC is a high throughput sequence QC analysis tool
    Description: FastQC reads a set of sequence files and produces a quality control report.
    Data Manager: Mike Lake
    Data Location: /shared/opt/fastqc-0.10.1

The README.yaml should be in StrictYAML format (https://github.com/crdoconnor/strictyaml).

The keys used in the YAML should be named the same as what is available in any
Data Management Plans that you may be using.

## How to run the Program

Get brief help on the program:

    $ ./ddc.py -h

Run the program to parse all the README.yaml files under /shared/eresearch

    $ ./ddc.py /shared/eresearch

or

    $ cd /shared/eresearch
    $ /pathto/ddc.py .

Run the program and save the Markdown output, then convert to a HTML page:

    $ ./ddc.py /shared/eresearch | tee CATALOG.yaml
    $ pandoc --css=styles.css --self-contained CATALOG.md > CATALOG.html

The `styles.css` file is optional.

Of course most users will have many directories to manage. A better option is to
run a bash script that runs this script over those directories, and combining the
Markdown docs into a website using a static site generator like MkDocs 
https://www.mkdocs.org. A short example of such a script is included and an 
example `mkdocs.yml` file.

## FAQ

Why does this script not recurse? It only looks for README.yaml files in the immediate subdirectories.

> The purpose of this script is to manage large amounts of data. There might be
> hundreds or thousands of directories. The directories might contain millions of files.
> We don't want to unexpectantly find that this script takes hours to run and is
> consuming lots of I/O bandwidth. If you wish to run this script on many
> subdirectories you can write a bash script to do this.

What use plain text README.yaml files? A database is faster.

> A database would put all the metadata in one place - inside the database.
> The metadata would then no longer be with the data it describes. If the data is
> moved then the connection with the data is broken. You would need to update the
> database.

What happens if this script can no longer run? Python changes and this script might not run with
Python 4 or later.

> If you cannot run this script anymore nothing really breaks.
> Future researchers or data managers will see be able to find and understand the data's
> metadata because:
>
> - The README.yaml files will still remain with the data in their directories.
> - The generated markdown files will readable.
> - The static web pages are still likely to be readable with any HTML browser even if they are not
>   being served by a web server.

## License

Copyright 2022 Mike Lake     

Data Directory Cataloger is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

Data Directory Cataloger is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
Data Directory Cataloger. If not, see http://www.gnu.org/licenses/.

Mike Lake

