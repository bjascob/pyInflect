#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
import spacy
import nltk
import pyinflect
from   MiscUtils import loadNLTKCorpus, ignoreWord


if __name__ == '__main__':

    # Configuration
    corp_fn   = 'austen-emma.txt'   # to see available do... print(nltk.corpus.gutenberg.fileids())
    max_chars = int(1e5)
    print_nones = False
    print_errs  = True

    # Matching exceptions to ignore
    ignores = ['was', 'were', 'am', 'are', "'s", "n't"]

    # Load Spacy
    print('Loading Spacy model')
    nlp = spacy.load('en_core_web_sm')

    # Load the corpus to test with
    print('Loading corpus')
    sents = loadNLTKCorpus(corp_fn, max_chars)
    print('Loaded {:,} test sentences'.format(len(sents)))
    print()

    # Loop through the sentences
    print('Processing sentences')
    stats = [0]*5     # total words, getInfl calls, infl None returns, infl good, infl bad
    for i, sent in enumerate(sents):
        doc = nlp(sent)
        for word in doc:
            if len(word.tag_) < 1:
                continue
            stats[0] += 1
            ptype = word.tag_[0]
            if ptype in ['N', 'V', 'R', 'J'] and word.tag_!='RP':
                stats[1] += 1
                tag_to_use = word.tag_
                infl = word._.inflect(tag_to_use)
                if not infl:
                    stats[2] += 1
                    if print_nones:
                        print('None: %s/%s %s' % (word.text, word.lemma_, word.tag_))
                    continue
                elif infl != word.text and not ignoreWord(word.text):
                    stats[3] += 1
                    if print_errs:
                        print('Err:  %s/%s %s -> %s' % (word.text, word.lemma_, word.tag_, infl))
                else:
                    stats[4] += 1
    print()
    print('Tested over %d sentences / %d words, looked up %d inflections' % (len(sents), stats[0], stats[1]))
    print('{:,} correct inflections'.format(stats[4]))
    print('{:,} inflections returned None'.format(stats[2]))
    print('{:,} errors / incorrect inflections'.format(stats[3]))
