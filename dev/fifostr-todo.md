## fifostr todo list
#
#  (c) 2011 manu chatterjee 

check add/rem pattern functions
def addPattern: (pattern, function, opt_name_string) #default is class_var "match_type_n"



#future
-add array or dict of patterns  eg
	[
		[pattern1, callbackfn1, optname1,  pos_s, pos_e] ,
		...
	]


##pattern consists of:
	pattern 	: regex | str | function of pattern to trigger on
	callbackfn 	: function to call back when pattern found
		params are (optname) #if supplied 
	optname 	: an optional label for when the pattern is found
	optlog		: optional to call logging fn when pattern hit (not-logged is default)
	pos_s		: start substring position to look for in fifostr (0 is default)
	pos_e		: end substring position to look for in fifostr (maxlen-1 is default)


##Todo:
-constructor 
	-take log-function #as in logging each event to log function
-add/del log-function
-pip install
-tests.py  #in tests directory
-override all __add__ etc functions so behaves correctly
-check all functions have comments
- usable documentation for when I forget how this works
-check patterns can use strings or regexes or function 
	-user_func(x) --> bool 
		e.g. []
-check Python 2.7+ and Python 3+ compatibility with tests
-.eqHead, .eqTail, .eq --> accept str or regex
