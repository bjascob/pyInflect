# pyinflect<br/>
**A python module for word inflections that works as a Spacy extension**

This module is based on the **[Automatically Generated Inflection Database (AGID)](http://wordlist.aspell.net/other)**.  The AGID data provides a list of inflections for various word lemma.

It is designed as an extension for **[Spacy](https://github.com/explosion/spaCy)** and will return the the inflected form of a word based on a supplied Penn Treekbank part-of-speech tag.  It can also be used a stanalone module outside of Spacy.

See the `scripts` directory for examples and tests of the system.

## Usage as an extension to Spacy
To use as an extension to Spacy, first import the module.  This will create a new `inflect` method for each Spacy Token that takes in a Penn Treebank tag.  The method returns the inflected form of the token's lemma based on the supplied treekbank tag.

```
> import pyinflect
> doc = nlp('My example.')
> doc[1]._.inflect('NNS')
examples
```

## Usage Standalone
To use standalone import the method `getInflection` and then call it directly.
```
> from pyinflect import getInflection
> getInflection('example', 'NNS')
examples
```

## Known Issues:
See KnownIssues.txt in the main directory for more specifics.
* Forms of the verb "be" is not completely specified by the treekbank tag.  When the inflected form is ambiguous, a list of possible candidates is returned.  This applies to "was"/"were" and "am"/"are".
* The AGID data is created by a 3rd party and not maintained here.  Some lemmas are not in that data file, infl.csv, and thus can not be inflected.
* In some cases the AGID may not contain the best inflection of the word.  For instance, lemma "people" with tag "NNS" will return "peoples" where you are likely to want the word "people" which is also plural.
