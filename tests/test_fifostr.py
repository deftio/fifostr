"""
Test Harness for fifostr.py library class
"""

import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../fifostr')

from fifostr import *

def testTypeStr():
	"""
	test internal "typeOf" function which is used for dynamically handling different pattern types
	"""
	myFifoStr = fifostr(5)
	assert myFifoStr.typeStr(123) == "int"  
	assert myFifoStr.typeStr("this") == "str"
	assert myFifoStr.typeStr(testTypeStr) == "function"

def testSimpleBoundedLengthFIFOOperations():
	"""
	test basic fifostr operations ... adding chars and checking head/tail/full-str extractions
	"""
	f = fifostr(10)
	f += "abc"
	assert f.all() == 'abc'
	assert f == 'abc'
	assert f.head(2) == 'ab'
	assert f.tail(2) == 'bc'
	f+= "defghijk"  		 #test the += operator
	assert f== "bcdefghijk"  #test the == operator
	assert f.eqhead("bcd") 
	assert f.eqhead("def") == False
	assert f.eqtail("hijk")
	assert f.eqtail("d23") == False
	assert f.eq("bcdefghijk")  #match full str
	assert f.eq("woeic") == False
	assert f.maxlen == 10  #this is what set earlier
	assert len(f) == 10
	f.append( '1')
	assert f== "cdefghijk1"
	f.append('234',True)
	assert f== "fghijk1234"
	f.appendleft('0')
	assert f== "0fghijk123"
	f.appendleft('zxc',True)
	assert f== "cxz0fghijk"
	assert len(f) == 10
	f.rotate(1)
	assert f== "kcxz0fghij"
	f.rotate(-3)
	assert f== "z0fghijkcx"
	x=f.pop()
	assert f== "z0fghijkc" and x=="x"
	x=f.popleft() 
	assert f== "0fghijkc" and x=="z"
	pass

def testSimpleUnBoundedLengthFIFOOperations():
	"""
	test basic fifostr operations where no maxlen is set
	"""
	f = fifostr() #no max length set
	f += "abc"
	assert f.all() == 'abc'
	assert f == 'abc'
	assert f.head(2) == 'ab'
	assert f.tail(2) == 'bc'
	f+= "defghijk"				#test the += operator
	assert f== "abcdefghijk"    #test the == operator
	assert f.eqhead("abcd") 
	assert f.eqhead("def") == False
	assert f.eqtail("hijk")
	assert f.eqtail("d23") == False
	assert f.eq("abcdefghijk")  #match full str
	assert f.eq("woeic") == False
	assert len(f) == 11
	f.append( '1')
	assert f== "abcdefghijk1"
	f.append('234',True)
	assert f== "abcdefghijk1234"
	f.appendleft('0')
	assert f== "0abcdefghijk1234"
	f.appendleft('zxc',True)
	assert f== "cxz0abcdefghijk1234"
	assert len(f) == 19	
	f.rotate(1)
	assert f== "4cxz0abcdefghijk123"
	f.rotate(-3)
	assert f== "z0abcdefghijk1234cx"
	pass

def testIndexAndSlicing():
	f = fifostr(10)
	f+= "abcdefghij"
	assert f[3] == 'd'			#accepts integer index  
	assert f[1:4] =='bcd' 		#accepts slice 
	assert f[[1,4,2]] == 'bec'  #accepts list 
	assert f[1,3,4] == 'bde'	#accepts tuple

def testSimplePatternMatches():
	"""
	test simple direct pattern matches
	"""
	f = fifostr()
	f += 'this and that'
	assert f.testPattern('this',0,4) == True
	assert f.testPattern('67890') == False

	#regexes
	r1=re.compile("[0-9]+")
	f.testPattern(r1) == False
	r2=re.compile("[a-z]|w+")
	f.testPattern(r2)
	
	#functions which act as parsers  (note since using callback these functions must return True if match foud or False if no match)
	def f1(s):
		return s=='this and that'
	assert f.testPattern(f1) == True

	def f2(s):
		return s=='67890'		
	assert f.testPattern(f2) == False
	pass

