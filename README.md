# pyinflect<br/>
**A python module for word inflections that works as a spaCy extension**.

This module is designed as an extension for **[spaCy](https://github.com/explosion/spaCy)** and will return the the inflected form of a word based on a supplied Penn Treekbank part-of-speech tag.  It can also be used a standalone module outside of Spacy. It is based on the **[Automatically Generated Inflection Database (AGID)](http://wordlist.aspell.net/other)**.  The AGID data provides a list of inflections for various word lemma. See the `scripts` directory for utilities that make good examples or the `tests` directory for unit tests / examples.

## Installation
```
pip3 install pyinflect
```

## Usage as an Extension to Spacy
To use with Spacy, you need Spacy version 2.0 or later.  Versions 1.9 and earlier do not support the extension methods used here.

To use as an extension to Spacy, first import the module.  This will create a new `inflect` method for each spaCy `Token` that takes a Penn Treebank tag as its parameter.  The method returns the inflected form of the token's lemma based on the supplied treekbank tag.
```
> import spacy
> import pyinflect
> nlp = spacy.load('en_core_web_sm')
> tokens = nlp('This is an example of xxtest.')
> tokens[3]._.inflect('NNS')
examples
```
When more than one spelling/form exists for the given tag, an optional form number can be supplied, otherwise the first one is returned.
```
> tokens[1]._.inflect('VBD', form_num=0)
was
> tokens[1]._.inflect('VBD', form_num=1)
were
```
When the lemma you wish to inflect is not in the lookup dictionary, the method returns `None`.  The optional parameter `inflect_oov` can be used to inflect the word using regular inflection rules.  In this case `form_num=0` selects the "regular" inflection and `form_num=1` selects the "doubled" version for verbs and adj/adv or the "Greco-Latin" for nouns.
```
> tokens[5]._.inflect('VBG', inflect_oov=True)
xxtesting
> tokens[5]._.inflect('VBG', inflect_oov=True, form_num=1)
xxtestting
```
You will need to figure out yourself which form_num to use.  There are basic helper functions in `pyinflect.InflectionRules` which can make a guess if the lemma uses "doubling" or "Greco-Latin" style rules.


## Usage Standalone
To use standalone, import the method `getAllInflections` and/or `getInflection` and call them directly.  `getAllInflections` returns all entries in the `infl.csv` file as a dictionary of inflected forms, where each form entry is a tuple with one or more spellings/forms for a given treebank tag.  The optional parameter `pos_type` (which is V, A or N) can be used to limited the returned data to specific parts of speech.  The method `getInflection` takes a lemma and a Penn Treebank tag and returns a tuple of the specific inflection(s) associated with it.
```
> from pyinflect import getAllInflections, getInflection
> getAllInflections('watch')
{'NN': ('watch',), 'NNS': ('watches',), 'VB': ('watch',), 'VBP': ('watch',), 'VBD': ('watched',), 'VBN': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',)}

> getAllInflections('watch', pos_type='V')
{'VB': ('watch',), 'VBP': ('watch',), 'VBD': ('watched',), 'VBN': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',)}

> getInflection('watch', tag='VBD')
('watched',)
```
The method `getInflection` takes the parameter `inflect_oov` and uses it similarly to what is described above with spaCy.
```
> getInflection('xxtest', 'VBG', inflect_oov=True)
('xxtesting', 'xxtestting')
```

## Issues:
If you find a bug, please report it on the **[GitHub issues list](https://github.com/bjascob/pyInflect/issues)**.  However be aware that when in comes to returning the correct inflection there are a number of different types of issues that can arise.  Some of these are not  readily fixable.  Issues with inflected forms include...
* Multiple spellings for an inflection (ie.. arthroplasties, arthroplastyes or arthroplastys)
* Mass form and plural types (ie.. people vs peoples)
* Forms that depend on context (ie.. further vs farther)
* Infections that are not fully specified by the tag (ie.. be/VBD can be "was" or "were")
* Incorrect lemmatization from spaCy (ie.. hating -> hat')
* Incorrect tagging (ie.. VBN vs. VBD)
* Errors in the AGID database

In order to assure that pyInflect returns the most commonly used inflected form/spelling for a given tag, a corpus technique is used.  In `scripts/12_CreateOverridesList.py`, words are lemmatized and tagged with spaCy then re-inflected with pyInflect.  When the original corpus word differs from pyInflect, the most commonly seen form is written to the `overrides.csv` file.  This technique can also help overcome lemmatization and tagging issues from spaCy and errors in the AGID database.  The file `CorpMultiInfls.txt` is a list of inflections/tags that came from multiple words in the corpus and thus may be problematic.

One common issue is that some forms of the verb "be" are not completely specified by the treekbank tag.  For instance be/VBD inflects to either "was" or "were" and be/VBP inflects to either "am", or "are". When the inflected form is ambiguous the first form is returned by default.  Setting the `form_num` in the Spacy inflection method allows returning other form(s).

Note that the AGID data is created by a 3rd party and not maintained here.  Some lemma are not in that data file, `infl.csv`, and thus can not be inflected using the dictionary methods.  In some cases the AGID may not contain the best inflection of the word.  For instance, lemma "people" with tag "NNS" will return "peoples" (pre-overrides) where you may want the word "people" which is also plural.


## Tags:
The module determines the inflection(s) returned by either a `pos_type` or a Penn Treebank `tag`.  The `pos_type` is either 'V', A' or 'N' for 'Verb', 'Adjective'/'Adverb' or 'Noun' respectively.  A list of treebank tags can be found **[here](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)**.  Not all of these are used by pyinflect.  The following is a list of the various types and tags used...

    pos_type = 'A'
    * JJ      Adjective
    * JJR     Adjective, comparative
    * JJS     Adjective, superlative
    * RB      Adverb
    * RBR     Adverb, comparative
    * RBS     Adverb, superlative

    pos_type = 'N'
    * NN      Noun, singular or mass
    * NNS     Noun, plural

    pos_type = 'V'
    * VB      Verb, base form
    * VBD     Verb, past tense
    * VBG     Verb, gerund or present participle
    * VBN     Verb, past participle
    * VBP     Verb, non-3rd person singular present
    * VBZ     Verb, 3rd person singular present
    * MD      Modal
