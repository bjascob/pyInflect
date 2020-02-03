#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
import unittest
import spacy
import pyinflect


# Just to faciliate testing
class InflTestHelper(object):
    def __init__(self, pos_type, lemma, forms):
        self.pos_type     = pos_type
        self.lemma        = lemma
        # Put the forms into a dictionary for easy comparion
        if pos_type == 'V':
            assert len(forms) == 3
            self.inflections = {'VB':lemma, 'VBZ':forms[0], 'VBN':forms[1], 'VBG':forms[2]}
        elif pos_type == 'A':
            assert len(forms) == 2
            self.inflections = {'JJ':lemma, 'JJR':forms[0], 'JJS':forms[1]}
        elif pos_type == 'N':
            assert len(forms) == 1
            self.inflections = {'NN':lemma, 'NNS':forms[0]}
        else:
            assert False, 'Invalid pos_type = %s' % pos_type

    def inflectionsInDict(self, form_dict, form_num=0):
        for tag, infl in self.inflections.items():
            forms = form_dict.get(tag, None)
            # for the base forms there's only one form so always use form_num=0
            fnum = 0 if tag in ['VB', 'JJ', 'RR', 'NN'] else form_num
            if not infl == forms[fnum]:
                return False
        return True


# Class for test cases
class InflectionRulesTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(InflectionRulesTests, self).__init__(*args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def testPosTypeException(self):
        self.assertRaises(ValueError, pyinflect.getAllInflectionsOOV, 'test', 'X')

    def testCapitalization(self):
        test_cases = []
        test_cases.append( InflTestHelper('V', 'DISmiss', ('Dismisses', 'Dismissed','Dismissing')))
        test_cases[-1].inflections['VB'] = 'Dismiss' # override InflTestHelper's so test is correct
        test_cases.append( InflTestHelper('A', 'Brainy', ('Brainier', 'Brainiest')) )
        test_cases.append( InflTestHelper('N', 'FLY', ('FLIES',)) )
        for word in test_cases:
            infl_dict = pyinflect.getAllInflectionsOOV(word.lemma, word.pos_type)
            msg = '\n%s\nCorrect : %s\nFunction: %s' %  (word.lemma, word.inflections, infl_dict)
            self.assertTrue( word.inflectionsInDict(infl_dict), msg)

    def testRegularVerbs(self):
        test_cases = []
        test_cases.append( InflTestHelper('V', 'dismiss', ('dismisses', 'dismissed','dismissing')) )
        test_cases.append( InflTestHelper('V', 'waltz', ('waltzes', 'waltzed', 'waltzing')) )
        test_cases.append( InflTestHelper('V', 'index', ('indexes', 'indexed', 'indexing')) )
        test_cases.append( InflTestHelper('V', 'detach', ('detaches', 'detached', 'detaching')) )
        test_cases.append( InflTestHelper('V', 'distinguish', ('distinguishes', 'distinguished', 'distinguishing')) )
        test_cases.append( InflTestHelper('V', 'tie', ('ties', 'tied', 'tying')) )
        test_cases.append( InflTestHelper('V', 'agree', ('agrees', 'agreed', 'agreeing')) )
        test_cases.append( InflTestHelper('V', 'canoe', ('canoes', 'canoed', 'canoeing')) )
        test_cases.append( InflTestHelper('V', 'dye', ('dyes', 'dyed', 'dyeing')) )
        test_cases.append( InflTestHelper('V', 'dry', ('dries', 'dried', 'drying')) )
        test_cases.append( InflTestHelper('V', 'love', ('loves', 'loved', 'loving')) )
        test_cases.append( InflTestHelper('V', 'talk', ('talks', 'talked', 'talking')) )
        for word in test_cases:
            infl_dict = pyinflect.getAllInflectionsOOV(word.lemma, word.pos_type)
            msg = '\n%s\nCorrect : %s\nFunction: %s' %  (word.lemma, word.inflections, infl_dict)
            self.assertTrue( word.inflectionsInDict(infl_dict), msg)

    def testDoubledVerbs(self):
        test_cases = []
        test_cases.append( InflTestHelper('V', 'ban', ('bans', 'banned','banning')) )
        test_cases.append( InflTestHelper('V', 'cancel', ('cancels', 'cancelled','cancelling')) )
        test_cases.append( InflTestHelper('V', 'clog', ('clogs', 'clogged','clogging')) )
        for word in test_cases:
            infl_dict = pyinflect.getAllInflectionsOOV(word.lemma, word.pos_type)
            msg = '\n%s\nCorrect : %s\nFunction: %s' %  (word.lemma, word.inflections, infl_dict)
            self.assertTrue( word.inflectionsInDict(infl_dict, form_num=1), msg)

    def testRegularAdjs(self):
        test_cases = []
        test_cases.append( InflTestHelper('A', 'brainy', ('brainier', 'brainiest')) )
        test_cases.append( InflTestHelper('A', 'gray', ('grayer', 'grayest')) )
        test_cases.append( InflTestHelper('A', 'fine', ('finer', 'finest')) )
        test_cases.append( InflTestHelper('A', 'clear', ('clearer', 'clearest')) )
        for word in test_cases:
            infl_dict = pyinflect.getAllInflectionsOOV(word.lemma, word.pos_type)
            msg = '\n%s\nCorrect : %s\nFunction: %s' %  (word.lemma, word.inflections, infl_dict)
            self.assertTrue( word.inflectionsInDict(infl_dict), msg)

    def testDoubledAdjs(self):
        test_cases = []
        test_cases.append( InflTestHelper('A', 'dim', ('dimmer', 'dimmest')) )
        test_cases.append( InflTestHelper('A', 'fit', ('fitter', 'fittest')) )
        test_cases.append( InflTestHelper('A', 'sad', ('sadder', 'saddest')) )
        for word in test_cases:
            infl_dict = pyinflect.getAllInflectionsOOV(word.lemma, word.pos_type)
            msg = '\n%s\nCorrect : %s\nFunction: %s' %  (word.lemma, word.inflections, infl_dict)
            self.assertTrue( word.inflectionsInDict(infl_dict, form_num=1), msg)

    def testRegularNouns(self):
        test_cases = []
        test_cases.append( InflTestHelper('N', 'fly', ('flies',)) )
        test_cases.append( InflTestHelper('N', 'illness', ('illnesses',)) )
        test_cases.append( InflTestHelper('N', 'waltz', ('waltzes',)) )
        test_cases.append( InflTestHelper('N', 'box', ('boxes',)) )
        test_cases.append( InflTestHelper('N', 'match', ('matches',)) )
        test_cases.append( InflTestHelper('N', 'splash', ('splashes',)) )
        test_cases.append( InflTestHelper('N', 'book', ('books',)) )
        for word in test_cases:
            infl_dict = pyinflect.getAllInflectionsOOV(word.lemma, word.pos_type)
            msg = '\n%s\nCorrect : %s\nFunction: %s' %  (word.lemma, word.inflections, infl_dict)
            self.assertTrue( word.inflectionsInDict(infl_dict), msg)

    def testGrecoNouns(self):
        test_cases = []
        test_cases.append( InflTestHelper('N', 'focus', ('foci',)) )
        test_cases.append( InflTestHelper('N', 'trauma', ('traumata',)) )
        test_cases.append( InflTestHelper('N', 'larva', ('larvae',)) )
        test_cases.append( InflTestHelper('N', 'ilium', ('ilia',)) )
        test_cases.append( InflTestHelper('N', 'taxon', ('taxa',)) )
        test_cases.append( InflTestHelper('N', 'analysis', ('analyses',)) )
        test_cases.append( InflTestHelper('N', 'cystis', ('cystides',)) )
        test_cases.append( InflTestHelper('N', 'foramen', ('foramina',)) )
        test_cases.append( InflTestHelper('N', 'index', ('indices',)) )
        test_cases.append( InflTestHelper('N', 'matrix', ('matrices',)) )
        for word in test_cases:
            infl_dict = pyinflect.getAllInflectionsOOV(word.lemma, word.pos_type)
            msg = '\n%s\nCorrect : %s\nFunction: %s' %  (word.lemma, word.inflections, infl_dict)
            self.assertTrue( word.inflectionsInDict(infl_dict, form_num=1), msg)

    def testGetInflection(self):
        self.assertEqual(pyinflect.getInflection('xxfocus', 'NN', inflect_oov=False), None)
        self.assertEqual(pyinflect.getInflection('xxfocus', 'NN', inflect_oov=True), ('xxfocus',))
        self.assertEqual(pyinflect.getInflection('xxfocus', 'NNS', inflect_oov=True),
            ('xxfocuses', 'xxfoci'))
        self.assertEqual(pyinflect.getInflection('xxban', 'VBG', inflect_oov=True),
            ('xxbaning', 'xxbanning'))
        self.assertEqual(pyinflect.getInflection('xxdim', 'JJR', inflect_oov=True),
            ('xxdimer', 'xxdimmer'))

    @unittest.skip("Skipping. SpaCy v2.2.3 lemmatizer error.  Switch to Lemminflect to fix.")
    def testSpacyGetInfl(self):
        tokens = self.nlp('xxtest this')
        self.assertEqual(tokens[0].lemma_, 'xxtest')    # spacy lemmatizer error (spacy v2.2.3)
        self.assertEqual(tokens[0]._.inflect('VBG', inflect_oov=False), None)
        self.assertEqual(tokens[0]._.inflect('VBG', inflect_oov=True), 'xxtesting')

    def testUseMethods(self):
        self.assertTrue(pyinflect.InflectionRules.useDoublingMethod('ban'))
        self.assertFalse(pyinflect.InflectionRules.useDoublingMethod('waltz'))
        self.assertTrue(pyinflect.InflectionRules.useGrecoMethod('focus'))
        self.assertFalse(pyinflect.InflectionRules.useGrecoMethod('fly'))


if __name__ == '__main__':
    # run all methods that start with 'test'
    unittest.main()
