#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
from   pyinflect import getInflection


if __name__ == '__main__':

    infl = getInflection('example', 'NNS')
    print(infl)
