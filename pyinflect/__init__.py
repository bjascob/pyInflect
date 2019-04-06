import os
from .Inflections import Inflections

__version__ = '0.1.0'

INFL_FN = os.path.join(os.path.dirname(__file__), 'infl.csv')

INFLECTION_ENGINE = Inflections(INFL_FN)

def InflectionEngine():
    return INFLECTION_ENGINE
