#!/usr/bin/python3
import setuptools

# There are currently no dependencies so this is fine but note that if
# dependencies are added, this is a bad technique because setup will
# fail if those aren't installed first.
from pyinflect import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyinflect',
    version=__version__,
    author='Brad Jascob',
    author_email='bjascob@msn.com',
    description='A python module for word inflections designed for use with Spacy.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bjascob/pyinflect',
    include_package_data=True,
    package_data={'':['*.csv']},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
)
