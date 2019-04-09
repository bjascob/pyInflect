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
                    forms.insert(1, ('<>',))
                for i, form in enumerate(forms):
                    # Convert the "form" tuple to a string separated with /
                    string = '/'.join(form)
                    if i < len(forms)-1:
                        f.write('%s,' % string)
                    else:
                        f.write('%s\n' % string)

    # Remove proper nouns (anything thtat starts with an upper-case)
    def removeProperNouns(self):
        ''' Remove all words starting with an uppercase character '''
        keys = list(self.data.keys())
        for key in keys:
            if key[0][0].isupper():
                del self.data[key]

    #######################################################
    ### Private Methods                                 ###
    #######################################################

    # Load the raw AGID infl.txt file
    def _load(self, fn):
        data = {}
        with open(fn) as f:
            for line in f:
                word, pos, forms = self._parse(line)
                data[(word,pos)] = forms
        return data

    # Parse a single line of the data file and return its contents
    def _parse(self, line):
        # Remove everything inside brackets
        line = self._removeBracedText(line)
        # line format is "word pos: form_info"
        lparts = line.split(':')
        # extract the word and pos (V=verb, N=noun, A=adjective or adverb)
        wparts = lparts[0].split(' ')
        word = self._extractAlpha(wparts[0])
        pos  = self._extractAlpha(wparts[1])
        # different forms are separated by |
        form_info = lparts[1]
        forms = []
        for form in form_info.split('|'):
            # Sometimes multiple spellings of the same form exist.  If so they
            # will be comma separated.  Keep these as a tuple of spellings for
            # that form.
            form = form.split(',')
            form = tuple([self._extractAlpha(f) for f in form])
            forms.append(form)
        return word, pos, forms

    # Return only letters by stripping everything else
    @staticmethod
    def _extractAlpha(string):
        return re.sub(r'[^a-zA-Z]', '', string)

    # Remove all text eclosed by {}
    @staticmethod
    def _removeBracedText(string):
        return re.sub(r'\{[^{}]*\}', '', string)
