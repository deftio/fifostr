#!/usr/bin/env bash
# bs bash script to run all the python packaging commands that I've read among the 4 different 'how to easily build a pypi package' guides
# IMHO the Python packaging community could learn a lot from the nodejs / npm community interms of ease of packaging... 
# ..and that's coming from a guy who's spent most of his time with C/C++

#first build this 
python setup.py sdist

#then this
python setup.py bdist_wheel --universal

#now try to upload..
#twine upload -r pypitest dist/fifostr-1.0.0  #note pypitest is the name given in the ~/.pypirc


#testing (in tests dir)
#py.test -vv
#python3 -m pytest  -vv
#./example.py