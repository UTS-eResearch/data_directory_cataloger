# README 

This is the data directory cataloger. The purpose of it is to help manage 
numerous directories by having a README.yaml in most directories and which 
stores metadata about the contents of that directory.

When the program is run on a top level directory it looks for README.yaml files in
the immediate sub-directories. From those README files it reads the metadata, and 
creates a single Markdown file summarising the metadata in the READMEs.
This Markdown doc can then be easily transformed to a HTML file (e.g. using pandoc) 
which will provide a single point of information about the contents of the directories.

Also System Administrators can look in the directory and find the file which
describes the data and who maintains it. The README.yaml files can be programatically 
searched for metadata such as the maintainer or data disposal dates.

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

Mike Lake
January 2022

