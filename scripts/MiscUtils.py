import sys
import nltk


# load sentences from the nltk corpus
# To see available files do... print(nltk.corpus.gutenberg.fileids())
def loadNLTKCorpus(corp_fn, max_chars=int(1e12)):
    text = nltk.corpus.gutenberg.raw(corp_fn)
    corpus_len = len(text)
    text = text[:max_chars]
    print('{:,} characters from {}, truncated to {:,}'.format(corpus_len, corp_fn, len(text)))
    text = text.replace('\n', ' ')
    sents = nltk.tokenize.sent_tokenize(text)
    sents = sents[1:-1] # clip the first and last
    return sents

# Instances were matching the original word to the returned inflection should
# be ignored.
def ignoreWord(word):
    if word.lower() in ['was', 'were', 'am', 'are', "'s", "n't", "ma'am", "'ve"]:
        return True
    return False

# Simple progress bar
class ProgressBar(object):
    def __init__(self, end_val, bar_len=20):
        self.end_val = end_val
        self.bar_len = bar_len

    def update(self, val):
        percent = float(val) / self.end_val
        if percent > 1.0:
            percent = 1.0
        hashes = '#' * int(round(percent * self.bar_len))
        spaces = ' ' * (self.bar_len - len(hashes))
        sys.stdout.write('\rPercent: [{0}] {1}%'.format(hashes + spaces,
                         int(round(100 * percent))))
        sys.stdout.flush()

    def clear(self):
        spaces = ' ' * (30 + self.bar_len)
        sys.stdout.write('\r{0}'.format(spaces))
        sys.stdout.write('\r')
