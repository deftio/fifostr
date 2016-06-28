## fifostr todo list
#
#  (c) 2011 manu chatterjee 

check add/rem pattern functions
def addPattern: (pattern, function, opt_name_string) #default is class_var "match_type_n"


	...
	]

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
	[x] get/setPattern Active/Inactive
	[x] pattern can be string
	[x] pattern can be compiled regex
	[x] pattern can be user parser function
	[x] operators support slicing, indexing
	[0] typeStr operator is "hidden" feature ## Todo: move test from example.py to tests dir
	[ ] constructor, take log-function #as in logging each event to log function
	[ ] length indefinite support
	[ ] add/del log-function
	[ ] pip installer
	[ ] tests.py / unit tests  #in tests directory
	[ ] check all functions have """docstring""" comments
	[x] check Python 2.7+ and Python 3+ compatibility with tests
	[0] .eqHead, .eqTail, .eq --> accept str or regex #too complicate for now.. just use .all() etc
	[x] test pattern add/del/triggers
	[ ] operator overloads #all currently not fully tested
	[ ] operators behave same as their base-class deque counter parts (e.g. see how list[] works realtive to str casting)
	[ ] __iadd__ (+=)
	[ ] __eq__ (=)
	[ ] append 		#with default inc=False 
	[ ] appendleft  #with default inc=False
	[ ] pop
	[ ] popleft		#with default inc=False
	[ ] reverse
	[ ] rotate		#with default inc=False
	[ ] __set_item__ #directly change one item (?)
	[ ]	proper markdown for README.md
	[ ] test and finish & fix example  portion in README.md, perhaps use example from python interpreter
	[ ] add pydoc strings to each function
	[ ] add,rotate, etc accept case where Inc=True and item is not iterable?
	[ ] document callback function parameters (e.g. match str passed, label passed)



# future
-add an array of patterns  eg 
	[
		[pattern1, callbackfn1, optname1,  pos_s, pos_e] ,
		[pattern2, callbackfn2, optname1,  pos_s, pos_e] ,
	