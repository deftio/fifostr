# fifostr todo list  
(c) 2011 manu chatterjee  packaged in 2016 

this file contains some free form thinking of things needed before fifostr can be 'published' via github or pip

much of the notes here are my internal thinking about what makes either a decent-enough complete module or good publishing hygene:
e.g

	- docs
	- tests
	- interface completeness
	- examples
	- lic & packaging


 
## features checklist (1.0.0)  -- what the module should do
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
	[x] typeStr operator is "hidden" feature ## Todo: move test from example.py to tests dir
	[x] __iadd__ (+=)
	[x] __eq__ (==)
	[x] append 		#with default inc=False  (increases fifostr by adding item on right)
	[x] appendleft  #with default inc=False  (increases fifostr by adding item on left)
	[x] pop 		#removes an item from right (returns right-most item, decreases fifostr by 1 item)
	[x] popleft		#removes an item from left with default inc=False  (returns left-most item, decreases fifostr by 1 item)
	[x] reverse     #transposes each element around center
	[x] rotate		#with default inc=False
	[x] remove      #remove item(s) with the supplied value
	[x] __set_item__ #directly change one item 
	[x] .eqHead, .eqTail, .eq --> accept str or regex #too complicated for regex for now.. just use .all() etc
	[x] test pattern add/del/triggers
	[x] document and check callback function parameters (e.g. match str(s,e) passed, label passed)  
	[x] allow ^ and $ to be used as start/end anchors for any pattern (useful for when fifostr is resized)
	[x] length indefinite support  #eg z=fifostr()  produces a fifostr of indefinite length
	[x] operator overloads 
	[x] operators behave same as their base-class deque counter parts (e.g. see how list[] etc works realtive to str casting)

### fundamental pattern consists of:
	pattern 	: regex | str | function of pattern to trigger on
	callbackfn 	: function to call when pattern found
		Arguments are (matching_string_section, label) 
	optname 	: an optional label for when the pattern is found
	pos_s		: start substring position to look for in fifostr (0 is default)
	pos_e		: end substring position to look for in fifostr (maxlen-1 is default)
	active		: whether this pattern is currently being interrogated
	optlog		: optional to call logging fn when pattern hit (not-logged is default) #feature deferred to future

## release housekeeping checklist  -- things to pack it up for release
	[x] license.txt file -- chose FreeBSD
	[ ] pip installer
	[x] create identity in pypi (pip online directory)
	[ ] tests.py / unit tests  #in /tests directory
	[x] check all functions have """docstring""" comments
	[x] function documentation in HTML in /docs directory --> accomplished with pydoc
	[x] check Python 2.7+ and Python 3+ compatibility with tests
	[x]	proper markdown for README.md
	[ ] test and finish & fix example  portion in README.md, perhaps use example from python interpreter  
	[x] add bitbucket compliant double spaces at end of each line in markdown files 
	

## future stuff 
	[ ] load/save array of patterns in one call (so can be stored to disk), note issue with serializing funcs
		[
			[pattern1, callbackfn1, optname1,  pos_s, pos_e] ,
			[pattern2, callbackfn2, optname1,  pos_s, pos_e] ,
		]
	[ ] make optimization of map() for patterns instead of loop  
		-keep "shadow" array of which patterns are active so as to remove check each time a char is added  
	[ ]  make all string patterns (patterns which are just passed as a string) converted to regex internally  
			note need to save the string in the pattern array holder so if a user does a "getPattern()" a string is returned  
	universal logging function support:
	[ ] add/del log-function  
	[ ] constructor, take log-function #as in logging each event to log function