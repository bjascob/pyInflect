#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
import readline
import spacy
import pyinflect
from   MiscUtils import ignoreWord


# Simple script to allow manual entry of sentences that will get tagged and lemmatized
# then inflected back to their original form.
if __name__ == '__main__':
    # Load Spacy
    print('Loading Spacy model')
    nlp = spacy.load('en_core_web_sm')
    print()

    # process the test sentence
    def process(sent):
        doc = nlp(sent)
        for word in doc:
            ptype = word.tag_[0]
            if ptype in ['N', 'V', 'R', 'J'] and word.tag_!='RP':
                tag_to_use = word.tag_
                infl = word._.inflect(tag_to_use, inflect_oov=True)
                if not infl:
                    print('  None:  %s/%s %s' % (word.text, word.lemma_, word.tag_))
                    continue
                elif infl != word.text and not ignoreWord(word.text):
                    print('   Err:  %s/%s %s -> %s' % (word.text, word.lemma_, word.tag_, infl))
                else:
                    print('  Good:  %s/%s %s -> %s' % (word.text, word.lemma_, word.tag_, infl))
            else:
                print('  n/a :  %s/%s %s' % (word.text, word.lemma_, word.tag_))

    print("Enter a sentence to test or 'q' to quit")
    while 1:
        sent = input('> ')
        if not sent or sent.lower() == 'q':
            break
        process(sent)
        print()
