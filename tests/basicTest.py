#!/usr/bin/python3
import sys
sys.path.insert(0, '..')    # make '..' first in the lib search path
import unittest
import spacy
import pyinflect


class basicTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(basicTest, self).__init__(*args, **kwargs)
        self.nlp = spacy.load('en_core_web_sm')

    def testSpacyInflect01(self):
        sent = 'I seem to be eating.'
        doc = self.nlp(sent)
        self.assertEqual(doc[0]._.inflect('PRP'), None)

        self.assertEqual(doc[1]._.inflect('VBN'), 'seemed')
        self.assertEqual(doc[1]._.inflect('VBD'), 'seemed')
        self.assertEqual(doc[1]._.inflect('VBG'), 'seeming')
        self.assertEqual(doc[1]._.inflect('VBZ'), 'seems')
        self.assertEqual(doc[1]._.inflect('VBP'), 'seem')
        self.assertEqual(doc[1]._.inflect('VB'),  'seem')

        self.assertEqual(doc[2]._.inflect('VB'),  None)

        self.assertEqual(doc[3]._.inflect('VB'),  'be')
        self.assertEqual(doc[3]._.inflect('VBD', 0), 'was')
        self.assertEqual(doc[3]._.inflect('VBD', 1), 'were')
        self.assertEqual(doc[3]._.inflect('VBN'), 'been')
        self.assertEqual(doc[3]._.inflect('VBG'), 'being')
        self.assertEqual(doc[3]._.inflect('VBP', 0),  'am')
        self.assertEqual(doc[3]._.inflect('VBP', 1), 'are')
        self.assertEqual(doc[3]._.inflect('VBZ'), 'is')

        self.assertEqual(doc[4]._.inflect('VBN'), 'eaten')
        self.assertEqual(doc[4]._.inflect('VBD'), 'ate')
        self.assertEqual(doc[4]._.inflect('VBG'), 'eating')
        self.assertEqual(doc[4]._.inflect('VBZ'), 'eats')
        self.assertEqual(doc[4]._.inflect('VBP'), 'eat')
        self.assertEqual(doc[4]._.inflect('VB'),  'eat')

    def testGetInfections01(self):
        self.assertEqual(pyinflect.getInflections('awake', 'V'),
            # default value returned from AGID
            #{'VB': ('awake',), 'VBP': ('awake',), 'VBD': ('awoke', 'awaked'),
            # 'VBN': ('awoken', 'awaked', 'awoke'), 'VBG': ('awaking',), 'VBZ': ('awakes',)})
            # Overrides modified return
            {'VB': ('awake',), 'VBP': ('awake',), 'VBD': ('awoke', 'awaked'),
             'VBN': ('awaked',), 'VBG': ('awaking',), 'VBZ': ('awakes',)})
        self.assertEqual(pyinflect.getInflections('awoke', 'V'), {})
        self.assertRaises(ValueError, pyinflect.getInflections, 'awake', 'VB')

    def testGetInflection02(self):
        self.assertEqual(pyinflect.getInflections('squirrel', tag='NN'),  {'NN': ('squirrel',)})
        self.assertEqual(pyinflect.getInflections('squirrel', tag='NNS'), {'NNS': ('squirrels', 'squirrel')})

    def testGetInflection03(self):
        self.assertEqual(pyinflect.getInflections('watch'),
            {'NN': ('watch',), 'NNS': ('watches',), 'VB': ('watch',), 'VBP': ('watch',), 'VBD': ('watched',),
             'VBN': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',)})
        self.assertEqual(pyinflect.getInflections('watch', pos_type='V'),
            {'VB': ('watch',), 'VBP': ('watch',), 'VBD': ('watched',), 'VBN': ('watched',),
             'VBG': ('watching',), 'VBZ': ('watches',)})
        self.assertEqual(pyinflect.getInflections('watch', tag='VBD'), {'VBD': ('watched',)})
        self.assertEqual(pyinflect.getInflections('watch', pos_type='A'), {})

    def testCapitalization01(self):
        doc = self.nlp('BRAd Is STANDING.')
        self.assertEqual(doc[0]._.inflect('NN'), 'Brad')
        self.assertEqual(doc[1]._.inflect('VB'), 'Be')
        self.assertEqual(doc[2]._.inflect('VB'), 'STAND')


if __name__ == '__main__':
    # run all methods that start with 'test'
    unittest.main()
