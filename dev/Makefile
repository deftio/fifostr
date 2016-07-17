#Makefile for fifostr.py


docs:
	pydoc -w ./fifostr.py
	mv fifostr.html docs
	zip ./docs/fifostr-docs.zip ./docs/*.html

test :
	py.test ./tests -vv
	python3 -m pytest  ./tests -vv

build:
	python setup.py sdist
	python setup.py bdist_wininst  #windows binary dist
	python setup.py bdist_rpm      #rpm version
	#python setup.py bdist --help-formats  #  (just for ref)

pushToPyPiTest:
	python setup.py sdist upload -r pypitest

publish:  
	python setup.py sdist upload -r pypi

clean :
	rm *.pyc 
	rm *~
