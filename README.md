# pyinflect<br/>
**A python module for word inflections that works as a Spacy extension**.

This module is designed as an extension for **[Spacy](https://github.com/explosion/spaCy)** and will return the the inflected form of a word based on a supplied Penn Treekbank part-of-speech tag.  It can also be used a stanalone module outside of Spacy. It is based on the **[Automatically Generated Inflection Database (AGID)](http://wordlist.aspell.net/other)**.  The AGID data provides a list of inflections for various word lemma. See the `scripts` directory for utilities that make good examples or the `tests` directory for unit tests / examples.

## Installation
```
pip3 install pyinflect
```

## Usage as an Extension to Spacy
To use with Spacy, you need Spacy version 2.0 or later.  Versions 1.9 and early do not support the extension methods used here.<br/>
To use as an extension to Spacy, first import the module.  This will create a new `inflect` method for each Spacy `Token` that takes in a Penn Treebank tag as its parameter.  The method returns the inflected form of the token's lemma based on the supplied treekbank tag.  When more than one spelling/form exists for the given tag, an optional form number parameter can be supplied, otherwise the first one is returned.

```
> import pyinflect
> doc = nlp('This is an example.')
> doc[3]._.inflect('NNS')
examples

> doc[1]._.inflect('VBD', 0)
was

> doc[1]._.inflect('VBD', 1)
were
```

## Usage Standalone
To use standalone, import the method `getAllInflections` and/or `getInflection` and call them directly.  `getAllInflections` returns all entries in the infl.csv file as a dictionary of inflected forms, where each form entry is a tuple with one or more spellings/forms for a given treebank tag.  The optional parameter `pos_type` (which is V, A or N) can be used to limited the returned data to specific parts of speech.  The method `getInflection` takes a lemma and a Penn Treebank tag and returns a tuple of the specific inflection(s) associated with it.
```
> from pyinflect import getAllInflections, getInflection
> getAllInflections('watch')
{'NN': ('watch',), 'NNS': ('watches',), 'VB': ('watch',), 'VBP': ('watch',), 'VBD': ('watched',), 'VBN': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',)}

> getAllInflections('watch', pos_type='V')
{'VB': ('watch',), 'VBP': ('watch',), 'VBD': ('watched',), 'VBN': ('watched',), 'VBG': ('watching',), 'VBZ': ('watches',)}

> getInflection('watch', tag='VBD')
('watched',)
```

## Issues:
If you find a bug, please report it on the **[GitHub issues list](https://github.com/bjascob/pyInflect/issues)**.  However, there are some inflections which are ambiguous because of different spellings or because multiple forms exist for the same lemma / treebank tag.  For these instances extra logic will need to be supplied by the user to determine which one to use.  Alternately the `overrides.csv` can be used to specify the preferred string the system returns.

See `KnownIssues.txt` for a list of lemma / inflections that may be problematic.

One common issues is that forms of the verb "be" are not completely specified by the treekbank tag.  When the inflected form is ambiguous the first person form is returned.  Setting the `form_num` to the Spacy inflection method allows returning the 2nd person version.

The AGID data is created by a 3rd party and not maintained here.  Some lemmas are not in that data file, `infl.csv`, and thus can not be inflected.  In some cases the AGID may not contain the best inflection of the word.  For instance, lemma "people" with tag "NNS" will return "peoples" where you may want the word "people" which is also plural.


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
