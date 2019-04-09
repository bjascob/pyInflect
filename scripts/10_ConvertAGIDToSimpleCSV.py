#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path

# Create an empty file file before importing pyinflect.
infl_fn = '../pyinflect/infl.csv'
open(infl_fn, 'w').close()
from pyinflect.AGIDReader import *


if __name__ == '__main__':

    agid_fn = '/home/bjascob/Libraries/agid-2016.01.19/infl.txt'

    # Read in AGID inflection file
    print('Loading AGID')
    agid = AGIDReader(agid_fn)

    # Remove all upper-case words
    agid.removeProperNouns()

    # Save a simplified version in csv format
    print('Saving inflections to ', infl_fn)
    agid.save(infl_fn)
    print('done')
    print()
