## fifostr
#
#  (c) 2011 manu chatterjee 

fifostr (First In First Out String) is a small python class I used for creating deque for string based operations.  In otherwords it allows pieces of a string to be treated in a mutable way with operations that you would expect from a bi-directional list such as insertion at either end and adding/removing N chars from either end.

fifostr also allows you to add / remove patterns which can trigger a user supplied function (E.g. if the pattern is "seen" then trigger the function).  
    these patterns can be strings, regexes or user-supplied-functions
    each pattern takes its pattern, an optional label, an optional start,stop index (defaults to looking at whole fifostr obj), and a callback_fn which is used if the pattern is detected

There is nothing really profound here -- one can argue its not worth its own repo. Originally  this was used in a python serial terminal program dioterm (which allowed the serial terminal to parse commands sent/received by both sides).  

Cheers-
MC

#Installation & usage
from fifostr import fifostr  #include this statement with a path to fifostr.py
fifostr.py is compatible (without mods) with both python 2.7+ and python 3+ as of this writing.

#Feature List
allows a string which is treated as a deque (fifo) object with:
-add/remove chars or strings at either end
-use slices, lists, or tupes to retrieve members
-get head/tail
-eq head/tail  --> means match a string to either the head or tail
-add/del/get patterns  --> pattern can be string | regex | user_supplied_fnc
-clear all patterns --> removes patterns from processing
-get/setPattern Active/Inactive  -->
operators support slicing, indexing

#Usage example 

See example.py  #same examples as here but more comments, use cases

from fifostr import *
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

#Notes
Absolutley *no* warranties on performance.  This is no replacement for a compiler/parser front end.  It just iterates over stored patterns every time something is added to the 
fifostring object.  If you do have a compiler front you wish to be called the just add one pattern in you pass your user-supplied-parser and let your own code do the work.

#Source code home
all source is at github:
http://github.com/deftio/fifostr

docs and other goodies at 
http://deftio.com/open-source

## Tests  
see __main__ in example.py file

## Release History
* 0.1.0 Initial release





