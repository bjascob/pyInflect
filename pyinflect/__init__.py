import os
from .Inflections import Inflections

__version__ = '0.2.0'

INFL_FN = os.path.join(os.path.dirname(__file__), 'infl.csv')
OVERRIDES_FN = os.path.join(os.path.dirname(__file__), 'overrides.csv')

INFLECTION_INST = Inflections(INFL_FN, OVERRIDES_FN)

def InflectionEngine():
    return INFLECTION_INST

def getAllInflections(lemma, pos_type):
    return INFLECTION_INST.getAllInflections(lemma, pos_type)

def getInflection(lemma, tag, use_first_person=True):
    return INFLECTION_INST.getInflection(lemma, tag, use_first_person)
