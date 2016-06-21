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

"""

from collections import deque

#Simple FIFO (First-In-First-Out) for strings --> allows rolling FIFO of last n chars seen
#use addPattern() / delPattern() to add/delete patterns to look for
#patterns can be strings or regular expressions (regex)

class FIFOStr(deque):
	def __init__(self, size):
		super( FIFOStr, self ).__init__(maxlen=size)
		self.patterns = {}
		self.foo = 7
    
	def head(self,l=1):
		if len(self)<l: 
		    l=len(self)
		return "".join([self[i] for i in xrange(l)])
    
	def tail(self,l=1):
		if len(self)<l: 
		    l=len(self)
		return "".join([self[i] for i in xrange(len(self)-l,len(self))])
    
	def all(self):
		return "".join(self)

	def eqhead(self,instring):
		return self.head(len(instring))==instring    
    
	def eqtail(self,instring):
		return self.tail(len(instring))==instring

	def append(self,x):
		print x
		return deque.append(self,x)

	def __iadd__(self,x)		:
		return deque.__iadd__(self,x)

	def addPattern(self):
		return ""

	def delPattern(self):
		return ""

	def showPatterns(self):
		return ""

	def clearPatterns(self):
		return ""



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
