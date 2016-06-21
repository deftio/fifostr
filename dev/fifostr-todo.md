## fifostr todo list
#
#  (c) 2011 manu chatterjee 

check add/rem pattern functions
def addPattern: (pattern, function, opt_name_string) #default is class_var "match_type_n"

rem ()


-check all functions have comments
- usable ocumentation for when I forget how this works
-check patterns can use strings or regexes
-check Python 2.7+ and Python 3+ compatibility with tests


#future
-add array or dict of patterns  eg
	[
		[pattern1, callbackfn1, optname1,  pos_s, pos_e] 
		pattern2 : fn2,
		etc
	]


##pattern consists of:
	pattern 	: regex or string of pattern to trigger on
	callbackfn 	: function to call back when pattern found
		params are (optname) #if supplied 
	optname 	: an optional label for when the pattern is found
	pos_s		: substring position to look for in fifostr (0 is default)
	pos_e		: 


##Todo:
-pip install
-tests.py  #in tests directory
-override all __add__ etc functions so behaves correctly