def testStoredPatterns():
	"""
	test adding/deleting setActive, finding stored patterns
	"""

	#this is the callback function for the pattern matches.  We'll use this later 

	def logf(matchStr,label):
		pass

	#set up fifostr tests for patterns
	f = fifostr(5)
	f+= "123456"
	f.addPattern("234",logf,label="234 hit across whole string")
	f.addPattern("234",logf,start=0, end=len("234"),label="234 at start")
	f.addPattern("67890",logf,label="67890 hit as whole str")
	f.addPattern('def',logf,start=3,end=6,label="'def' btw 3,6")
		#regexes
	r1=re.compile("[0-9]+")
	r2=re.compile("[a-z]|w+")
	f.addPattern(r1,logf,label="r1 hit")
	f.addPattern(r2,logf,label="r2 hit")

	def f1(s):
		return s=='this and that'
	def f2(s):
		return s=='67890'		
	x1=f.addPattern(f1,logf,label="f1 hit")
	x2=f.addPattern(f2,logf,label="f2 hit")
	#f.showPatterns()
	pats = f.showPatterns()

	#check to see if all patterns got stored
	assert pats == {
					0: ["234",0,"$",logf,"234 hit across whole string",True],
					1: ["234",0,3,logf,"234 at start",True],
					2: ["67890",0,"$",logf,"67890 hit as whole str", True],
					3: ["def",3,6,logf,"'def' btw 3,6",True],
					4: [re.compile("[0-9]+"),0,"$",logf,"r1 hit",True],
					5: [re.compile("[a-z]|w+"),0,"$",logf,"r2 hit",True],
					6: [f1,0,"$",logf,"f1 hit",True],
					7: [f2,0,"$",logf,"f2 hit",True]
					}

	results = f.testAllPatterns() #test all the patterns added and are active #note pass doCallbacks=True to activate callback fns

	assert results == 					[
					[0, '234 hit across whole string', False],
					[1, '234 at start', True],
					[2, '67890 hit as whole str', False],
					[3, "'def' btw 3,6", False],
					[4, 'r1 hit', True],
					[5, 'r2 hit', False],
					[6, 'f1 hit', False],
					[7, 'f2 hit', False]]
	assert len(results)==8

	assert 7==f.delPattern(x1) #show deleting a pattern from the search
	pats = f.showPatterns() #get remaining patterns
	
	assert pats == {
				0: ["234",0,"$",logf,"234 hit across whole string",True],
				1: ["234",0,3,logf,"234 at start",True],
				2: ["67890",0,"$",logf,"67890 hit as whole str", True],
				3: ["def",3,6,logf,"'def' btw 3,6",True],
				4: [re.compile("[0-9]+"),0,"$",logf,"r1 hit",True],
				5: [re.compile("[a-z]|w+"),0,"$",logf,"r2 hit",True],
				7: [f2,0,"$",logf,"f2 hit",True]
				}

	assert len(pats)==7

	f.setPatternActiveState(x2,False)  #show retrieving pattern by index and setting inactive
	assert f.getPattern(x2) == [f2,0,"$",logf,"f2 hit",False]

	#end pattern management deleting / adding etc

	#find a stored pattern..
	#now show searching for stored pattern matchers in the pattern dict
	#this is not searching the fifo-string itself, just the stored patterns that we have entered
	assert f.findPatternByLabel("foo") == [] #no matches returns empty list
	assert f.findPatternByLabel("234 at start") ==  [["234",0,3,logf,"234 at start",True]] #shows match	
	assert f.findPatternByLabel(re.compile("[rf][0-9]")) == [
				 [re.compile("[0-9]+"),0,"$",logf,"r1 hit",True],
				 [re.compile("[a-z]|w+"),0,"$",logf,"r2 hit",True],
				 [f2,0,"$",logf,"f2 hit",False]
				]
	#end of pattern management -- finding a stored pattern 


	#now beging actual pattern matching and triggers
	f = fifostr(5)  #just simpler for testing purposes

	f+= "12345"

	#and finally demonstrate that patterns auto-trigger when items inserted in fifostr .. which afterall
	#is the point of the whole thing.. ;)
	cs = '67890abcdefghijklmnop'
	i = 0

	
	f += cs[i]  # do it one char at a time so we can see the matches
	i += 1
	f += cs[i]  # do it one char at a time so we can see the matches
	i += 1
	
	#to see hit and callback testing testing look at example.py
	pass

	

