# Make this usable outside of Spacy
try:
    from spacy.tokens import Token
except ImportError:
    pass


class Inflections(object):
    ''' Class for inflecting words

    This class loads the simplified AGID inflection data and uses it to inflect
    English words from their lemma, based on the supplied treebank tag.

    Args:
        infl_fn (str): filename of the AGID simplified CSV file.
        overrides_fn (str): Optional CSV file with overrides to the AGID data.
    '''
    def __init__(self, infl_fn, overrides_fn=None):
        self.infl_data = self._loadInflections(infl_fn)
        if overrides_fn:
            self.overrides = self._loadOverrides(overrides_fn)
        try:
            Token.set_extension('inflect', method=self.spacyGetInfl)
        except NameError:
            pass

    # Get all inflections in the DB
    def getAllInflections(self, lemma, pos_type):
        ''' Method for getting all inflections for a word.

        This is a standalone method that takes in a given word lemma and returns
        all the associated inflections.

        Args:
            lemma (str): The lemma of the word to lookup
            pos_type (str): Must be 'V', 'A' or 'N' (Verb, Adverb/Adjective, Noun)

        Returns:
            Method returns a list of tuples.  Each entry in the list is a specific inflection
            ordered in the same manner as the AGID.  Each tuple contains various spellings for
            the inflection.
            The capitalization style of the returned forms will be the same as the lemma
            None is returned if the lemma/pos_type is not found in the database.
        '''
        # Get the forms for the lemma or return None if not in the DB
        if pos_type not in ['V', 'A', 'N']:
            raise ValueError('Unrecognized pos type =%s.  Must be V, A or N' % pos_type)
        caps_style = self._getCapsStyle(lemma)
        forms = self.infl_data.get((lemma.lower(), pos_type), None)
        if forms:
            forms = [self._applyCapsStyleToTuple(f, caps_style) for f in forms]
        return forms

    # Get tag specific inflections
    # For tags see https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    def getInflection(self, lemma, tag, use_first_person=True):
        ''' Method for getting inflected words based on their treebank tag.

        This is a standalone method that takes in a given word lemma and returns
        a the associated inflection.

        Args:
            lemma (str): The lemma of the word to lookup
            tag (str): Treebank part-of-speech tag.
            use_first_person (bool): Used only for the specific case of the lemma "be"
                and the tags VBD (past) or VBP (present).  For this verb there
                are 2 possible forms for tag VBD (was/were) and 2 for VBP (am/are).
                If True, return the 1st person (was or am) form.  If False the
                2nd person (were or are) is returned.

        Returns:
            Method returns a tuple of the with various spellings of the inflection.
            The first entry in the tuple is typically the most common.  Many words
            will only have a single spelling.
            The capitalization style of the returned forms will be the same as the lemma
            None is returned if nothing is found in the database.
        '''
        # First thing, check if the lemma/tag is in the overrides file.  If so, just
        # use that value.
        key = (lemma.lower(),tag)
        infl = self.overrides.get(key, None)
        if infl:
            caps_style = self._getCapsStyle(lemma)
            infl = self._applyCapsStyle(infl, caps_style)
            return (infl,)  # tuple
        # Otherwise lookup data in the AGID
        # Get the AGID POS tag from the first letter of the treebank tag
        pos_type = self._tagToAGIDPOSType(tag)
        if not pos_type:
            return None
        # Get all forms for the lemma
        forms = self.getAllInflections(lemma, pos_type)                 # list of tuples
        tag_form = self._getFormsForTag(lemma, tag, pos_type, forms)    # tuple or list for "be"
        # Handle special case for "be"
        if isinstance(tag_form, list):
            if use_first_person:
                return tag_form[0]  # tuple
            else:
                return tag_form[1]  # tuple
        else:
            return tag_form         # tuple

    def spacyGetInfl(self, token, tag, use_first_person=0):
        ''' Spacy extension method "inflect"

        This function is not intended to be called directly.  It is an extension
        to Spacy as defined in the "set_extension" call in "__init__" above.
        Parameters are the same as the "getInflection" method above but only the
        first spelling of any given inflection is returned.
        '''
        # Notes on Spacy lemma capitalization (as of 2.1.3):
        #   Spacy returns the lemmas for words that it knows in lowercase but will return
        #   words this it doesn't (like proper nouns) in the original form.
        #   ie.. nlp('BRAd Is Sitting.') = 'BRAd', 'be', 'sit'
        # Fix this so the capitalization is always preserved in the lemma
        caps_style = self._getCapsStyle(token.text)
        lemma = self._applyCapsStyle(token.lemma_, caps_style)
        tag_form = self.getInflection(lemma, tag, use_first_person)
        if not tag_form:
            return None
        return tag_form[0]

    #######################################################
    ### Private Methods                                 ###
    #######################################################

    # Load infl.csv file
    @staticmethod
    def _loadInflections(fn):
        data = {}
        with open(fn) as f:
            for line in f:
                line = line.strip()
                x = line.split(',')
                word = x[0]
                pos  = x[1]
                # Forms may have multiple spellings separated by /
                forms = [tuple(f.split('/')) for f in x[2:]]
                data[(word, pos)] = forms
        return data

    # Load the overrides.csv file
    @staticmethod
    def _loadOverrides(fn):
        data = {}
        with open(fn) as f:
            for line in f:
                line = line.strip()
                word, pos, infl = line.split(',')
                data[(word,pos)] = infl
        return data

    # Converts the Penn Treebank tag string to V, A or N
    @staticmethod
    def _tagToAGIDPOSType(tag):
        pos_type = tag[0]
        if pos_type in ['J', 'R']:
            pos_type = 'A'
        if pos_type not in ['V', 'A', 'N']:
            raise ValueError('Unrecognized pos_type =%s.  Must be V, A or N' % pos_type)
        return pos_type

    # Get the capitalization style of the word
    @staticmethod
    def _getCapsStyle(word):
        if word.isupper():
            return 'all_upper'
        elif word and word[0].isupper():
            return 'first_upper'
        else:
            return 'lower'

    # Replicate the capitalization style in the new word
    @staticmethod
    def _applyCapsStyle(word, style):
        if style not in ['all_upper', 'first_upper', 'lower']:
            raise ValueError('Invalid caps style = %s' % style)
        if style=='all_upper':
            return word.upper()
        elif style=='first_upper':
            return word.capitalize()
        else:
            return word.lower()

    # Simple helper method to change all words in a tuple
    @classmethod
    def _applyCapsStyleToTuple(cls, words, style):
        new_words = [cls._applyCapsStyle(w, style) for w in words]
        return tuple(new_words)

    # Returns a tuple of the various forms for the spelling
    # In the special case of "be" returns a list of tuples for the possible inflections
    # Note that both lemma and forms are expected to have the correct caps style already.
    @staticmethod
    def _getFormsForTag(lemma, tag, pos_type, forms):
        if not forms:
            return None
        nforms = len(forms)
        # Handle the verbs "be".
        # There is a nice explanation at..return forms
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
        if lemma.lower()=='be':
            if tag=='VB':
                return (lemma,)
            elif tag=='VBD':
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
        elif lemma.lower()=='wit':
            return None
        # Handle Verbs
        #   VBN: Verb, past participle                  -> agid->past part (2nd form) if it exists
        #                                                  else agid->past (1st form)
        #   VBD: Verb, past tense                       -> agid->past (1st form)
        #   VBG: Verb, gerund or present participle     -> ing forms (3rd form)
        #   VBZ: Verb, 3rd person singular present      -> s form (4th form)
        #   VB: Verb, base form                         -> lemma
        #   VBP: Verb, non-3rd person singular present  -> lemma
        elif pos_type=='V':
            if tag not in ['VBN', 'VBD', 'VBG', 'VBZ', 'VB', 'VBP']:
                raise ValueError('Unrecognized Treebank tag for pos_type=V: %s' % tag)
            if tag=='VBN' and nforms>1 and forms[1] != ('<>',):
                return forms[1]
            elif tag=='VBN' or tag=='VBD' and nforms>0:
                return forms[0]
            elif tag=='VBG' and nforms>2:
                return forms[2]
            elif tag=='VBZ' and nforms>3:
                return forms[3]
            elif tag in ['VB', 'VBP']:
                return (lemma,)
            else:
                return None
        # Handle adjectives and adverbs
        #   JJ: Adjective               -> base form / lemma
        #   JJR: Adjective, comparative -> 1st form
        #   JJS: Adjective, superlative -> 2nd form
        #   RB: Adverb 	                -> base form (base form / lemma
        #   RBR: Adverb, comparative    -> 1st form
        #   RBS: Adverb, superlative    -> 2nd form
        elif pos_type=='A':
            if tag not in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']:
                raise ValueError('Unrecognized Treebank tag for pos_type=A: %s' % tag)
            if tag in ['JJ', 'RB']:
                return (lemma,)
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
        elif pos_type=='N':
            if tag not in ['NN', 'NNS', 'NNP', 'NNPS']:
                raise ValueError('Unrecognized Treebank tag for pos_type=N: %s' % tag)
            if tag in ['NN', 'NNP']:
                return (lemma,)
            elif tag in ['NNS', 'NNPS'] and nforms>0:
                return forms[0]
        else:
            return None
