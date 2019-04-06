#!/usr/bin/python3
import spacy
import nltk
import pyinflect


if __name__ == '__main__':

    # Configuration
    corp_fn   = 'austen-emma.txt'   # to see available do... print(nltk.corpus.gutenberg.fileids())
    max_chars = int(1e5)
    print_nones = False
    print_errs  = True

    # Load Spacy
    print('Loading Spacy model')
    nlp = spacy.load('en_core_web_sm')

    # Load the corpus to test with
    print('Loading corpus')
    text = nltk.corpus.gutenberg.raw(corp_fn)
    print('{:,} characters in corpus, truncated to {:,}'.format(len(text), max_chars))
    text = text[:max_chars]
    text = text.replace('\n', ' ')
    sents = nltk.tokenize.sent_tokenize(text)
    sents = sents[1:-1] # clip the first and last
    print('Used %d test sentences from corpus' % len(sents))
    print()

    # Loop through the sentences
    print('Processing sentences')
    stats = [0]*5     # total words, getInfl calls, infl None returns, infl good, infl bad
    verbs = []
    for i, sent in enumerate(sents):
        doc = nlp(sent)
        for word in doc:
            if len(word.tag_) < 1:
                continue
            stats[0] += 1
            ptype = word.tag_[0]
            if ptype=='N' or ptype=='V' or ptype=='R' or ptype=='J':
                stats[1] += 1
                tag_to_use = word.tag_
                infl = word._.inflect(tag_to_use)
                if not infl:
                    stats[2] += 1
                    if print_nones:
                        print('None: %s/%s %s' % (word.text, word.lemma_, word.tag_))
                    continue
                elif infl != word.text.lower() and not isinstance(infl, list):
                    stats[3] += 1
                    if print_errs:
                        print('Err:  %s/%s %s -> %s' % (word.text, word.lemma_, word.tag_, infl))
                else:
                    stats[4] += 1
    print()
    print('Tested over %d sentences / %d words, looked up %d inflections' % (len(sents), stats[0], stats[1]))
    print('%d inflection returned None' % stats[2])
    print('%d errors / incorrect inflections' % stats[3])
    print('%d correct inflections' % stats[4])
