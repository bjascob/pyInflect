import os
from .Inflections import Inflections

__version__ = '0.4.0'

INFL_FN = os.path.join(os.path.dirname(__file__), 'infl.csv')
OVERRIDES_FN = os.path.join(os.path.dirname(__file__), 'overrides.csv')

INFLECTION_INST = Inflections(INFL_FN, OVERRIDES_FN)

def InflectionEngine():
    return INFLECTION_INST

def getAllInflections(lemma, pos_type=None):
    return INFLECTION_INST.getAllInflections(lemma, pos_type)

def getInflection(lemma, tag):
    return INFLECTION_INST.getInflection(lemma, tag)
