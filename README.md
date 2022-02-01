README 

This is the data directory checker. The purpose of it is to help manage 
numerous directories by having a README.yaml in most directories and which 
stores metadata about the contents of that directory.

# Example for Testing

On Mikes laptop:

    $ cd ~/git/hpc_examples/
    $ ~/git/data_dir_checker/ddc.py . | tee README.md
    $ pandoc --css=styles.css --self-contained README.md > README.html

The `styles.css` file is optional.

# Data Management Plan Notes

Typical Data Management Plan fields might include:

    Project Name: 
    Project Description:
    Start Date: 
    End Date:
    People:
     - Data manager: 
     - Contributors:
      
    Maintainer: 
    Provenance: Downloaded from xxx on 2020.01.01
    Data storage location: 
    RDMP link: 
    Data retention and disposal:
      - Minimum retention period:

Typical Data Record fields might include:

    Data record Title HPC Home for mlake
    Description Contents of the HPC home directory 

    Data manager
    - Name
    - Email

    Contributors
    - Name
    - Email

    # When should your data be reviewed for disposal?
    Minimum retention period
    Earliest possible disposal date of the data
    Where is the data?


