## fifostr todo list  
(c) 2011 manu chatterjee  
 
  
## pattern consists of:
	pattern 	: regex | str | function of pattern to trigger on
	callbackfn 	: function to call back when pattern found
		params are (matching_string_section) 
	optname 	: an optional label for when the pattern is found
	optlog		: optional to call logging fn when pattern hit (not-logged is default)
	pos_s		: start substring position to look for in fifostr (0 is default)
	pos_e		: end substring position to look for in fifostr (maxlen-1 is default)
	active		: whether this pattern is currently being interrogated

## features list
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
	[0] typeStr operator is "hidden" feature ## Todo: move test from example.py to tests dir
	
	[x] length indefinite support  #eg z=fifostr()  produces a fifostr of indefinite length
	[ ] pip installer
	[ ] tests.py / unit tests  #in tests directory
	[ ] check all functions have """docstring""" comments
	[x] check Python 2.7+ and Python 3+ compatibility with tests
	[x] .eqHead, .eqTail, .eq --> accept str or regex #too complicate for now.. just use .all() etc
	[x] test pattern add/del/triggers
	[o] operator overloads #all currently not fully tested
	[ ] operators behave same as their base-class deque counter parts (e.g. see how list[] works realtive to str casting)
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
	[ ]	proper markdown for README.md
	[ ] test and finish & fix example  portion in README.md, perhaps use example from python interpreter  
	[ ] add pydoc strings to each function  
	[ ] document callback function parameters (e.g. match str(s,e) passed, label passed)  
	[x] add bitbuck compliant double spaces at end of each line in readme  
	[x] allow ^ and $ to be used as anchors for any pattern 
	


## future
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