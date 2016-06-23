#!/usr/bin/env python
from __future__ import print_function #just for parenthesis wrapping in python 2

"""
	exmaple.py - A demo of using FIFOStr 
	
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
	in a product, an acknowledgment in the product documentation would be
	appreciated but is not required.

	2. Altered source versions must be plainly marked as such, and must not be
	misrepresented as being the original software.

	3. This notice may not be removed or altered from any source
	distribution.

"""

from fifostr import FIFOStr
import re
import itertools

def main():
	#simple examples...
	myFifoStr=FIFOStr(5)
	print ("myFifoStr=FIFOStr(5) ==>",myFifoStr)
	
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
	print (myFifoStr.typeStr(123))
	print (myFifoStr.typeStr("123"))
	print (myFifoStr.typeStr(1.2))
	print (myFifoStr.typeStr(re.compile("we")))
	print (myFifoStr.typeStr(main))

	
	#retrieval  
	print (myFifoStr[3])			#accepts integer index  
	print (myFifoStr[1:4]) 			#accepts slice TODO accept indexing e.g. [1,5,-1]
	print (myFifoStr[[1,4,2]]) 		#accepts list 
	print (myFifoStr[1,3,4])		#accepts tuple

	#print (myFifoStr.testPattern("123"))

if __name__ == '__main__':
    main()
