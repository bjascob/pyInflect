#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
import spacy
import pyinflect
from   MiscUtils import ignoreWord


if __name__ == '__main__':

    # Test setence
    sent = 'I seem to be lost.'

    # Load Spacy
    print('Loading Spacy model')
    nlp = spacy.load('en_core_web_sm')
    print()

    # process the test sentence
    print('Testing: ', sent)
    doc = nlp(sent)
    for word in doc:
        ptype = word.tag_[0]
        if ptype in ['N', 'V', 'R', 'J'] and word.tag_!='RP':
            tag_to_use = word.tag_
            infl = word._.inflect(tag_to_use)
            if not infl:
                print('None: %s/%s %s' % (word.text, word.lemma_, word.tag_))
                continue
            elif infl != word.text and not ignoreWord(word.text):
                print('Err:  %s/%s %s -> %s' % (word.text, word.lemma_, word.tag_, infl))
            else:
                print('Good: %s/%s %s -> %s' % (word.text, word.lemma_, word.tag_, infl))
