#!/usr/bin/env python3

'''
This is the data directory cataloger. The purpose of it is to help manage 
numerous directories by having a README.yaml in most directories and which 
stores metadata about the contents of that directory.

This program expects a "base" directory as input. 

Under this base directory it then looks for subdirectories, but only ONE level down.
In each first level subdirectory it looks for the README.yaml file that should describe 
the data under that subdirectory.

Once it has found the README.yaml file it parses that file, and appends the metadata 
to a Markdown document summarising the metadata in the READMEs. 

This Markdown doc is just printed to standard output so it can be viewed or redirected 
to an output file. The output file can be converted to a HTML file using pandoc.

Author: Mike Lake
Date: 2022.01.25

To get help for using the program just run: ./ddc.py -h 
'''
    
# Filename of the README in each directory that contains the directory meta information.
# This does not need to be literally "README.yaml". It just needs to not clash with other filename 
# in the directory that you are processing. Example, if you don't want to use README.yaml then you 
# might use CATALOG.yaml. 
readme='README.yaml'

import argparse, os, sys
import yaml, datetime

def parse_args():

    parser = argparse.ArgumentParser( \
        description='Program to catalog all %s docs under a directory.' % readme)

    # Mandatory arguments.
    parser.add_argument('directory', help='The directory to catalog.')

    # Optional arguments. None

    args = parser.parse_args()
    return args

def get_readmes(basedir):
    '''
    Given a base directory return two lists:
    1. A found list of all directory paths that have a README.yaml 
    2. A missing list of directory paths that do not have a README.yaml
    They are sorted alphabetically for the convenience of the user.
    '''

    found = []      # List of paths for found READMEs.
    missing = []    # List of paths missing READMEs.

    # scandir returns an iterator of DirEntry objects for the given path.
    subdirs = [ f.path for f in os.scandir(basedir) if f.is_dir() ]

    for dir in subdirs: 
        # Append the path to the directory to either the found list or the
        # missing list, depending on whether the README was found or not.
        if os.path.isfile(os.path.join(dir, readme)):
            found.append(dir)
        else:
            missing.append(dir)
   
    # Sort alphabetically.
    found.sort()
    missing.sort()

    # Return a tuple of a list of the found and the missing READMEs.
    return (found, missing)

def parse_readmes(found):
    '''
    Takes a list of directories containing a README.yaml file and parses that README doc.
    Each doc's YAML structure is a dictionary.
    '''
    data = {}
    for dir in found:
        file = os.path.join(dir, readme)
        with open(file, 'r') as stream:
            try:
                # Note here, use safe_load() and not load()! Do not trust user input!
                # Especially as this program might be run as the root user.
                doc = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print('Error in reading YAML file: ', e)

        # Debugging lines
        #print('---------------------------')
        #print('README: %s' % file)
        #print('PYTHON OBJECT: ', doc)
        #print('YAML DUMP:')
        #print(yaml.dump(doc, default_flow_style=False, sort_keys=False))
        #print(doc.keys())

        # Here we add the current "dir" to this YAML doc so that we will have
        # this info when we print out the Markdown table.
        doc['Directory'] = dir

        # Add this YAML doc to the data dictionary with the directory path as the key.
        data[dir] = doc

    return data

def check_metadata(data):
    '''
    All the READMEs should have the same metadata keys.
    But we should allow one or more to have missing keys.
    Here we print out the keys. 
    The number of keys should be the same.
    '''

    # This set starts off as empty but will, at the end of the loop, contain 
    # the complete set of all metadata values from all the README.yam files. 
    metadata = set()

    for directory in data.keys():
        doc = data[directory]
        this_set = set(doc.keys())
        # The | operator gives the union of the two sets. By doing a union of sets 
        # we are effectively adding this latest set to the final metadata set.
        metadata = metadata | this_set

    print('\nThe following are all the %d metadata attributes found in the %s files.' \
        % (len(metadata), readme))
    print('These should all be unique. If not edit and correct the %s files.' % readme)
    print('')
    [print(' -', item) for item in sorted(metadata)]

    # Now that we have a metadata set containing all the metadata values that are
    # present in the README.yam files we can check if any READMEs are missing any 
    # metadata values.

    print('\nChecking each %s file against the metadata list above ...\n' % readme) 
    for directory in data.keys():
        doc = data[directory]
        this_set = set(doc.keys())
        if len(doc) != len(metadata):
            # Note: The set difference used below isn’t commutative! 
            print(' -', os.path.join(directory, readme), '    ')

            # Alternatives to printing the set differences.
            #print('    Possibly missing: ', metadata - this_set)
            #print('    Possibly missing: `%s`' % str(metadata - this_set))
            #print('    Possibly missing: ', end='')
            #print([str(item) for item in (metadata - this_set)])

            # This is probably the clearest in Markdown for printing the set differences.
            print('    Possibly missing: ', end='')
            l = ['"%s"' % item for item in (metadata - this_set)]
            print('` %s `' % ', '.join(l))

