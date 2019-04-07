import os
from .Inflections import Inflections

__version__ = '0.1.1'

INFL_FN = os.path.join(os.path.dirname(__file__), 'infl.csv')

INFLECTION_INST = Inflections(INFL_FN)

def InflectionEngine():
    return INFLECTION_INST

def getInflection(lemma, tag):
    return INFLECTION_INST.getInflection(lemma, tag)
