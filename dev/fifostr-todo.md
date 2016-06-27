## fifostr todo list
#
#  (c) 2011 manu chatterjee 

check add/rem pattern functions
def addPattern: (pattern, function, opt_name_string) #default is class_var "match_type_n"



# future
-add array or dict of patterns  eg
	[
		[pattern1, callbackfn1, optname1,  pos_s, pos_e] ,
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

## Todo:
	[ ] constructor, take log-function #as in logging each event to log function
	[ ] add/del log-function
	[ ] pip installer
	[ ] tests.py / unit tests  #in tests directory
	[ ] check all functions have comments
	[ ] 
	[x] check Python 2.7+ and Python 3+ compatibility with tests
	[0] .eqHead, .eqTail, .eq --> accept str or regex #too complicate for now.. just use .all() etc
	[ ] test pattern add/del/triggers
	[ ] operator overloads #all currently not fully tested
	[ ] operators behave same as their base-class deque counter parts (e.g. see how list[] works realtive to str casting)
	[ ] __iadd__ (+=)
	[ ] __eq__ (=)
	[ ] append 		#with default inc=False 
	[ ] appendleft  #with default inc=False
	[ ] pop
	[ ] popleft
	[ ] reverse
	[ ] rotate
	[ ] __set_item__ #directly change one item (?)
	[ ]	proper markdown
	[ ] add pydoc strings to each function

## features list
	[x] head
	[x] tail
	[x] eqhead
	[x] eqtail
	[x] add/del/get pattern
	[x] clear all patterns
	[x] get/setPattern Active/Inactive
	[x] operators support slicing, indexing

