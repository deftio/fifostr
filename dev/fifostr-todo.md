# fifostr todo list  
(c) 2011 manu chatterjee  packaged in 2016 

this file contains some free form thinking of things needed before fifostr can be 'published' via github or pip

much of the notes here are my internal thinking about what makes either a decent-enough complete module or good publishing hygene

e.g
	- docs
	- tests
	- interface completeness
	- examples
	- license
	- packaging and dir structure

I'd released projects in other langauges but going the python packing release "process" has been interesting from a code-delievery point of view.

### features checklist (1.1.1)
    [ ] get Sphinx docs working
    [ ] use continuous build checkin such as .travis.yml
    [ ] auto convert python type long to FIFOStr (both typeStr, and in operators which convert numbers to string.  only applies to 2.7x )

### features checklist (1.1.0)
	[x] PEP8 compliant naming (FIFOStr)
	[x] 100% code coverage in tests

### features checklist (1.0.0)  -- what the module does
	[x] head
	[x] tail
	[x] eqhead
	[x] eqtail
	[x] add/del/get pattern
	[x] clear all patterns
	[x] get/setPattern also make Active/Inactive
	[x] pattern can be string
	[x] pattern can be compiled regex
	[x] pattern can be user parser function
	[x] operators support slicing, indexing
	[x] find a pattern by label using str or regex 
	[x] typeStr operator is "hidden" feature 
	[x] __iadd__ (+=) #add chars to fifostr right (note does not do resize), all chars added in 1 shot
	[x] __eq__ (==)  #compare fifostr as if it were a string
	[x] __get_item__ #operator overload  allows slicing, lists
	[x] __set_item__ #directly change one item # note, no enforcement if user passes a string longer than 1 char
	[x] __str__		#allow proper cast to str object
	[x] __add__     #allow fifostr to be added like a str object (myFifoStr + "this string")
	[x] __radd__    #allows fifostr to be added like str object ("this string" +myFifoStr)
	[x] append 		#with default inc=False  (increases fifostr by adding item(s) on right)
	[x] appendleft  #with default inc=False  (increases fifostr by adding item(s) on left)
	[x] pop 		#removes an item from right (returns right-most item, decreases fifostr by 1 item)
	[x] popleft		#removes an item from left with default inc=False  (returns left-most item, decreases fifostr by 1 item)
	[x] reverse     #flips each element around 'center'
	[x] rotate		#with default inc=False
	[x] remove      #remove item(s) with the supplied value
	[x] .eqHead, .eqTail, .eq 
	[x] test pattern add/del/triggers
	[x] document and check callback function parameters (e.g. match str(s,e) passed, label passed)  
	[x] allow ^ and $ to be used as start/end anchors for any pattern (useful for when fifostr is resized by append, appendleft, pop etc)
	[x] length indefinite support  #eg z=fifostr()  produces a fifostr of indefinite length
	[x] operators behave same as their base-class deque counter parts (e.g. see how list[] etc works realtive to str casting)
	[x] accept None as callback_function.  (allows user to just supply a parser function that does everything w/o needing callback to do work)

#### (note) fundamental pattern consists of:
	pattern 	: regex | str | function of pattern to trigger on
	callbackfn 	: function to call when pattern found
		Arguments are (matching_string_section, label) 
	optname 	: an optional label for when the pattern is found
	pos_s		: start substring position to look for in fifostr (0 is default)
	pos_e		: end substring position to look for in fifostr (maxlen-1 is default)
	active		: whether this pattern is currently being interrogated
	optlog		: optional to call logging fn when pattern hit (not-logged is default) #feature deferred to future

### release housekeeping checklist  -- things to pack it up for release
	[x] license.txt file -- chose FreeBSD
	[x] pip installer 
	[x] pip3 installer
	[x] create identity in pypi (pip online directory)
	[x] tests.py / unit tests  #in /tests directory, note callbacks are tested in example.py
	[x] 100% test coverage (1.1)
	[x] check all functions have """docstring""" comments
	[x] function documentation in HTML in /docs directory --> accomplished with pydoc  (apparently Pypi doesn't play with pydoc, requires Sphinx)
	[x] check Python 2.7+ and Python 3+ compatibility with tests
	[x]	proper markdown for README.md
	[x] test and finish & fix example  portion in README.md, perhaps use example from python interpreter  
	[x] add bitbucket compliant double spaces at end of each line in markdown files 
	[x] makefile - build, run tests, clean (e.g remove .pyc, *~), package
		../tests/pytest  #run tests  (be sure to run both python2, python3 )
		../docs/pydoc -w ../fifostr.py 
		../docs/zip fifostr-docs.zip *.html #documenation for upload to pypi.org
		python packaging once above done twine etc...
		make clean  #run makefile, remove *~, .pyc and other garbage


### future stuff .. could be never :)
	[ ] load/save array of patterns in one call (so can be stored to disk), note issue with dealing callback & parser funcs
		[
			[pattern1, callbackfn1, optname1,  pos_s, pos_e] ,
			[pattern2, callbackfn2, optname1,  pos_s, pos_e] ,
		]
	[ ] make optimization of map() for patterns instead of loop  
	[ ] keep "shadow" array of which patterns are active so as to remove check each time a char is added  
	[ ] make all string patterns (patterns which are just passed as a string) converted to regex internally  
			note need to save the string in the pattern array holder so if a user does a "getPattern()" a string is returned 
			then exec a master regex (for all matches) across fifostr "string" 
			note that when combining these stringified regexes we need to add offset bounds in to the regex construct
	[ ] universal logging function support: (allows one func which logs all changes and label hits to a stream - useful for debugging serial stuff)
		[ ] add/del log-function  callback
		[ ] allow filename also?  or perhaps just make a default log function which is included with FIFOStr.defaultLog(filename) which can be passed?
			or use typeStr() if FifoStr.addLogf(log) --> if log is a str open a file, if log is a function, use as callback
		[ ] constructor, take log-function #as in logging each event to log function 
	[ ] allow optional flush each time
	[ ] make standalone commandline app which allows patterns to be loaded from a user-spec'd file, takes streams as input, output logf output
	[ ] add continuous integration (e.g. travis-ci or jenkins for check-ins)