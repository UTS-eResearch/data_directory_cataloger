# Detailed Usage

This covers some details on how you would use the Data Directory Cataloger to manage
a collection of data directories. In this example I'm using my `hpc_examples` directory.
This contains example scripts for a High Performance Computer cluster.

## Other Metadata Fields One Could Use

* Maintainer:
* Provenance: Downloaded from xxx on 2020.01.01
* RDMP link:
* Data retention and disposal:
* Minimum retention period:

## Looking at README.yaml Files

Find all the README.yaml files under just the immediate subdirectories.

    $ find . -maxdepth 2 -name README.yaml
    ./job_arrays/README.yaml
    ./mpi/README.yaml
    ./primes/README.yaml

This is how to quickly look at all the README.yaml files under the immediate subdirectories.

    $ for f in `find . -maxdepth 2 -name README.yaml`; do echo "$f"; cat $f | sed 's/^/   /'; done
    ./job_arrays/README.yaml
       Title: PBS Job Arrays
       Description: 
       Data Manager: Mike Lake
    ./mpi/README.yaml
       Title: HPC Job Examples for MPI
       Description: HPC Job Examples for MPI
       Data Manager: Mike Lake
       Earliest possible disposal date: 2024
    ./primes/README.yaml
       Title: PBS Primes
       Description: Example of submitting a primes job via PBS
       Data Manager: Mike Lake

To see what README.yaml files just contain the field "Earliest possible disposal date"
in a compact manner we can use:

    $ for f in `find . -maxdepth 2 -name README.yaml`; do echo -n "$f  "; cat $f | grep Earliest || echo ''; done
    ./job_arrays/README.yaml
    ./mpi/README.yaml  Earliest possible disposal date: 2024
    ./primes/README.yaml

## Adding a Field

We can see below that most of my README.yaml files are missing the "Earliest
possible disposal date" field. I'd like to append this to the files that are
missing this field.

    hpc_examples/$ for f in `find . -maxdepth 2 -name README.yaml`; do echo -n "$f  "; cat $f | grep disposal || echo ''; done
    ./.git/README.yaml  
    ./primes/README.yaml  
    ./job_arrays/README.yaml  
    ./mpi/README.yaml  Earliest possible disposal date: 2024
    ./profiling/README.yaml  
    ./checkpointing_dmtcp/README.yaml  
    ./overtime/README.yaml  
    ./cuda/README.yaml  
    ./README.yaml  Earliest possible disposal date: 2024
    ./matlab/README.yaml  

Just create a bash script like this:    

    #!/bin/bash
    
    # Add a line to all README.yaml files in the immediate subdirectories.
    
    # Set the variable "add" to the line that you wish to add.
    # Do not forget the colon. Example:
    #   add="Earliest possible disposal date: 2024"
    add="Earliest possible disposal date: 2024"
    
    files=$(find . -mindepth 2 -maxdepth 2 -name README.yaml)
    for f in $files; do
        grep "$add" $f > /dev/null
        if [ $? -eq 0 ]; then
            # This file already contains this line.
            continue
        fi
        echo "Added to $f"
        echo "$add" >> $f
    done

Run it.

    $ ./ddc_field_add.sh 
    Added to ./.git/README.yaml
    Added to ./primes/README.yaml
    Added to ./job_arrays/README.yaml
    Added to ./profiling/README.yaml
    Added to ./checkpointing_dmtcp/README.yaml
    Added to ./overtime/README.yaml
    Added to ./cuda/README.yaml
    Added to ./matlab/README.yaml

Done. If you run it again nothing will be changed.

    $ ./ddc_field_add.sh
    $ 

## Removing a Field

Many of my READMEs have a field that is not required, and in fact conflics with another field.
I wish to remove the field "Minimum retention period". Here is an example:

    ./pbs_manuals/README.yaml
      Title: Copies of the PBS Manuals for Users
      Description: Contains copies of the PBS manuals which users can download.
      Data Manager: Mike Lake
      Minimum retention period: 2 years        <== We wish to remove this line.
      Earliest possible disposal date: 2024

