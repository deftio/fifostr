#!/usr/bin/env python

"""
Test Harness for fifostr.py library class
"""


import re

from  fifostr import *
#from collections import deque, Iterable

def testTypeStr():
	"""
	test internal "typeOf" function which is used for dynamically handling different pattern types
	"""
	myFifoStr = FIFOStr(5)
	assert myFifoStr.typeStr(123) == "int"  
	assert myFifoStr.typeStr("this") == "str"
	assert myFifoStr.typeStr(testTypeStr) == "function"
	pass

def testStrConstructor(): 
	"""
	test internal constructor using a string parameter
	"""
	testString = "this is a test string."
	myFifoStr = FIFOStr(testString)
	assert myFifoStr.all() == testString
	assert myFifoStr.head(4) == "this"
	assert myFifoStr.tail(4) == "ing."
	assert len(myFifoStr) == len(testString)
	myFifoStr += "more."
	assert len(myFifoStr) == len(testString) # should stay same length
	assert myFifoStr.eqtail("more.")
	pass

def testMisc():
	myFifoStr = FIFOStr(5)
	assert myFifoStr.iterable([2,4,5]) == True
	assert myFifoStr.iterable(3) == False

	myFifoStr += "abcdefg"
	assert myFifoStr.head(6) == "cdefg"  #ask for more items than are in the fifostr obj
	assert myFifoStr.tail(6) == "cdefg"  #ask for more items than are in the fifostr obj


	myFifoStr += "abcde"
	assert myFifoStr['$'] != "abcdef"
	assert myFifoStr['^'] != "abcdef"
	
	pass

def testSimpleBoundedLengthFIFOOperations():
	"""
	test basic fifostr operations ... adding chars and checking head/tail/full-str extractions
	"""
	f = FIFOStr(10)
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

	f += 1
	assert f.tail(1) == "1"

	f += 2.1
	assert f.tail(3) == "2.1"

	assert f[7:10] == "2.1"
	pass

def testSimpleUnBoundedLengthFIFOOperations():
	"""
	test basic fifostr operations where no maxlen is set
	"""
	f = FIFOStr() #no max length set
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

	f[3] = 'm' #test __setitem__
	assert f[3] == 'm'
	pass

def testIndexAndSlicing():
	f = FIFOStr(10)
	f+= "abcdefghij"
	assert f[3] == 'd'			#accepts integer index  
	assert f[1:4] =='bcd' 		#accepts slice 
	assert f[[1,4,2]] == 'bec'  #accepts list 
	assert f[1,3,4] == 'bde'	#accepts tuple
	assert f[-1] == 'j'         #accepts negative indexing
	assert f[-2:-1] == 'i'      #accepts slice w negative index
	assert f[-3:-1] == 'hi'     #accepts slice w negative index
	assert f['^':2] == 'ab'     #accepts begin of string symbol

def testSimplePatternMatches():
	"""
	test simple direct pattern matches
	"""
	f = FIFOStr()
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

	assert str(f) == "this and that"
	assert f+' other' == "this and that other"
	assert 'other ' +f == "other this and that"
	
	pass

def testStoredPatterns():
	"""
	test adding/deleting setActive, finding stored patterns
	"""

	#this is the callback function for the pattern matches.  We'll use this later 

	def logf(s,label=""):  
		assert len(s)!=0	#pragma: no cover
		print("callback-> match_str:"+s+"  label:"+label) #pragma: no cover


	#assert logf("foo","bar") != None

	#set up fifostr tests for patterns
	f = FIFOStr(5)
	f+= "123456"
	f.addPattern("234",logf,label="234 hit across whole string")
	f.addPattern("234",logf,start=0, end=len("234"),label="234 at start")
	f.addPattern("67890",logf,label="67890 hit as whole str")
	f.addPattern("def",logf,start=3,end=6,label="'def' btw 3,6")
	f.addPattern("345",logf, start="^", end="$", label=".. any hit across whole string")
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
					4: ["345","^","$",logf,".. any hit across whole string", True],
					5: [re.compile("[0-9]+"),0,"$",logf,"r1 hit",True],
					6: [re.compile("[a-z]|w+"),0,"$",logf,"r2 hit",True],
					7: [f1,0,"$",logf,"f1 hit",True],
					8: [f2,0,"$",logf,"f2 hit",True]
					}

	results = f.testAllPatterns() #test all the patterns added and are active #note pass doCallbacks=True to activate callback fns

	assert results == 					[
					[0, '234 hit across whole string', False],
					[1, '234 at start', True],
					[2, '67890 hit as whole str', False],
					[3, "'def' btw 3,6", False],
					[4, ".. any hit across whole string", False],
					[5, 'r1 hit', True],
					[6, 'r2 hit', False],
					[7, 'f1 hit', False],
					[8, 'f2 hit', False]]
	assert len(results)==9

	assert 8==f.delPattern(x1) #show deleting a pattern from the search
	pats = f.showPatterns() #get remaining patterns
	
	assert pats == {
				0: ["234",0,"$",logf,"234 hit across whole string",True],
				1: ["234",0,3,logf,"234 at start",True],
				2: ["67890",0,"$",logf,"67890 hit as whole str", True],
				3: ["def",3,6,logf,"'def' btw 3,6",True],
				4: ["345","^","$",logf,".. any hit across whole string", True],
				5: [re.compile("[0-9]+"),0,"$",logf,"r1 hit",True],
				6: [re.compile("[a-z]|w+"),0,"$",logf,"r2 hit",True],
				8: [f2,0,"$",logf,"f2 hit",True]
				}

	assert len(pats)==8

	f.setPatternActiveState(x2,False)  #show retrieving pattern by index and setting inactive
	assert f.getPattern(x2) == [f2,0,"$",logf,"f2 hit",False]

	assert f.getPattern(44) == None #check out of bounds

	assert f.getPatternActiveState(3) == True #check that this pattern is active
	assert f.getPatternActiveState(300) == -1 # coverage test -- show that if index is too big it returns -1
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

	assert f.append("123456",False) #== "23456"
	assert f.append("abcdef",True) 
	assert f.appendleft("123456",False)
	assert f.appendleft("abcdef",True) 
	
	assert f.extend("123456") 
	assert f.extendleft("abcdef")
	
	assert f.rotate(6,True) 
	assert f.rotate(6,False) 

	assert f.pop()
	assert len(f) == 4
	assert f.popleft()
	assert len(f) == 3

	assert f.remove('e')
	assert f.reverse()
	f[1] = 'z' #test pattern triggers on __set_item__

	#end of pattern management -- finding a stored pattern 


	#now beging actual pattern matching and triggers
	#f = FIFOStr(5)  #just simpler for testing purposes

	f+= "12345"

	#and finally demonstrate that patterns auto-trigger when items inserted in fifostr .. which afterall
	#is the point of the whole thing.. ;)
	cs = '67890abcdefghijklmnop'
	i = 0

	
	f += cs[i]  # do it one char at a time so we can see the matches
	i += 1
	f += cs[i]  # do it one char at a time so we can see the matches
	i += 1
	
	#and finally clear out the patterns..
	assert f.clearPatterns() == 0
	#to see hit and callback testing testing look at example.py
	pass

	
#test version if for  ode coverage testing -- just eliminate false positives by checking that version info is returned from the library
def testVer():
	f=FIFOStr()
	v = f.ver()
	assert len(v["version_str"]) > 0
	assert len(v["version"]) > 0
	assert len(v["url"]) > 0



def testdisphook():
	FIFOStr.fifodisplay(123)
	a = FIFOStr("testing display hook")
	FIFOStr.fifodisplay(a)
	