def create_markdown_header(timenow):

    # Valid Markdown docs have some metadata at the top. Set that here.
    # Note we use a backslash here to suppress the leading newline 
    # as we do not want that in the Markdown.
    metadata = '''\
---
pagetitle: %s
creator: %s
date: %s
---''' % ('Data Directory Check', sys.argv[0], timenow)

    print(metadata)

def create_markdown_table(columns, data):
    '''
    This takes a list of the keys to print out and the YAML data. 
    The columns is a list and might be like this: ['Title', 'Description', 'Data Manager']
    The data is a dictionary of all the YAML docs keyed by their path.
    The final Markdown doc summarising this would be like this:

    | Title | Description |
    | ----- | ----------- |
    | HPC Job Examples for PBS Job Arrays | some description |
    | HPC Job Examples for Checkpointing  | "                |
    | HPC Job Examples for MPI            | "                |
    '''

    print('') 

    # Print the Markdown header from the keys.
    print('| ', end='') 
    print(' | '.join(columns), end='')
    print(' |') 

    # Print the underlining for the header above.
    l = [ '-' * len(col) for col in columns ]
    print('| ', end='') 
    print(' | '.join(l), end='')
    print(' |') 

    # Print the data.
    for key in data.keys():
        doc = data[key]
        l = []
        for col in columns:
            if col not in doc:
                # This doc is missing this key.
                doc[col] = '' 
            if not doc[col]:
                # This doc has the key but its missing a value.
                doc[col] = '' 
            l.append(doc[col])
        print('| ', end='') 
        print(' | '.join(l), end='')
        print(' |') 

def main():

    # Get the program args.
    args = parse_args()
    basedir = args.directory

    # This arg shoud be a directory.
    if not os.path.isdir(basedir):
        print('Error: you must supply a directory, %s is not a directory.' % basedir)
        print('For help run: %s -h' % sys.argv[0])
        sys.exit()
    
    # Get the time and todays date.
    timenow = datetime.datetime.now().strftime('%Y-%m-%d at %I:%M %p')
    
    create_markdown_header(timenow)
    print('# Directory `%s`' % basedir)

    # The "data" variable is a dictionary. It's keys will be the README.yaml 
    # file paths and the values are the YAML structures for that README.yaml  
    data = {}

    # Get all the READMEs under the base directory. 
    (found, missing) = get_readmes(basedir)

    # Print some info to the user on what was found or otherwise.
    if len(missing) != 0:
        print('\n## Warnings\n')
        print('\nThe following subdirectories are missing a %s file:\n' % readme)
        for path in missing: 
            print(' -', path)

    print('\n## Summary\n')
    print('\nFound %d `%s` files in the directories under `%s`.' % (len(found), readme, basedir))
    if len(found) == 0:
        print('Exiting.')
        sys.exit()

    #print('\nFound a %s file in the following directories:\n' % readme)
    #for path in found:
    #    print(' -', path)

    # Parsing these README YAML docs.
    data = parse_readmes(found)

    print('A summary of the metadata in these files follows.')
    # TODO how can users easily specify the columns to print?  Maybe a ddc.conf file?
    # This might be a ddc.yaml that contains the keys and the definition of each key 
    # that should be in each README.
    # Place in this list the keys that you wish to print out. 
    # Capitisation is important. They have to match the keys in your YAML structure.
    columns = ['Directory', 'Title', 'Description', 'Data Manager']
    create_markdown_table(columns, data)

    # Check the metadata in these READMEs for consistency.
    print('\n## Supplementary Information')
    check_metadata(data)
    
    print('\nThis page last updated on %s' % timenow)

if __name__ == '__main__':
    main()

