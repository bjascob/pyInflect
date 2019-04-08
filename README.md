# pyinflect<br/>
**A python module for word inflections that works as a Spacy extension**

This module is designed as an extension for **[Spacy](https://github.com/explosion/spaCy)** and will return the the inflected form of a word based on a supplied Penn Treekbank part-of-speech tag.  It can also be used a stanalone module outside of Spacy.

It is based on the **[Automatically Generated Inflection Database (AGID)](http://wordlist.aspell.net/other)**.  The AGID data provides a list of inflections for various word lemma.

See the `scripts` directory for examples and tests of the system or the `tests` directory for unit test examples.

## Installation
```
pip3 install pyinflect
```

## Usage as an Extension to Spacy
To use as an extension to Spacy, first import the module.  This will create a new `inflect` method for each Spacy `Token` that takes in a Penn Treebank tag as its parameter.  The method returns the inflected form of the token's lemma based on the supplied treekbank tag.  When more than one spelling exists for the inflection, only the first one is returned.

```
> import pyinflect
> doc = nlp('My example.')
> doc[1]._.inflect('NNS')
examples
```

## Usage Standalone
To use standalone, import the method `getAllInflections` or `getInflection` and call it directly.  `getAllInflections` returns all entries in the infl.csv file as a list of inflected forms, where each form entry is a tuple with one or more spellings. `getInflection` returns only the form that corresponds to the given treebank tag.
```
> from pyinflect import getAllInflections, getInflection
> getAllInflections('be', 'V')
[('was', 'wast'), ('were',), ('been',), ('being',), ('am',), ('are', 'art'), ('is',), ('are',)]

> getInflection('be', 'VBD')
('were',)
```

## Known Issues:
See KnownIssues.txt for more specifics.
* Forms of the verb "be" are not completely specified by the treekbank tag.  When the inflected form is ambiguous the first person form is returned.  Setting a flag to the method allows returning the 2nd person version of the inflection.  This only applies to the "was"/"were" and "am"/"are" forms of "be".
* The AGID data is created by a 3rd party and not maintained here.  Some lemmas are not in that data file, infl.csv, and thus can not be inflected.
* In some cases the AGID may not contain the best inflection of the word.  For instance, lemma "people" with tag "NNS" will return "peoples" where you may want the word "people" which is also plural.  There is an existing "overrides.csv" file which these can be added to if needed.
