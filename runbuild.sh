#!/usr/bin/env bash
# bs bash script to run all the python packaging commands that I've read among the 4 different 'how to easily build a pypi package' guides
# IMHO the Python packaging community could learn a lot from the nodejs / npm community interms of ease of packaging... 
# ..and that's coming from a guy who's spent most of his time with C/C++

if [ $# -eq 0 ]
then
	echo "runbuild tests  # to test package"
	echo "runbuild build  # to build package"
	echo "runbuild upload-pypitest to publish to pypi test server"
	echo "runbuild upload-pypi to publish to pypi server (official release)"
	exit 0
fi

if [ $1 == 'build' ]  #don't forget the spaces.... its sh afterall..
then
	#first build this 
	python setup.py sdist

	#then this
	python setup.py bdist_wheel --universal
fi

#now try to upload..
#twine upload -r pypi dist/fifostr-1.0.0  #note pypi is the name given in the ~/.pypirc

if [ $1 == 'tests' ]
then
	#testing (in tests dir)
	#(cd ./tests && py.test -vv)
	(cd ./tests && py.test --doctest-modules --cov ./test_fifostr.py -vv)
	#(cd ./tests && python3 -m pytest  -vv)
	(cd ./tests && python3 -m pytest --doctest-modules --cov ./test_fifostr.py -vv)
fi

if [ $1 == 'upload-pypitest' ]
then
	python setup.py sdist upload -r testpypi 
fi

if [ $1 == 'upload-pypi' ]
then
	python setup.py sdist upload -r pypi
fi

#./example.py
