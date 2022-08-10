#!/bin/bash

# This installs or updates the data directory cataloger from the git directory.
# You will need to set the directory where you wish to install the programs below.
# Run this script with sudo if the destination directory is only writable by root.
#
# Usage:
#
#   $ ./install_ddc.sh
#
# or:
#
#   $ sudo ./install_ddc.sh

# Set the full path to the directory where you wish to install the two DDC
# programs here. Do not add any trailing / on the end.
dest='/opt/eresearch/bin'

# Nothing else below here needs to be changed.

function get_version {
    # This stores the current git version in the variable "version_string".
    #
    # If this repo is checked out at a tagged release version then just
    # use the tag number only for the displayed version, like 2.0.0.
    # If this repo is not at a tagged release then we wish to know the exact
    # patch that a user might be using so use the long "git describe" string
    # like 2.0.0-6-g382c9e0.
    # The command "git describe" string format is:
    #   'tag' - 'number of commits' - 'abbreviated commit name'
    # e.g. git describe v2.0.0 --long
    #      v2.0.0-0-g7ef3b13  <== The middle number is zero.
    #
    # ie.g. git describe --long
    #      v2.0.0-6-g382c9e0  <== The middle number is not zero.
    #
    description=$(git describe --long)
    version_num=$(echo $description | cut -d '-' -f1)  # e.g. v2.0.0
    num_commits=$(echo $description | cut -d '-' -f2)  # e.g. 71
    commit_hash=$(echo $description | cut -d '-' -f3)  # e.g. g1d02627
    if [ $num_commits -eq 0 ]; then
        # This is a tagged release.
        version_string=$version_num
    else
        # This version has commits after the last tagged release.
        version_string="$version_num + $num_commits ($commit_hash)"
    fi
}

######
# Main
######

echo ""
echo "----------------------------------------------"
echo "Install or Update the Data Directory Cataloger"
echo "----------------------------------------------"
echo ""

if [ ! -d $dest ]; then
    echo "The directory $dest does not exist. "
    echo "Exiting."
    exit 0
fi

# Get the current git version.
get_version

# Check user really wants to install.
echo "This script will install the two DDC programs to ${dest}/"
echo "The version being installed is $version_string"

read -r -p "Type \"y\" to install. Any other key will exit: " REPLY
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "exiting"
    exit 0
fi

# If the destination directory does not exist, then create it.
if [ ! -d $dest ]; then
    echo "Creating directory $dest"
    mkdir -p $dest
    if [ $? -ne 0 ]; then
        echo "Could not create directory $dest"
        echo "Perhaps you need to use sudo. Exiting."
        exit 0
    fi            
fi

# Backup any existing ddc.py program and rename it with todays date.
# But once todays backup is created, don't overwrite it again.
TODAY=$(date "+%Y.%m.%d")   # Todays date, 2013.12.26
if [ -f ${dest}/ddc.py ] && [ ! -f ${dest}/ddc_${TODAY}.py ]; then
    echo "Copying ddc.py to backup."        
    cp ${dest}/ddc.py ${dest}/ddc_${TODAY}.py
    if [ $? -ne 0 ]; then
        echo "Could not create backup."
        echo "Perhaps you need to use sudo. Exiting."
        exit 0
    fi            
fi        

# Copy the programs to the destination.
cat ddc.py | sed "s/VERSION_STRING/$version_string/" > ${dest}/ddc.py
cp write_readmes.py ${dest}/

