#!/usr/bin/env bash
# this is bash shell script to run all the python packaging commands that I've read among the 4 different 'how to easily build a pypi package' guides
# IMHO the Python packaging community could learn a lot from the nodejs / npm community interms of ease of packaging... 
# ..and that's coming from a guy who's spent most of his time with C/C++ and assembly language!

if [ $# -eq 0 ]  # show command line options
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
	python3 setup.py sdist

	#then this
	python3 setup.py bdist_wheel --universal

	#this requires pandoc to be installed (on ubuntu sudo apt-get install pandoc)
	#pandoc --from=markdown --to=rst --output=README.rst README.md 
	#pandoc --from=markdown_strict --to=rst --output=README.rst README.md
	pandoc --from=gfm --to=rst --output=README.rst README.md
	pandoc README.md -f markdown -t html -o README-content.html
fi

#now try to upload..
#twine upload -r pypi dist/fifostr-1.0.0  #note pypi is the name given in the ~/.pypirc

if [ $1 == 'tests' ]
then
	#testing (in tests dir)
	##(cd ./tests && py.test --doctest-modules --cov ./test_fifostr -vv) ## OLD DEPRECATED
	(cd ./tests && py.test --doctest-modules --cov-report term --cov=fifostr -vv)  # was working
	#(cd ./tests && python3 -m pytest  -vv) ## OLD DEPRECATED
	#(cd ./tests && python -m pytest --doctest-modules --cov-report term --cov=fifostr -vv) ## works locally but not in travis for python 3.3
	(cd ./tests && python3 -m pytest --doctest-modules --cov-report term --cov=fifostr -vv) ## works locally but not in travis for python 3.3
fi

if [ $1 == 'upload-pypitest' ]
then
	# python setup.py sdist upload -r testpypi   # it works but not with markdown format documentation.
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
fi

if [ $1 == 'upload-pypi' ]
then
	# python setup.py sdist upload -r pypi  #old way works but not with markdown format documentation
	twine upload dist/*
fi

#./example.py
