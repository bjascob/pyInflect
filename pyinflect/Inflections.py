# Make this usable outside of Spacy
try:
    from spacy.tokens import Token
except ImportError:
    pass


class Inflections(object):
    ''' Class for inflecting words

    This class loads the AGID inflection data and uses it to inflect English words
    from their lemma, based on the supplied treebank tag.

    Args:
        fn (str): filename of the AGID simplified CSV file.
    '''
    def __init__(self, fn):
        self.data = self._load(fn)
        try:
            Token.set_extension('inflect', method=self._spacyGetInfl)
        except NameError:
            pass

    # Load infl.csv file
    @staticmethod
    def _load(fn):
        data = {}
        with open(fn) as f:
            for line in f:
                line = line.strip()
                x = line.split(',')
                data[(x[0], x[1])] = x[2:]
        return data

    def _spacyGetInfl(self, token, tag):
        return self.getInflection(token.lemma_, tag)

    # For tags see https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    def getInflection(self, lemma, tag):
        ''' General method for inflecting words.

        This method can be used standalone.  It will also be called by the Spacy
        pipeline methods above.

        Args:
            lemma (str): The lemma of the word
            tag (str): Treebank part-of-speech tag.

        Returns:
            Method returns the inflected word.
        '''
        lemma = lemma.lower()
        # Get the AGID POS tag from the first letter of the treebank tag
        pos = tag[0]
        if pos in ['J', 'R']:
            pos = 'A'
        if pos not in ['V', 'A', 'N']:
            return None
            #raise ValueError('Unrecognized pos type =%s.  Must be V, A or N' % pos)
        # Get the forms for the lemma or return None if not in the DB
        forms = self.data.get((lemma, pos), [])
        if not forms:
            return None
        nforms = len(forms)
        # Handle the verbs "be".
        # There is a nice explanation at..
        #   https://english.stackexchange.com/questions/139537/
        #       in-how-many-inflectional-forms-can-a-verb-be-written-english
        #   VBD => was      -> <past 1st & 3d singular> (agid 1st form)
        #   VBD => were     -> <2d singular, plural, past subjunctive> (agid 2nd form)
        #   VBN => been     -> <past participle> (agid 3rd form)
        #   VBG => being    -> <present participle> (agid 4th form)
        #   VBP => am       -> <present 1st singular> (agid 5th form)
        #   VBP => are      -> <2d singular> (agid 6th form)
        #   VBZ => is       -> <3d singular> (agid 7th form)
        #   VBP => are      -> <plural present> (agid 8th form)
        if lemma=='be':
            if tag=='VBD':
                return [forms[0], forms[1]]     # exact form is ambiguous
            elif tag=='VBN':
                return forms[2]
            elif tag=='VBG':
                return forms[3]
            elif tag=='VBP':
                return [forms[4], forms[5]]     # exact form is ambiguous
            elif tag=='VBZ':
                return forms[6]
            else:
                return None
        # Handle special case "wit".  This is an uncommon verb so for now just return None.
        elif lemma=='wit':
            return None
        # Handle Verbs
        #   VBN: Verb, past participle                  -> agid->past part (2nd form) if it exists
        #                                                  else agid->past (1st form)
        #   VBD: Verb, past tense                       -> agid->past (1st form)
        #   VBG: Verb, gerund or present participle     -> ing forms (3rd form)
        #   VBZ: Verb, 3rd person singular present      -> s form (4th form)
        #   VB: Verb, base form                         -> lemma
        #   VBP: Verb, non-3rd person singular present  -> lemma
        elif pos=='V':
            if tag not in ['VBN', 'VBD', 'VBG', 'VBZ', 'VB', 'VBP']:
                raise ValueError('Unrecognized Treebank tag for pos=V: %s' % tag)
            if tag=='VBN' and nforms>1 and forms[1] != '<>':
                return forms[1]
            elif tag=='VBN' or tag=='VBD' and nforms>0:
                return forms[0]
            elif tag=='VBG' and nforms>2:
                return forms[2]
            elif tag=='VBZ' and nforms>3:
                return forms[3]
            elif tag in ['VB', 'VBP']:
                return lemma
            else:
                return None
        # Handle adjectives and adverbs
        #   JJ: Adjective               -> base form / lemma
        #   JJR: Adjective, comparative -> 1st form
        #   JJS: Adjective, superlative -> 2nd form
        #   RB: Adverb 	                -> base form (base form / lemma
        #   RBR: Adverb, comparative    -> 1st form
        #   RBS: Adverb, superlative    -> 2nd form
        elif pos=='A':
            if tag not in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']:
                raise ValueError('Unrecognized Treebank tag for pos=A: %s' % tag)
            if tag in ['JJ', 'RB']:
                return lemma
            elif tag in ['JJR', 'RBR'] and nforms>0:
                return forms[0]
            elif tag in ['JJS', 'RBS'] and nforms>1:
                return forms[1]
            else:
                return None
        # Handle nouns
        #   NN: Noun, singular or mass  -> base/lemma
        #   NNS: Noun, plural           -> 1st form
        #   NNP: Proper noun, singular  -> base/lemma
        #   NNPS: Proper noun, plural   -> 1st form
        elif pos=='N':
            if tag not in ['NN', 'NNS', 'NNP', 'NNPS']:
                raise ValueError('Unrecognized Treebank tag for pos=N: %s' % tag)
            if tag in ['NN', 'NNP']:
                return lemma
            elif tag in ['NNS', 'NNPS'] and nforms>0:
                return forms[0]
        else:
            return None
