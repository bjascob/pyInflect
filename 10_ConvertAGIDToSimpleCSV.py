#!/usr/bin/python3
from pyinflect.AGIDReader import *


if __name__ == '__main__':

    agid_fn = 'agid/infl.txt'
    infl_fn = 'pyinflect/infl.csv'

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
