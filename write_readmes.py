#!/usr/bin/env python3

'''
This creates README.yaml files in all the first level subdirectories under a base directory.
This program just takes one input arg, a base directory path. 
The output is a list of the README.yaml files found and/or created.
To change the contents of the README.yaml you will need to edit this script.
'''
    
readme='README.yaml'

import os, sys, datetime

def create_readmes(basedir):
    '''
    Given a base directory find the top level subdirectories. If there is a 
    README.yaml then do not replace it, if there is no README.yaml then 
    create one using the doc string below. 
    '''

    found = []      # List of paths for found READMEs.

    # scandir returns an iterator of DirEntry objects for the given path.
    subdirs = [ f.path for f in os.scandir(basedir) if f.is_dir() ]

    for dir in subdirs: 
        doc = '''\
---
Title: 
Description: 
Data Manager: Mike Lake
Data Location: %s
---
''' % dir

        file = os.path.join(dir, readme)
        if os.path.isfile(file):
            # Found a README.yaml, do not overwrite it.
            found.append(file)
            continue
        else:
            # Create a README.yaml
            with open(file, 'w') as fh:
                fh.write(doc)
            fh.close()
            print('Wrote ', file)
   
    # Sort alphabetically just for the users convenience.
    found.sort()

    # Return the found files.
    return found

def main():

    if len(sys.argv) != 2:
        print('Needs a directory as an arg. Exiting.')
        sys.exit()
    else:
        basedir = sys.argv[1]

    # This arg shoud be a directory.
    if not os.path.isdir(basedir):
        print('Error: you must supply a directory, %s is not a directory.' % basedir)
        print('Exiting')
        sys.exit()
    
    # Get the time and todays date.
    timenow = datetime.datetime.now().strftime('%Y-%m-%d at %I:%M %p')
   
    # Create READMEs under the base directory if they do not exist. 
    found = create_readmes(basedir)

    if len(found) != 0:
        print('\nThe following directories have a %s file:\n' % readme)
        for path in found:
            print(path)

if __name__ == '__main__':
    main()

