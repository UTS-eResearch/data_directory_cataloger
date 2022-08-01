# README

This is the Data Directory Cataloger. The purpose of it is to help manage
numerous directories by having a README.yaml in most directories and which
stores metadata about the contents of that directory. Typical metadata that
you would store might be "Description", "Data Manager" and "Disposal Date".

When the `ddc.py` program is run on a directory it looks for `README.yaml` files
in the **immediate** sub-directories. From those `README.yaml` files it reads the
metadata, and outputs a single Markdown document summarising the metadata in the READMEs.
This Markdown doc can then be easily transformed to a HTML file (e.g. using `pandoc`)
which will provide a single point of information about the contents of the directories.

Also System Administrators can look in the sub-directories and will find the `README.yaml` 
files which describe the data and who manages it. The README.yaml files can be also 
be programatically searched for metadata such as the data manager or data disposal
dates.

Multiple top level directories can be cataloged and the Markdown docs can be combined 
into a static website which then describes multiple top-level directories. Each
of those might even have different metadata fields.

## What a README.yaml Looks Like

Example: `/shared/opt/fastqc-0.10.1/README.yaml`

    Title: FastQC is a high throughput sequence QC analysis tool
    Description: FastQC reads a set of sequence files and produces a quality control report.
    Data Manager: Mike Lake
    Data Location: /shared/opt/fastqc-0.10.1

The README.yaml should be in StrictYAML format (https://github.com/crdoconnor/strictyaml).

The keys used in the YAML should be named the same as what is available in any
Data Management Plans that you may be using.

## How to run the DDC Program

Get brief help on the program:

    $ ./ddc.py -h

Run the program on a single "top level" directory to find and parse the README.yaml
files in the immediate sub-directories of that directory. For example our 
`/shared/opt` directory contains a dozen sub-directories containing scientific software,
and each of those directories contain a README.yaml file.

    $ ./ddc.py /shared/opt

or

    $ cd /shared/opt
    $ /pathto/ddc.py .

It will print a single Mardown document containing the metadata in the READMEs. 

We actually need to save this output so it can be converted to a HTML page so
redirect it to a file:
    
    $ ./ddc.py /shared/opt > CATALOG.yaml

Now you can use a utility like `pandoc` to convert the Markdown to a HTML page:

    $ pandoc --css=styles.css --self-contained CATALOG.md > CATALOG.html

See the examples directory in this repo for an example of running this on our
`/shared/opt/` directory. This alsp contains an example `styles.css` file.

Of course most users will have many directories to manage. A better option is to
run a bash script that runs this script over those directories, and combining the
Markdown docs into a website using a static site generator like MkDocs 
https://www.mkdocs.org. A short example of such a script is included and an 
example `mkdocs.yml` file.

## Writing your Initial README.yaml Files 

This short script can save a lot of time by writing a README.yaml
file into each of the immediate sub-directories of a top level directory.
The text of the README.yaml file that will be written is in the script. 
You need to edit it to change the text.

    $ ./write_readmes.py top_level-directory

## FAQ

Why does this script not recurse? It only looks for README.yaml files in the
immediate subdirectories.

> The purpose of this script is to manage large amounts of data. There might be
> hundreds or thousands of directories. The directories might contain millions of files.
> We don't want to unexpectedly find that this script takes hours to run and is
> consuming lots of I/O bandwidth. If you wish to run this script on many
> subdirectories you can write a bash script to do this.

Why use plain text README.yaml files? A database is faster.

> A database would put all the metadata in one place - inside the database.
> The metadata would then no longer be with the data it describes. If the data is
> moved then the connection with the data is broken. You would need to update the
> database.

What happens if this script can no longer run? Python changes and this script might
not run with Python 4 or later.

> If you cannot run this script anymore nothing really breaks.
> Future researchers or data managers will see be able to find and understand the data's
> metadata because:
>
> - The README.yaml files will still remain with the data in their directories.
> - The generated markdown files will readable.
> - The static web pages are still likely to be readable with any HTML browser even 
>   if they are not being served by a web server.

## License

Copyright 2022 Mike Lake     

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
Data Directory Cataloger. If not, see http://www.gnu.org/licenses/.

Mike Lake

