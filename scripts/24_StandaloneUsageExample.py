#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
from   pyinflect import getInflections


if __name__ == '__main__':

    print(getInflections('be'))
    print(getInflections('be', tag='VBD'))
    print()

    print(getInflections('watch'))
    print(getInflections('watch', pos_type='V'))
    print(getInflections('watch', tag='VBD'))
    print()
