
Sphinx
------
The documentation in this directory uses sphinx.  To install do..
sudo apt-get install python-sphinx


Build
-----
To build the documents do..
make rst
make html   (or any other target)
Note that there is a warning during the build which doesn't apear to hurt anything...
    checking consistency... xx/docs/source/modules.rst: WARNING: document isn't included in any toctree


To view 
-------
As example do..
firefox build/html/index.html


For first-time setup/config
---------------------------
Nice directions at https://developer.ridgerun.com/wiki/index.php/How_to_generate_sphinx_documentation_for_python_code_running_in_an_embedded_system

mkdir docs
cd docs

sphinx-quickstart (use default for all except...)
    > Separate source and build directories (y/n) [n]: y
    > autodoc: automatically insert docstrings from modules (y/n) [n]: y
    > viewcode: include links to the source code of documented Python objects (y/n) [n]: y
    > Create Windows command file? (y/n) [y]: n

edit source/config.py
    At the top uncomment the import os and sys lines
    uncomment sys.path.insert and change to '../..'
    Under extesions add 'sphinxcontrib.napoleon'

edit Makefile and add (be sure to use tabs not spaces)..
    rst:
        sphinx-apidoc -f -o ./source/ .. ../setup.py
    clean:
        rm -f ./source/setup.rst
        rm -f ./source/pyinflect.rst
        rm -f ./source/modules.rst
        rm -rf build

touch _static/.gitkeep
touch _templates/.gitkeep

