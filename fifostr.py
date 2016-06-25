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

#Simple constant ENUM style generator used for indexing internal pattern storage array
def enum(**enums):
    return type('Enum', (), enums)
PATIDX = enum(PATTERN=0, START=1, END=2, CALLBACKFN=3, LABEL=4, ACTIVE=5) #used internally

#Simple FIFO (First-In-First-Out) for strings --> allows rolling FIFO of last n chars seen
#use addPattern() / delPattern() to add/delete patterns to look for in the fifo
#patterns can be strings, regular expressions (regex), or a user-supplied-function provided that
#the function takes a string, returns a bool

class fifostr(deque):
	def __init__(self, size):
		super( fifostr, self ).__init__(maxlen=size) #inheritance from deque
		self.patterns 	= {} #dict of patterns to search for
		self.patternIdx = 0

	#hackish internal typeOf Operator... takes certain types and returns string equivalent
	def typeStr(self,x):
		xt = str(type(x))
		def f(): return
		t = {
			str(type(123))	:"int",
			str(type(0.1)) : "float",
			str(type(re.compile(""))): "regex",
			str(type(self.head)):"function", #note raw type is 'instancemethod'
			str(type(f)):"function",
			str(type("")):"str",
			str(type(fifostr)):"class"
		}
		if (xt) in t:
			return t[xt]
		return xt

    #head,tail,all operations ==============================================
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
		#todo do pattern handling
		return deque.append(self,x)

	def __iadd__(self,x)		:
		#todo do pattern handling
		deque.__iadd__(self,x)
		self.testAllPatterns(doCallbacks=True,retnList=False)
		return self

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
	def testPattern(self, pattern, start=0,end='e'): #test if a pattern matches btw start and end positions in fifostr
		if (end=='e'):
			end=len(self)
		s=self[start:end]		
		pt = self.typeStr(pattern)
		#cheesy dynamic type handling here...  
		if (pt=="str"):  		#test match if pattern is == string 
			if pattern==s:
				return True
		elif (pt=="regex"): 	#if the regex matches using re.search() return True
			if pattern.search(s) != None:
				return True
		elif (pt=="function"):  #if its a function then we pass the string to the function
			return pattern(s)==True #enforces primitive casting to boolean
		#else pattern is not allowable type...
		return False

	def testAllPatterns(self,doCallbacks=False,retnList=True): #checks all active patterns, returns result as list [index,label,<result>]
		l = []
		for i in self.patterns:
			if (self.patterns[i][PATIDX.ACTIVE]): #is an active pattern 
				e = self.patterns[i][PATIDX.END]
				if e == 'e':
					e=len(self)
				r=self.testPattern(self.patterns[i][PATIDX.PATTERN],self.patterns[i][PATIDX.START],e)
				l.append([i,self.patterns[i][PATIDX.LABEL],r])
				if (doCallbacks):
					if r:
						self.patterns[i][PATIDX.CALLBACKFN](self[self.patterns[i][PATIDX.START]:e],self.patterns[i][PATIDX.LABEL])
		if retnList:
			return l
		return len(l) #if not returning list, then return the # of matched patterns

	def addPattern(self, pattern, callbackfn, start=0, end='e',label="",active=True): #returns index to stored pattern
		n = self.patternIdx
		self.patterns[n] = [pattern,start,end,callbackfn,label,active] #note order is important since used elsewhere
		#PATIDX = enum(PATTERN=0, START=1, END=2, CALLBACKFN=3, LABEL=4, ACTIVE=5)  # see declaration above class def
		self.patternIdx += 1

		return n

	def delPattern(self,index): #remove a pattern from storage
		if (index in self.patterns):
			del self.patterns[index]
		return self.numPatterns()

	def getPattern(self,index): #retrieve a pattern from storage via its index
		if (index in self.patterns):
			return list(self.patterns[index])
		return None		

	def findPatternByLabel(self,label): #allows string or compiled regex
		r=[]
		if self.typeStr(label)=="str":
			for i in self.patterns:
				if self.patterns[i][PATIDX.LABEL] == label:
					r.append(list(self.patterns[i]))
		elif self.typeStr(label)=="regex":
			for i in self.patterns:
				if label.search(self.patterns[i][PATIDX.LABEL]) != None:
					r.append(list(self.patterns[i]))
		return r

	def setPatternActiveState(self,index,state): #set a pattern's active state
		if (index in self.patterns):
			self.patterns[index][PATIDX.ACTIVE] = state==True
		return state==True

	def getPatternActiveState(self,index): #see if a pattern is active or not
		if (index in self.patterns):
			return self.patterns[index][PATIDX.ACTIVE]
		return -1 #error in index


	def showPatterns(self): #get all patterns stored
		return dict(self.patterns) #return shallow copy of current patterns

	def clearPatterns(self): #remove all patterns from pattern search dictionary
		self.patterns={}
		return numPatterns()

	def numPatterns(self):	 #show number of patterns in the search dictionary
		return len(self.patterns)

"""
#see examples.py for complete examples in use, including using patterns 
#these examples commented out below are just for getting started.
def main():
	#simple examples...
	myFifoStr=fifostr(5) #create a fifostr of 5 characters length 
	print "myFifoStr=fifiostr(5) ==>",myFifoStr
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