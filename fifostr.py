#!/usr/bin/env python
"""
	fifostr.py - A FIFO for strings derived from deque
	
	@copy Copyright (C) <2012>  <M. A. Chatterjee>
	
	@author M A Chatterjee, deftio [at] deftio [dot] com
	
	This software is provided 'as-is', without any express or implied
	warranty. In no event will the authors be held liable for any damages
	arising from the use of this software.

	Permission is granted to anyone to use this software for any purpose,
	including commercial applications, and to alter it and redistribute it
	freely, subject to the following restrictions:

	1. The origin of this software must not be misrepresented; you must not
	claim that you wrote the original software. If you use this software
	in a product, an acknowledgment in the product documentation is required.

	2. Altered source versions must be plainly marked as such, and must not be
	misrepresented as being the original software.

	3. This notice may not be removed or altered from any source
	distribution.

	#this class should work on either python 2.7+ or python 3+ distributions
	#for performance notes see README.md
"""

from collections import deque
import re 
import itertools

#Simple FIFO (First-In-First-Out) for strings --> allows rolling FIFO of last n chars seen
#use addPattern() / delPattern() to add/delete patterns to look for in the fifo
#patterns can be strings, regular expressions (regex), or a user-supplied-function provided that
#the function takes a string, returns a bool

class FIFOStr(deque):
	def __init__(self, size):
		super( FIFOStr, self ).__init__(maxlen=size) #inheritance from deque
		self.patterns = {} 

	#hackish internal typeOf Operator... takes certain types and returns string equivalent
	def typeStr(self,x):
		xt = str(type(x))
		def f(): return
		t = {
			str(type(123))	:"int",
			str(type(0.1)) : "float",
			str(type(re.compile(""))): "regex",
			str(type(self.head)):"function", #note type is 'instancemethod'
			str(type(f)):"function",
			str(type("")):"str"
		}
		if (xt) in t:
			return t[xt]
		return xt

    #head, tail, all operations ==============================================
	def head(self,l=1):
		if len(self)<l: 
		    l=len(self)
		return "".join([self[i] for i in range(l)])
    
	def tail(self,l=1):
		if len(self)<l: 
		    l=len(self)
		return "".join([self[i] for i in range(len(self)-l,len(self))])
    
	def all(self):
		return "".join(self)

	#simple tests for equality at head/tail/all given a string ===============
	def eqhead(self,instring):
		return self.head(len(instring))==instring    
    
	def eqtail(self,instring):
		return self.tail(len(instring))==instring

	def eq(self,instring):
		return self.all()==instring

	#operators================================================================
	def append(self,x,inc): #inc is bool, whether to ingest all of x at once (normal) or 1 at a time
		print (x)
		return deque.append(self,x)

	def __iadd__(self,x)		:
		#todo do pattern handling
		return deque.__iadd__(self,x)

	def __getitem__(self, index): #add slicing support ... its a "string" after all ;)
		#print("--->",index,type(index)) #debug
		if isinstance(index, slice):
			return "".join(itertools.islice(self, index.start, index.stop, index.step))
		if isinstance(index, list):
			return "".join([deque.__getitem__(self, x) for x in index])
		if isinstance(index, tuple):
			return "".join([deque.__getitem__(self, x) for x in index]			)
		return str(deque.__getitem__(self, index))

	#pattern handling==========================================================
	def testPattern(self,pattern, callbackfn, start=0,end='end',label="",log=False):
		if (end=='end'):
			end=len(self)
		pt = self.typeStr(pattern)
		if (pt=="str"):
			print (pattern,pt)
		elif (pt=="regex"):
			print (pattern,pt)
		elif (pt=="function"):
			print (pattern,pt)
		#else pattern is not allowable type...
		return -1
		print (start,end)

	def addPattern(self):
		return ""

	def delPattern(self):
		return ""

	def showPatterns(self):
		return ""

	def clearPatterns(self):
		return ""

"""
#see examples.py for complete examples in use.
#these examples commented out below are just for getting started.
def main():
	#simple examples...
	myFifoStr=FIFOStr(5)
	print "myFifoStr=FIFOStr(5) ==>",myFifoStr
	myFifoStr+='1234567'
	print "print myFifoStr+='1234567' ==>",myFifoStr
	print "myFifoStr.head(3)= ",myFifoStr.head(3)
	print "myFifoStr.tail(4)= ",myFifoStr.tail(4)
	print "myFifoStr.head(10)=",myFifoStr.head(10)
	print "myFifoStr.tail(10)=",myFifoStr.tail(10)
	print "len(myFifoStr)=",len(myFifoStr)
	print "myFifoStr.eqhead(\"3456\")=",myFifoStr.eqhead("3456")
	print "myFifoStr.eqhead(\"567\")=",myFifoStr.eqhead("567")
	print "myFifoStr.eqtail(\"4567\")=",myFifoStr.eqtail("4567")
	print "myFifoStr.eqtail(\"abc\")=",myFifoStr.eqtail("abc")
	myFifoStr+='890'
	print "myFifoStr+='890 ===>'",myFifoStr
	print "myFifoStr.head(3)= ",myFifoStr.head(3)
	print "myFifoStr.tail(4)= ",myFifoStr.tail(4)
	print "myFifoStr.head(10)=",myFifoStr.head(10)
	print "myFifoStr.tail(10)=",myFifoStr.tail(10)
	

if __name__ == '__main__':
    main()
"""