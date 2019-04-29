#!/usr/bin/python3
#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
import unittest
import pyinflect


# Just to faciliate testing
class InflTestHelper(object):
    def __init__(self, pos_type, lemma, forms):
        self.pos_type     = pos_type
        self.lemma        = lemma
        # Put the forms into a dictionary for easy comparion
        if pos_type == 'V':
            assert len(forms) == 3
            self.inflections = {'VBZ':forms[0], 'VBN':forms[1], 'VBG':forms[2]}
        elif pos_type == 'A':
            assert len(forms) == 2
            self.inflections = {'JJR':forms[0], 'JJS':forms[1]}
        elif pos_type == 'N':
            assert len(forms) == 1
            self.inflections = {'NNS':forms[0]}
        else:
            assert False, 'Invalid pos_type = %s' % pos_type

    def inflectionsInDict(self, form_dict, form_num=0):
        for tag, infl in self.inflections.items():
            if not infl == form_dict.get(tag, None)[form_num]:
                return False
        return True


# Class for test cases
class InflectionRulesTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(InflectionRulesTests, self).__init__(*args, **kwargs)

    def testPosTypeException(self):
        self.assertRaises(ValueError, pyinflect.getAllInflectionsOOV, 'test', 'X')

    def testCapitalization(self):
        test_cases = []
        test_cases.append( InflTestHelper('V', 'DISmiss', ('Dismisses', 'Dismissed','Dismissing')) )
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


if __name__ == '__main__':
    # run all methods that start with 'test'
    unittest.main()
