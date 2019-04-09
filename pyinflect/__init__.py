import os
from .Inflections import Inflections

__version__ = '0.3.0'

INFL_FN = os.path.join(os.path.dirname(__file__), 'infl.csv')
OVERRIDES_FN = os.path.join(os.path.dirname(__file__), 'overrides.csv')

INFLECTION_INST = Inflections(INFL_FN, OVERRIDES_FN)

def InflectionEngine():
    return INFLECTION_INST

def getInflections(lemma, pos_type=None, tag=None):
    return INFLECTION_INST.getInflections(lemma, pos_type, tag)
