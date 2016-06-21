## fifostr
#
#  (c) 2011 manu chatterjee 

fifostr (First In First Out String) is a tiny python class I used for creating deque for string based operations.  In otherwords it allows pieces of a string to be treated in a mutable way with operations that you would expect from a bi-directional list such as insertion at either end and grabbing N chars from either end.

fifostr also allows you to add / remove patterns which can trigger a user supplied function (E.g. if the pattern is "seen" then trigger the function).  

There is nothing really profound here -- one can argue its not worth its own repo but at the time I was thinking of expanding some its abilities with some parsing ideas which may or may not ever happen but if so I'll come back here.  Originally  this was used in a python serial terminal program dioterm (which allowed the serial terminal to parse commands sent/received by both sides).  


Cheers-
MC

#Installation & usage
from fifostr import FIFOStr  #include this statement with a path to fifostr.py


#Usage example 

See example.py

def main():
    myFifoStr=FIFOStr(5) #make a fifostr of length 
    myFifoStr+='1234567' #adds 1234567 to fifostr ... but len of fifostr is 5
                         # so only 34567 is retained
   
    print "myFifoStr.head(3)= ",myFifoStr.head(3) #shows 345
    print "myFifoStr.tail(4)= ",myFifoStr.tail(4) #shows 4567

    # the eqhead and eqtail functions allow string compares against
    # the head or the tail

    myFifoStr.eqhead("3456")= True
    myFifoStr.eqhead("567")= False
    myFifoStr.eqtail("4567")= True
    myFifoStr.eqtail("abc")= False


#Source code home
all source is at github:
http://github.com/deftio/fifostr

docs and other goodies at 
http://deftio.com/open-source

## Tests  (requires mocha and chai test suites)
see __main__ in fifostr.py file

## Release History
* 0.1.0 Initial release





