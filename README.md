# pyinflect<br/>
**A python module for word inflections that works as a Spacy extension**

This module is based on the **[Automatically Generated Inflection Database (AGID)](http://wordlist.aspell.net/other)**.  The AGID data provides a list of inflections for various word lemma.

It is designed as an extension for **[Spacy](https://github.com/explosion/spaCy)** and will return the the inflected form of a word based on a supplied Penn Treekbank part-of-speech tag.  It can also be used a stanalone module outside of Spacy.

## Usage as an extension to Spacy
To use as an extension to Spacy, first import the module.  This will create a new `infect` method for each Spacy Token that takes in a Penn Treebank tag.  The method returns the inflected form of the token's lemma based on the supplied treekbank tag.

```
> import pyinflect
> doc = nlp('My example.')
> doc[1]._.inflect('NNS')
examples
```

## Usage Standalone
To use as a standalone module first import the `InflectionEngine` and then call the engine's `getInflection` method.
```
> from pyinflect import InflectionEngine
> InflectionEngine().getInflection('example', 'NNS')
examples
```

## Known Issues:
* Forms of the verb "be" are not completely specified by the treekbank tag.  When the inflected form is ambiguous, a list of possible candidates is returned.  This applies to "was"/"were" and "am"/"are".
* The AGID data is created by a 3rd party and not maintained here.  Some lemmas are not in that data file, infl.csv, and thus can not be inflected.
* In some cases the AGID may not contain the best inflection of the word.  For instance, lemma "people" with tag "NNS" will return "peoples" where you are likely to want the word "people" which is also plural.
