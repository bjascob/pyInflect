import re


class AGIDReader(object):
    ''' Class for converting AGID data.

    This class is designed to read data from the raw AGID file, simplify it and
    then save it in a standardized CVS format.

    Args:
        fn (str): The AGID raw input file (infl.txt) and path.
    '''
    def __init__(self, fn):
        self.data = self._load(fn)

    def _load(self, fn):
        data = {}
        with open(fn) as f:
            for line in f:
                word, pos, forms = self._parse(line)
                data[(word,pos)] = forms
        return data

    def _parse(self, line):
        # line format is "word pos: form_info"
        lparts = line.split(':')
        # extract the word and pos (V=verb, N=noun, A=adjective or adverb)
        wparts = lparts[0].split(' ')
        word = self._extractAlpha(wparts[0])
        pos = self._extractAlpha(wparts[1])
        # Braces arround text denotes an explanation and should be removed
        form_info = lparts[1]
        form_info = self._removeBracedText(form_info)
        # different forms are separated by |
        forms = []
        for form in form_info.split('|'):
            # Sometimes multiple spellings of the same form exist.
            # The first is the prefered so keep that one
            form = form.split(',')[0]
            form = self._extractAlpha(form)
            forms.append(form)
        return word, pos, forms

    # Return only letters by stripping everything else
    @staticmethod
    def _extractAlpha(string):
        return re.sub(r'[^a-zA-Z]', '', string)

    @staticmethod
    def _removeBracedText(string):
        return re.sub(r'\{[^{}]*\}', '', string)

    # Save the data to csv format
    # Incoming data format is
    #   verbs: <past tense> [<past participle>] <-ing form> <-s form>
    #   adjective or adverbs: <-er form> <-est form>
    #   nouns: <plural>
    #   see readme for special cases for be and wit
    def save(self, fn):
        ''' Save the parsed data in .csv format

        Args:
            fn (str): The output filename (ie.. "pyinflect/infl.csv")
        '''
        if not fn.endswith('.csv'):
            fn += '.csv'
        with open(fn, 'w') as f:
            for (word, pos), forms in sorted(self.data.items()):
                f.write('%s,%s,' % (word, pos))
                # for verbs with 3 fields, always write 4 fields,
                #   even if optional <past part> isn't there
                if pos=='V' and len(forms)==3:
                    forms.insert(1, '<>')
                for i, form in enumerate(forms):
                    if i < len(forms)-1:
                        f.write('%s,' % form)
                    else:
                        f.write('%s\n' % form)

    # Remove proper nouns (anything thtat starts with an upper-case)
    def removeProperNouns(self):
        ''' Remove all words starting with an uppercase character '''
        keys = list(self.data.keys())
        for key in keys:
            if key[0][0].isupper():
                del self.data[key]