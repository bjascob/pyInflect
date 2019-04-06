#!/usr/bin/python3
from   pyinflect import InflectionEngine


if __name__ == '__main__':

    infl = InflectionEngine().getInflection('example', 'NNS')
    print(infl)
