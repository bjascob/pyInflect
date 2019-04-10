#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
from   collections import defaultdict
import nltk
import spacy
from   MiscUtils import loadNLTKCorpus, ignoreWord, ProgressBar

# Create an empty overrides file before importing pyinflect.
# Normally the overrrides file loads when importing so it needs to be there but
# any overrides in will be used and so will mess up this script.
# Fix this issue by creating an empty file
overrides_fn = '../pyinflect/overrides.csv'
open(overrides_fn, 'w').close()
import pyinflect


# This script creates an overrides file that allows the system to overcome issues with
# the way Spacy lemmetizes words and invalid data in the AGID.
# The created file is a mapping from lemma/tag to the correct inflection.  Note that
# this only overrides methods where the treebank tag is used, not ones where the
# simplified AGID tag (V, N or A) is used.
# Note that if the AGID version is changed this script should be re-run.
# Also note that if Spacy changes their lemmetizer or if a different lemmetizer is used
# these overrides may no longer be valid.
if __name__ == '__main__':

    # Configuration
    #corp_fns  = ['austen-emma.txt']                # 7,491 sentences
    corp_fns  = nltk.corpus.gutenberg.fileids()     # 18 files with 94K sentences
    max_chars = int(1e9)

    # Load Spacy
    print('Loading Spacy model')
    nlp = spacy.load('en_core_web_sm')

    # Load the corpus to test with
    print('Loading corpus')
    sents = []
    for corp_fn in corp_fns:
        sents += loadNLTKCorpus(corp_fn, max_chars)
    print('Loaded {:,} test sentences'.format(len(sents)))
    print()

    # Loop through the sentences
    print('Processing sentences')
    infl_dict = defaultdict(set)       # key(lemma, tag) = set(correct inflections)
    bad_keys = set()
    pb = ProgressBar(len(sents))
    for i, sent in enumerate(sents):
        doc = nlp(sent)
        for word in doc:
            if len(word.tag_) < 1:
                continue
            # Skip "be" since it's already an oddball case and may have errors
            if word.lemma_.lower() == 'be':
                continue
            # Only inflect Nouns, Verbs, Adverbs and Adjectives (and not Particles) and skip
            # some corner cases
            ptype = word.tag_[0]
            if ptype in ['N', 'V', 'R', 'J'] and word.tag_!='RP' and not ignoreWord(word.text):
                infl = word._.inflect(word.tag_)
                # Skip all any None return for now
                if not infl:
                    continue
                # Save all inflections to a dictionary, whos value is a set of the correct inflected values
                key = (word.lemma_.lower(), word.tag_)
                infl_dict[key].add(word.text.lower())
                if infl.lower() != word.text.lower():
                    bad_keys.add(key)
        pb.update(i)
    pb.clear()
    print('Completed.  Loaded {:,} words/tags with inflections'.format(len(infl_dict)))
    print()

    # Eliminate anything that has more than one inflection for the key(ie.. word/tag)
    print('Word/tag keys that map to more than one inflection (these will not go into the overrides)...')
    ambiguous_infl = []
    for key, value in sorted(infl_dict.items()):
        if len(value) > 1:
            ambiguous_infl.append(key)
            print('  %s/%s -> %s' % (key[0], key[1], str(value)))
    for key in ambiguous_infl:
        if key in infl_dict:
            del infl_dict[key]
        if key in bad_keys:
            bad_keys.remove(key)

    # Print some stats
    nbad = len(bad_keys)
    print('Total good word/tag keys = {:,}'.format(len(infl_dict)-nbad))
    print('Total bad  word/tag keys = {:,}'.format(nbad))
    print()

    # Save the overrides to a file
    print('Saving corrected bad keys to overrides file: ', overrides_fn)
    with open(overrides_fn, 'w') as f:
        for key in sorted(bad_keys):
            infl = list(infl_dict[key])[0]    # checked from more than 1 in the set above
            lemma, tag = key
            f.write('%s,%s,%s\n' % (lemma, tag, infl))
    print('done')
