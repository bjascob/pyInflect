#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
from   pyinflect import getInflection, getAllInflections


if __name__ == '__main__':

    lemma    = 'be'
    tag      = 'VBD'
    pos_type = 'V'

    forms = getAllInflections(lemma, pos_type)
    print(forms)

    infl = getInflection(lemma, tag, use_first_person=False)
    print(infl)
