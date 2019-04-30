import sys
import logging
from   copy import deepcopy
# Make this usable outside of Spacy
try:
    import spacy
except ImportError:
    pass
from . import InflectionRules


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
        if 'spacy' in sys.modules:
            min_version = '2.0'
            mv = min_version.split('.')
            sv = spacy.__version__.split('.')
            if sv[0] > mv[0] or (sv[0] == mv[0] and sv[1] >= mv[1]):
                spacy.tokens.Token.set_extension('inflect', method=self.spacyGetInfl)
            else:
                logging.warning('Spacy extensions are disabled.  Spacy version is %s.  '
                                'A minimum of %s is required', spacy.__version__, min_version)

    # Get all inflections in the DB
    def getAllInflections(self, lemma, pos_type=None):
        ''' Method for getting all inflections for a word.

        This is a standalone method that takes in a given lemma and returns
        all the associated inflections.

        Args:
            lemma (str): The lemma of the word to lookup
            pos_type (str): Optional.  Must be 'V', 'A' or 'N' (Verb, Adverb/Adjective, Noun)
                Returned data is limited to this category if present.

        Returns:
            Method returns a dictionary of the treebank tags with a tuple of their associated forms.
            The capitalization style of the returned forms will be the same as the lemma
            An empty dictionary is returned if the lemma is not found in the database.
        '''
        # Get the forms for the lemma from the main database
        forms = deepcopy(self.infl_data.get(lemma.lower(), {}))
        # Apply any overrides
        overrides = deepcopy(self.overrides.get(lemma.lower(), {}))
        forms.update(overrides)
        if not forms:
            return {}
        # Capitalize all the inflected forms the same as the lemma
        caps_style = self._getCapsStyle(lemma)
        forms = self._applyCapsStyleToDict(forms, caps_style)
        # If there's a pos_type (V, A or N) then return all those types
        if pos_type is not None:
            candidate_tags = self._posTypeToTags(pos_type)
            for key in list(forms.keys()):
                if key not in candidate_tags:
                    del forms[key]
        return forms

    # Get all inflections using the Inflection Rules
    def getAllInflectionsOOV(self, lemma, pos_type):
        ''' Method for using Inflection rules to create a list of inflections for a word.

        This is a standalone method that takes in a given lemma and returns all the associated
        inflections.

        Args:
            lemma (str): The lemma of the word to lookup
            pos_type (str): Must be 'V', 'A' or 'N' (Verb, Adverb/Adjective, Noun)

        Returns:
            Method returns a dictionary of the treebank tags with a tuple of their forms.
            For verbs, adjectives and adverbs, the first form is the "regular" form and the second
            is the doubled form.  For nouns, the first form is the "regular" form and the second
            is the "greco-latin".

            This method may return the inflections under multiple tags.  The goals is to return
            under all possible valid tags so whichever key the user puts into the dictionary will
            give the proper inflection. (past/participle form of verbs are tagged VBN and VBD and
            for pos_type = 'A' both JJx and RBx tags are returned).

            The capitalization style of the returned forms will be the same as the lemma.
        '''
        caps_style = self._getCapsStyle(lemma)
        if pos_type == 'V':
            rv = InflectionRules.buildRegVerb(lemma)
            dv = InflectionRules.buildDoubledVerb(lemma)
            forms = {'VB':(lemma,), 'VBZ':(rv[0], dv[0]), 'VBN':(rv[1], dv[1]), \
                     'VBD':(rv[1],dv[1]), 'VBG':(rv[2],dv[2])}
        elif pos_type == 'A':
            ra = InflectionRules.buildRegAdjAdv(lemma)
            da = InflectionRules.buildDoubledAdjAdv(lemma)
            forms = {'JJ':(lemma,), 'RB':lemma, \
                     'JJR':(ra[0],da[0]), 'RBR':(ra[0],da[0]), \
                     'JJS':(ra[1],da[1]), 'RBS':(ra[1],da[1])}
        elif pos_type == 'N':
            rn = InflectionRules.buildRegNoun(lemma)
            gn = InflectionRules.buildGrecNoun(lemma)
            forms = {'NN':(lemma,), 'NNS':(rn[0],gn[0])}
        else:
            raise ValueError('Unrecognized pos_type = %s' % pos_type)
        forms = self._applyCapsStyleToDict(forms, caps_style)
        return forms

    # Get all inflections in the DB
    def getInflection(self, lemma, tag, inflect_oov=False):
        ''' Method for getting a lemma's inflection for a specific Penn Treebank tag.

        This is a standalone method that takes in a given lemma and returns
        all the associated inflection.

        Args:
            lemma (str): The lemma of the word to lookup
            tag (str):  Penn Treebank tag.  Returned data is limited to this tag.
            inflect_oov (bool): If False only inflections from the AGID lookup are returned.
            If True, InflectionRules via getAllInflectionsOOV will be used to find inflections.

        Returns:
            Method returns a tuple of the inflection(s).
            The capitalization style of the returned forms will be the same as the lemma
            None is returned if the lemma / tag is not found.
        '''
        # Get the forms for the lemma from the main database
        # and use the treebank tag to find the correct return value
        # If we don't find anything in the dictionary, use the rules
        forms = self.getAllInflections(lemma, None)
        if not forms and inflect_oov:
            try:
                pos_type = self._tagToAGIDPOSType(tag)
                forms = self.getAllInflectionsOOV(lemma, pos_type)
            except ValueError:
                pass
        form = forms.get(tag, None)
        return form

    def spacyGetInfl(self, token, tag, form_num=0, inflect_oov=False):
        ''' Spacy extension method "inflect"

        This function is not intended to be called directly.  It is an extension
        to Spacy as defined in the "set_extension" call in "__init__" above.

        Args:
            lemma (str): The lemma of the word to lookup
            tag (str): Penn Treebank tag.  Returned data is limited to this category.
            form_num (int): When more than one form is associated with the given tag,
                return this index in the list.  The default is 0.

        Returns:
            Method returns a string for the inflection
            The capitalization style of the returned forms will be the same as the lemma.
        '''
        # Notes on Spacy lemma capitalization (as of 2.1.3):
        #   Spacy returns the lemmas for words that it knows in lowercase but will return
        #   words this it doesn't (like proper nouns) in the original form.
        #   ie.. nlp('BRAd Is Sitting.') = 'BRAd', 'be', 'sit'
        # Fix this so the capitalization is always preserved in the lemma
        caps_style = self._getCapsStyle(token.text)
        lemma = self._applyCapsStyle(token.lemma_, caps_style)
        tag_form = self.getInflection(lemma, tag, inflect_oov)
        if not tag_form:
            return None
        if form_num < len(tag_form):
            return tag_form[form_num]
        else:
            return tag_form[0]

    #######################################################
    ### Private Methods                                 ###
    #######################################################

    # Load infl.csv file
    @classmethod
    def _loadInflections(cls, fn):
        data = {}
        with open(fn) as f:
            for line in f:
                line = line.strip()
                x = line.split(',')
                # Forms may have multiple spellings separated by /
                forms = [tuple(f.split('/')) for f in x[2:]]
                data = cls._loadInflLineToDict(data, x[0], x[1], forms)
        return data

    # Load the overrides.csv file
    @staticmethod
    def _loadOverrides(fn):
        data = {}
        with open(fn) as f:
            for line in f:
                line = line.strip()
                lemma, tag, forms = line.split(',')
                forms = tuple(forms.split('/'))
                data[lemma] = {tag:forms}
        return data

    # Converts the Penn Treebank tag string to V, A or N
    @staticmethod
    def _tagToAGIDPOSType(tag):
        pos_type = tag[0]
        if pos_type in ['J', 'R']:
            pos_type = 'A'
        if tag == 'MD':
            pos_type = 'V'
        if pos_type not in ['V', 'A', 'N']:
            raise ValueError('Unrecognized pos_type =%s.  Must be V, A or N' % pos_type)
        return pos_type

    # Converts the pos_type (V, A or N) to a list of potential treebank tags
    @staticmethod
    def _posTypeToTags(pos_type):
        if pos_type=='V':
            return ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD']
        elif pos_type=='A':
            return ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']
        elif pos_type=='N':
            return ['NN', 'NNS', 'NNP', 'NNPS']
        else:
            raise ValueError('Unrecognized pos_type =%s.  Must be V, A or N' % pos_type)


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
    def _applyCapsStyleToDict(cls, data, style):
        for key, words in data.items():
            # Check of the values in the dictionary are single string or tuple/list of them
            if isinstance(words, (list, tuple)):
                new_words = [cls._applyCapsStyle(w, style) for w in words]
                data[key] = tuple(new_words)
            else:
                data[key] = cls._applyCapsStyle(words, style)
        return data

    # Add entries to "data" for the lemma.
    # forms is a list of tuples where each tuple has
    @classmethod
    def _loadInflLineToDict(cls, data, lemma, pos_type, forms):
        # Add the lemma key to the data if one isn't already there
        if lemma not in data:
            data[lemma] = {}
        # Handle special case words
        if cls._isSpecialCase(data, lemma, pos_type):
            pass
        # Nouns.  Don't inflect proper nouns
        elif pos_type=='N':
            data[lemma]['NN']  = (lemma,)
            data[lemma]['NNS'] = forms[0]
        # Adjectives and Adverbs
        elif pos_type=='A':
            data[lemma]['JJ'] = (lemma,)
            data[lemma]['RB'] = (lemma,)
            data[lemma]['JJR'] = forms[0]
            data[lemma]['RBR'] = forms[0]
            data[lemma]['JJS'] = forms[1]
            data[lemma]['RBS'] = forms[1]
        # Verbs
        elif pos_type=='V':
            data[lemma]['VB']  = (lemma,)
            data[lemma]['VBP'] = (lemma,)
            data[lemma]['VBD'] = forms[0]
            if forms[1]==('<>',):
                data[lemma]['VBN'] = forms[0]
            else:
                data[lemma]['VBN'] = forms[1]
            data[lemma]['VBG'] = forms[2]
            data[lemma]['VBZ'] = forms[3]
        return data

    # Similar to _loadInflLineToDict but for specific oddball cases
    # Returns True if a case is handled here.
    @staticmethod
    def _isSpecialCase(data, lemma, pos_type):
        # only -> onliest has no comparative form
        if lemma=='only' and pos_type=='A':
            data[lemma]['JJS'] = ('onliest',)
            data[lemma]['RBS'] = ('onliest',)
            return True
        # methinks -> methought (this is just wrong in the AGID)
        elif lemma=='methinks' and pos_type=='V':
            data[lemma]['VB']  = ('methinks',)
            data[lemma]['VBD'] = ('methought',)
            return True
        # modal verbs
        elif lemma=='may' and pos_type=='V':
            data[lemma]['MD']  = ('may', 'mayst', 'might')
            return True
        elif lemma=='shall' and pos_type=='V':
            data[lemma]['MD']  = ('shall', 'shalt', 'should')
            return True
        # Other verbs
        # The verb "be" had 2 ambigous forms for a give treebank tag: was/were and am/are
        elif lemma=='be' and pos_type=='V':
            data[lemma]['VB']  = ("be",)
            data[lemma]['VBD'] = ('was', 'were')
            data[lemma]['VBG'] = ('being',)
            data[lemma]['VBN'] = ('been',)
            data[lemma]['VBP'] = ('am', 'are')
            data[lemma]['VBZ'] = ('is',)
            return True
        # can
        elif lemma=='can' and pos_type=='V':
            data[lemma]['MD']  = ('can', 'canst', 'could')
            data[lemma]['VB']  = ('can',)
            data[lemma]['VBD'] = ('canned',)
            data[lemma]['VBG'] = ('canning',)
            data[lemma]['VBN'] = ('canned',)
            data[lemma]['VBP'] = ('can',)
            data[lemma]['VBZ'] = ('cans',)
            return True
        # will
        elif lemma=='will' and pos_type=='V':
            data[lemma]['MD']  = ('will', 'wilt', 'would', 'wouldst')
            data[lemma]['VB']  = ('will',)
            data[lemma]['VBD'] = ('willed',)
            data[lemma]['VBG'] = ('willing',)
            data[lemma]['VBN'] = ('willed',)
            data[lemma]['VBP'] = ('will',)
            data[lemma]['VBZ'] = ('wills',)
            return True
        # with
        elif lemma=='wit' and pos_type=='V':
            data[lemma]['VB']  = ('wit',)
            data[lemma]['VBD'] = ('wist',)
            data[lemma]['VBG'] = ('witting',)
            data[lemma]['VBN'] = ('wist',)
            data[lemma]['VBP'] = ('wot', 'wost', 'wit', 'wite')
            data[lemma]['VBZ'] = ('wot',)
            return True
        else:
            return False
