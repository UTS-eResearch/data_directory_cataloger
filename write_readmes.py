#!/usr/bin/env python3

'''
This creates README.yaml files in all the first level subdirectories under
a top level directory. Existing README.yaml files are not overwritten.

Usage:

This program just takes one mandatory arg, the top level directory path.
This must be the first argument.
The user can also supply a second arg; either "-t" or "--test".
If this is supplied no README.yaml files will actually be written.

The output is a list of the README.yaml files found and/or created.

    path_to/write_readmes.py top_directory [-t]

To change the contents of the README.yaml you will need to edit this script.
    
TODO: An optional README template e.g. -r README_opt.yaml

Mike Lake
'''

# This is the name of the file to be written. Do not change this.
readme='README.yaml'

# This is the template for the README.yaml that will be written.
# This program will automatically add a "Data Location" field 
# to the end of this template. So do not add one here.
# Note you will also want a trailing space after each ":".
readme_default = '''\
Title: 
Description: 
Data Manager: 
'''

import os, sys

def usage(msg=None):
    print('')
    print("Usage: %s top_directory [-t]" % sys.argv[0])
    print('  Required: a top directory  e.g. /opt')
    print('  Optional: -t or --test to only do a test.')
    print('')
    if msg:
        print(msg)
    sys.exit()

def create_readmes(topdir, template=readme_default, test=False):
    '''
    Given a top level directory find the top level subdirectories. If there
    is a README.yaml then do not replace it, if there is no README.yaml then
    create one.
    '''

    found = [] # List of paths for found READMEs.

    # scandir returns an iterator of DirEntry objects for the given path.
    subdirs = [ f.path for f in os.scandir(topdir) if f.is_dir() ]

    for dir in subdirs:
        doc = template + "Data Location: %s\n" % dir
        file = os.path.join(dir, readme)

        # Debugging lines that can be uncommented.
        #print(file)
        #for line in doc.split('\n'):
        #    print('  ', line)

        if os.path.isfile(file):
            # Found a README.yaml, do not overwrite it.
            found.append(file)
            continue
        else:
            # Create a README.yaml
            if not test:
                with open(file, 'w') as fh:
                    fh.write(doc)
                fh.close()
                print('Wrote ', file)
            else:
                print('Would have wrote ', file)

    # Sort alphabetically just for the users convenience.
    found.sort()

    # Return the found files.
    return found

def main():
    '''
    ./prog 
    ./prog dir 
    ./prog dir template
    ./prog dir template -t
    '''

    test = False

    # Process the args. I do not like argparse.
    if len(sys.argv) < 2:
        usage('Error: You need to specify a top level directory. Exiting')
    elif len(sys.argv) == 2:
        topdir = sys.argv[1]
        print('Processing %s ...' % topdir)
    elif len(sys.argv) == 3:
        topdir = sys.argv[1]
        if sys.argv[2] == '-t' or sys.argv[2] == '--test':
            print('Testing only %s' % topdir)
            test = True
        else:
            usage('Error: Not a valid option: %s' % sys.argv[2])
    else:
        usage('Error: Too many args passed.')
        sys.exit()

    # Check the topdir exists and is a directory.
    if not os.path.isdir(topdir):
        print('Error: you must supply a directory, %s is not a directory.' % topdir)
        print('Exiting')
        sys.exit()

    # Create READMEs under the top directory if they do not exist.
    found = create_readmes(topdir, readme_default, test)

    if len(found) != 0:
        print('\nThe following directories already had a %s file so were not changed:' % readme)
        for path in found:
            print('  ', path)

if __name__ == '__main__':
    main()

