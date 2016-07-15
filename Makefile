#Makefile for fifostr.py


docs:
	pydoc -w ./fifostr.py
	mv fifostr.html docs
	zip ./docs/fifostr-docs.zip ./docs/*.html

test :
	py.test ./tests

clean :
	rm *.pyc 
	rm *~
