import os
from .Inflections import Inflections

__version__ = '0.4.1'
__agid_version__ = '2016.01.19' # infl.csv came from this AGID version
__spacy_version__ = '2.1.3'     # the script for overrides.csv used this for lemma/tagging

INFL_FN = os.path.join(os.path.dirname(__file__), 'infl.csv')
OVERRIDES_FN = os.path.join(os.path.dirname(__file__), 'overrides.csv')

INFLECTION_INST = Inflections(INFL_FN, OVERRIDES_FN)

def InflectionEngine():
    return INFLECTION_INST

def getAllInflections(lemma, pos_type=None):
    return INFLECTION_INST.getAllInflections(lemma, pos_type)

def getAllInflectionsOOV(lemma, pos_type, use_doubling=False, use_greco=False):
    return INFLECTION_INST.getAllInflectionsOOV(lemma, pos_type, use_doubling, use_greco)

def getInflection(lemma, tag):
    return INFLECTION_INST.getInflection(lemma, tag)
