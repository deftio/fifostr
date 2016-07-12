"""
Test Harness for fifostr.py library class
"""

import sys
sys.path.insert(0, '..')

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

def testSimplePatternMatches():
	"""
	test simple direct pattern matches
	"""
	f = fifostr(10)
	pass

def testPatternStorageManagement():
	"""
	test adding/deleting setActive, finding stored patterns
	"""
	pass

def testStoredPatternMatches():
	"""
	test stored patterns against a fifostr object 
	"""
	pass


