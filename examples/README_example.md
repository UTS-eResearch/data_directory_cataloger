# README for this Example

In this directory is an example of what the web page which describes
the software under our directory for shared optional programs looks like. 
Open `example.html` in your web browser. Below is a description of how it
was generated.

## Our Directory `/shared/opt/`

Our top level directory of shared optional programs under `/shared/opt/` 
contains software directories like the list below:

    $ ls -1 /shared/opt/
    centos6
    fastqc-0.10.1
    fastqc-0.11.9
    gromacs-2018.8
    gromacs-2019.6
    gromacs-2020.4
    gromacs-2021.4
    intel
    julia-1.0.0
    julia-1.6.2
    matlab_R2021b
    mmseqs2-v12
    openmpi-4.0.4
    openmpi-4.1.2
    R-3.4.4

## Write the README.yaml Files

This short script just saves a bit of time by writing a README.yaml
file into each of the sub-directories. The text of the README.yaml file
that will be written is in the script. You can edit it to change the text.
For this example nothing needed to be changed so it was just run.

    $ ./write_readmes.py /shared/opt

Each of the top level directories now contains a README.yaml file.

## The README.yaml files under `/shared/opt/`

These are what some of the README.yaml files now look like under the
directory `/shared/opt/`.

/shared/opt/R-3.4.4/README.yaml

    Title: R version 3.4.4
    Description: R version 3.4.4. This is old and can be removed.
    Data Manager: Mike Lake

/shared/opt/centos6/README.yaml

    Title: Old Centos 6 programs
    Description: Older programs compiled under Centos 6. They may work under Centos 8.
    Data Manager: Mike Lake

/shared/opt/fastqc-0.10.1/README.yaml

    Title: FastQC is a high throughput sequence QC analysis tool
    Description: FastQC reads a set of sequence files and produces from each one a quality control report. 
    Data Manager: Mike Lake

/shared/opt/gromacs-2018.8/README.yaml

    Title: GROMACS 2018.8
    Description: Molecular dynamics package mainly designed for simulations of proteins, lipids, and nucleic acids. Compiled with PBS MPI.
    Data Manager: Mike Lake

/shared/opt/intel/README.yaml

    Title: Intel Compiler
    Description: Intel compiler version 2018
    Data Manager: Mike Lake

As you can see above we now have all the metadata describing each sub-directory in the READMEs.

## Run the DDC Program

I then ran the Data Directory Cataloger program over the top level directory directory, directing
the output to `example.md`:
    
    $ ./ddc.py /shared/opt > example.md

## Use pandoc to Create a Webpage

Then I used "pandoc" to convert the "example.md" Markdown document into the
"example.html" HTML page. 
    
    $ pandoc --css=styles.css --self-contained example.md > example.html

This requires the `styles.css` to be in this directory. It will produce a
standalone HTML doc. The `--self-contained` option will insert the styles
into the head of the doc. Hence it will not require the separate styles.css
file to be present when viewing the web page.

You can install `pandoc` from your Linux distribution's repositories.

Mike Lake    
June 2022

