#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
from   pyinflect import getAllInflections, getInflection


if __name__ == '__main__':

    print(getAllInflections('be'))
    print(getInflection('be', tag='VBD'))
    print()

    print(getAllInflections('watch'))
    print(getAllInflections('watch', pos_type='V'))
    print(getInflection('watch', tag='VBD'))
    print()
