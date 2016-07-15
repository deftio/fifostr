#!/usr/bin/env python
from __future__ import print_function #just for parenthesis wrapping in python 2

"""
	exmaple.py - A demo of using FIFOStr 
		
	Copyright (c) 2011-2016, M. A. Chatterjee <deftio at deftio dot com>
	All rights reserved.

	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met:

	* Redistributions of source code must retain the above copyright notice, this
	  list of conditions and the following disclaimer.

	* Redistributions in binary form must reproduce the above copyright notice,
	  this list of conditions and the following disclaimer in the documentation
	  and/or other materials provided with the distribution.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
	FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
	DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
	SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
	CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
	OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
	OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
import sys
sys.path.append('..')  #this is just to find fifostr which is in one up in the dir 

from fifostr import fifostr
import re
import pprint


def main():
	pp = pprint.PrettyPrinter(depth=6) #for nice printing complex objects
	#simple examples...
	print("simple examples for fifostr\nA class for treatings strings as FIFO(deque) with matching abilities\n")
	myFifoStr=fifostr(5)
	print ("myFifoStr=fifostr(5) ==>",myFifoStr)
	
	myFifoStr+='1234567'
	print ("print myFifoStr+='1234567' ==>",myFifoStr)
	
	#show head/tail fns
	print ("myFifoStr.head(3)=",myFifoStr.head(3))
	print ("myFifoStr.tail(4)= ",myFifoStr.tail(4))
	print ("myFifoStr.head(10)=",myFifoStr.head(10))
	print ("myFifoStr.tail(10)=",myFifoStr.tail(10))
	
	print ("len(myFifoStr)=",len(myFifoStr))
	
	print ("myFifoStr.eqhead(\"3456\")=",myFifoStr.eqhead("3456"))
	print ("myFifoStr.eqhead(\"567\")=",myFifoStr.eqhead("567"))
	print ("myFifoStr.eqtail(\"4567\")=",myFifoStr.eqtail("4567"))
	print ("myFifoStr.eqtail(\"abc\")=",myFifoStr.eqtail("abc"))
	print ("myFifoStr.eq(\"34567\")=",myFifoStr.eq("34567"))
	myFifoStr+='890'
	print ("myFifoStr+='890 ===>'",myFifoStr)
	print ("myFifoStr.head(3)= ",myFifoStr.head(3))
	print ("myFifoStr.tail(4)= ",myFifoStr.tail(4))
	print ("myFifoStr.head(10)=",myFifoStr.head(10))
	print ("myFifoStr.tail(10)=",myFifoStr.tail(10))
	print ("myFifoStr.all()=",myFifoStr.all())

	#tests for internal type testing... 
	print (myFifoStr.typeStr(123))				#returns "int"
	print (myFifoStr.typeStr("123"))			#returns "str"
	print (myFifoStr.typeStr(1.2))				#returns "float"
	print (myFifoStr.typeStr(re.compile("we"))) #returns "regex"
	print (myFifoStr.typeStr(main))				#returns "function"

	
	#retrieval  
	print ("\nindexing")
	print ("myFifoStr[3]="+myFifoStr[3])			#accepts integer index  
	print ("myFifoStr[1:4]="+myFifoStr[1:4]) 		#accepts slice TODO accept indexing e.g. [1,5,-1]
	print ("myFifoStr[[1,4,2]]="+myFifoStr[[1,4,2]])#accepts list 
	print ("myFifoStr[1,3,4]="+myFifoStr[1,3,4])	#accepts tuple

	#simple pattern matching
	print ("\npattern match tests")
	print ("\nstrings========")
	print ("myFifoStr.testPattern('this')",myFifoStr.testPattern('this'))
	print ("myFifoStr.testPattern('67890')",myFifoStr.testPattern('67890'))
	print ("\nregexes========")
	r1=re.compile("[0-9]+")
	print ("r1=re.compile([0-9]+)\nmyFifoStr.testPattern(r1)",myFifoStr.testPattern(r1))
	r2=re.compile("[a-z]+")
	print ("r2=re.compile([a-z]+)\nmyFifoStr.testPattern(r2)",myFifoStr.testPattern(r2))
	print ("\nfunctions======")
	def f1(s):
		return s=='tada'
	print ("def f1(s):\n\treturn s=='tada'\nmyFifoStr.testPattern(r1)",myFifoStr.testPattern(f1))
	print ()
	def f2(s):
		return s=='67890'		
	print ("def f1(s):\n\treturn s=='67890'\nmyFifoStr.testPattern(r1)",myFifoStr.testPattern(f2))
	print ("\n")

	#storing / deleting and managing patterns
	
	#this simple function is used for the callbackfn in the next set of examples
	def logf(s,label=""):
		print("callback-> match_str:"+s+"  label:"+label)

	myFifoStr.addPattern("234",logf,label="234 hit across whole string")
	myFifoStr.addPattern("234",logf,start=0, end=len("234"),label="234 at start")
	myFifoStr.addPattern("67890",logf,label="67890 hit as whole str")
	myFifoStr.addPattern('def',logf,start=1,end=4,label="'def' btw 3,5")
	myFifoStr.addPattern(r1,logf,label="r1 hit")
	myFifoStr.addPattern(r2,logf,label="r2 hit")
	x1=myFifoStr.addPattern(f1,logf,label="f1 hit")
	x2=myFifoStr.addPattern(f2,logf,label="f2 hit")
	pp.pprint(myFifoStr.showPatterns())

	print()
	pp.pprint(myFifoStr.testAllPatterns()) #test all the patterns added and are active #note pass doCallbacks=True to activate callback fns

	print()
	myFifoStr.delPattern(x1) #show deleting a pattern from the search
	pp.pprint(myFifoStr.showPatterns())

	print()
	myFifoStr.setPatternActiveState(x2,False)  #show retrieving pattern by index and setting inactive
	pp.pprint(myFifoStr.getPattern(x2))

	#now show searching for stored pattern matchers in the pattern dict
	#this is not searching the fifo-string itself, just the stored patterns that we have entered
	print("find pattern by label 'foo':",myFifoStr.findPatternByLabel("foo")) #no matches returns empty list
	print("find pattern by label '234 hit':",myFifoStr.findPatternByLabel("234 at start")) #shows match
	print("find pattern by label using regex '[rf][0-9]':")
	pp.pprint(myFifoStr.findPatternByLabel(re.compile("[rf][0-9]")))

	#and finally demonstrate that patterns auto-trigger when items inserted in fifostr .. which afterall
	#is the point of the whole thing.. ;)
	print("\nfifo pattern trigger examples ============")
	for c in '01234567890abcdefghijklmnop':  #show using inc which accomplishes same thing
		myFifoStr += c
		print ('added: "'+ c + '"  fifostr--> ' + myFifoStr.all() + " ==================")

	print("\done ... \n")
if __name__ == '__main__':
    main()
