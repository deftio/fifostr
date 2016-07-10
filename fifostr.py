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

from collections import deque, Iterable
import re 
import itertools

#Simple constant ENUM style generator used for indexing internal storage array
def enum(**enums):
    return type('Enum', (), enums)
PIDX = enum(PATTERN=0, START=1, END=2, CALLBACKFN=3, LABEL=4, ACTIVE=5) #used internally


#Simple FIFO (First-In-First-Out) for strings --> allows rolling FIFO of last n chars seen
#use addPattern() / delPattern() to add/delete patterns to look for in the fifo
#patterns can be strings, regular expressions (regex), or a user-supplied-function provided that
#the function takes a string, returns a bool

class fifostr(deque):

	def __init__(self, size=None):
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

	#checker for iterability for some ops.  actually I was just very iterable when I realised this 
	#wasn't a built in in the language  ;)
	def iterable(self,obj):
	    return isinstance(obj, collections.Iterable)

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

	#overides================================================================
	def append(self,x,inc=False): #inc is bool, whether to ingest all of x at once (normal) or 1 at a time
		x = str(x)
		if inc==False: #this will append all of x at once
			deque.append(self,x)
			if len(self.patterns)>0:
				self.testAllPatterns(doCallbacks=True,retnList=False)
		else: #do each append, one at a time, so that all patterns can be checked
			for i in range(len(x)):
				deque.append(self,x[i])
				#todo do inc handling
				if len(self.patterns)>0:
					self.testAllPatterns(doCallbacks=True,retnList=False)
		return self

	def appendleft(self,x,inc=False): #inc is bool, whether to ingest all of x at once (normal) or 1 at a time
		x = str(x)
		if inc==False: #this will appendleft all of x at once
			deque.appendleft(self,x)		
			if len(self.patterns)>0:
				self.testAllPatterns(doCallbacks=True,retnList=False)
		else: #do each appendleft, one at a time, so that all patterns can be checked
			for i in range(len(x)):
				deque.appendleft(self,x[i])		
				if len(self.patterns)>0:
					self.testAllPatterns(doCallbacks=True,retnList=False)		
		return self

	def rotate(self,x,inc=1): #inc is bool, whether to ingest all of x at once (normal) or 1 at a time
		if inc==False: #this will rotate all of x at once
			deque.rotate(self,x)
			if len(self.patterns)>0:
				self.testAllPatterns(doCallbacks=True,retnList=False)
		else:
			for i in range(len(x)):
				deque.rotate(self,1) #1 at a time..
				if len(self.patterns)>0:
					self.testAllPatterns(doCallbacks=True,retnList=False)
		return self

	def pop(self): 
		deque.pop(self)
		if len(self.patterns)>0:
			self.testAllPatterns(doCallbacks=True,retnList=False)
		return self

	def popleft(self): 
		deque.popleft(self)
		if len(self.patterns)>0:
			self.testAllPatterns(doCallbacks=True,retnList=False)
		return self

	def reverse(self): #inc is bool, whether to ingest all of x at once (normal) or 1 at a time
		deque.reverse(self)
		if len(self.patterns)>0:
			self.testAllPatterns(doCallbacks=True,retnList=False)
		return self

	#operators================================================================
	def __eq__(self,x):
		return self.all()==x

	def __iadd__(self,x)		:
		deque.__iadd__(self,x)
		if len(self.patterns)>0:
			self.testAllPatterns(doCallbacks=True,retnList=False)
		return self

	def __getitem__(self, index): #add slicing support ... its a "string" after all ;)		
		#print("--->",index,type(index)) #debug
		if isinstance(index, slice):
			s = index.start
			e = index.stop
			if (e=='$') or (e== None): # the character "$" is used to specify end-of-string anchor in regex, so also allowed here
				e=len(self)
			if (e < 0):
				e = len(self)+e  # the character "^" is used to specifiy start-of-string anchor in regex, so also allowed here
			if (s=='^') or (s==None): 
				s=0
			return "".join(itertools.islice(self, s, e, index.step))
		if isinstance(index, list):
			return "".join([deque.__getitem__(self, x) for x in index])
		if isinstance(index, tuple):
			return "".join([deque.__getitem__(self, x) for x in index])
		if isinstance(index, str):
			if index == '$':
				index = len(self)
			if index == "^":
				index = 0
		return str(deque.__getitem__(self, index))
	
	def __setitem__(self, key, value):
		value = str(value)
		deque.__setitem__(self,key, value)
		if len(self.patterns)>0:
			self.testAllPatterns(doCallbacks=True,retnList=False)
		return self

	#pattern handling==========================================================
	def testPattern(self, pattern, start=0,end='$'): #test if a pattern matches btw start and end positions in fifostr
		if start == '^':
			start = 0
		if end == '$':
			end = len(self)-1
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
		for i in self.patterns: #todo replace with map()
			if (self.patterns[i][PIDX.ACTIVE]): #is an active pattern 
				r=self.testPattern(self.patterns[i][PIDX.PATTERN],self.patterns[i][PIDX.START] ,self.patterns[i][PIDX.END])
				l.append([i,self.patterns[i][PIDX.LABEL],r])
				if (doCallbacks):
					if r:
						self.patterns[i][PIDX.CALLBACKFN](self[self.patterns[i][PIDX.START]:self.patterns[i][PIDX.END]],self.patterns[i][PIDX.LABEL])
		if retnList:
			return l
		return len(l) #if not returning list, then return the # of matched patterns

	def addPattern(self, pattern, callbackfn, start=0, end='$',label="",active=True): #returns index to stored pattern
		n = self.patternIdx
		self.patterns[n] = [pattern,start,end,callbackfn,label,active] #note order is important since used elsewhere
		#PIDX = enum(PATTERN=0, START=1, END=2, CALLBACKFN=3, LABEL=4, ACTIVE=5)  # see declaration above class def
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
				if self.patterns[i][PIDX.LABEL] == label:
					r.append(list(self.patterns[i]))
		elif self.typeStr(label)=="regex":
			for i in self.patterns:
				if label.search(self.patterns[i][PIDX.LABEL]) != None:
					r.append(list(self.patterns[i]))
		return r

	def setPatternActiveState(self,index,state): #set a pattern's active state
		if (index in self.patterns):
			self.patterns[index][PIDX.ACTIVE] = state==True
		return state==True

	def getPatternActiveState(self,index): #see if a pattern is active or not
		if (index in self.patterns):
			return self.patterns[index][PIDX.ACTIVE]
		return -1 #error in index


	def showPatterns(self): #get all patterns stored
		return dict(self.patterns) #return shallow copy of current patterns

	def clearPatterns(self): #remove all patterns from pattern search dictionary
		self.patterns={}
		return numPatterns()

	def numPatterns(self):	 #show number of patterns in the search dictionary
		return len(self.patterns)

	#version info
	def ver(self):
		return 	{
					"version" : "1.0"					
				}