We can check how many READMEs have this line. Of the 7 READMEs, 6 of them have
the field that I wish to remove.

    $ for f in `find . -maxdepth 2 -name README.yaml`; do echo -n "$f  "; cat $f | grep retention || echo ''; done
    ./README.yaml
    /ansys/README.yaml  Minimum retention period: 1 years
    ./hpc_users/README.yaml  Minimum retention period: 2 years
    ./singularities/README.yaml  Minimum retention period: 2 years
    ./pbs_logs/README.yaml  Minimum retention period: 2 years
    ./pbs_job_examples/README.yaml  Minimum retention period: 2 years
    ./pbs_manuals/README.yaml  Minimum retention period: 2 years
    $

This also picked up the README in the current directory. To exclude this we can add a`-mindepth 2`
to the find command.

First backup the READMEs. The command below will create a tarball of them.
After the editing, if all is OK, we can remove this backup.

    $ tar cvf README_backups.tar `find . -maxdepth 2 -name README.yaml`

We will use sed to edit these files in-place. The usage would be something like this:
`sed -i 's/Minimum retention.*//' filename`. But first lets do a few tests of
our regex pattern that we will use in the sed command.

    $ cat ./ansys/README.yaml
    Title: ANSYS Finite Element Analysis Software
    Description: This Finite Element Analysis Software is an old version and can be removed.
    Data Manager: Mike Lake
    Minimum retention period: 1 years
    Earliest possible disposal date: 2023

This should remove the "Minimum retention ..." line:

    $ sed 's/^Minimum retention period:.*$//' ./ansys/README.yaml
    Title: ANSYS Finite Element Analysis Software
    Description: This Finite Element Analysis Software is an old version and can be removed.
    Data Manager: Mike Lake
     
    Earliest possible disposal date: 2023

Oh. Looks like we would end up with a blank line in there. We don't want that.
You might think that we can just a newline to the regex in sed like this:
`sed 's/Minimum retention period:.*\n//' ./ansys/README.yaml`. You can try it,
but that does not work, as sed strips off the newline before as it reads the line.
Hence the regex will no longer match the line. There are many ways to fix this.
We will just add another sed to remove the blank line:

    $ sed -e 's/^Minimum retention period:.*$//' -e '/^$/d' ./ansys/README.yaml
    Title: ANSYS Finite Element Analysis Software
    Description: This Finite Element Analysis Software is an old version and can be removed.
    Data Manager: Mike Lake
    Earliest possible disposal date: 2023

This works, so now try the fix on one file by adding the `-i` option to sed:

    $ sed -i -e 's/^Minimum retention period:.*$//' -e '/^$/d' ./ansys/README.yaml

Now we can do the fix for all the README files! But instead of the long one-liner here:

    for f in `find . -mindepth 2 -maxdepth 2 -name README.yaml`; do sed -i -e 's/^Minimum retention period:.*$//' -e '/^$/d' $f;  done

Place this into a bash script (e.g. `ddc_field_remove.sh`) and make it executable and run that.
Its been modified so its easier to reuse another time. Note double quotes to allow variable
interpolation in the first sed replace.
Also if you remove the -i you can see what would be done as a dry-run. 

    #!/bin/bash
    # Remove a line from all README.yaml files in the immediate subdirectories.

    # Set the variable remove to the field name that you wish to be removed,
    # upto and including the ':'. Do not include the value.
    remove='Minimum retention period:'

    files=$(find . -mindepth 2 -maxdepth 2 -name README.yaml)
    for f in $files; do
        # If you remove the -i you can see what would be done. 
        sed -i -e "s/^${remove}.*$//" -e '/^$/d' $f
    done

There should be no output if all goes OK. No harm done if you accidentally run
it again, nothing will be changed.

    $ ./ddc_field_remove.sh
    $

Now just repeat the command that printed the READMEs and check they all look OK.

    $ for f in `find . -maxdepth 2 -name README.yaml`; do echo -n "$f  "; cat $f | grep retention || echo ''; done

If you are certain that all is OK then you can now remove the `README_backups.tar`.

