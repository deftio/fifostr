# fifostr.py

a small python lib for treating strings as fifos with triggerable patterns
(c) 2011 manu chatterjee    deftio (at) deftio.com


fifostr (First In First Out String) is a small python originally used for combining  deque & string based operations for a embedded terminal program.  It allows pieces of a string to be treated in a mutable way with operations that you would expect from a bi-directional list such as insertion at either end and adding/removing N chars from either end.

fifostr also allows you to add / remove patterns which can trigger a user supplied function (E.g. if the pattern is "seen" then trigger the function).  
    these patterns can be strings, regexes or user-supplied-functions
    each pattern takes its pattern, an optional label, an optional start,stop index (defaults to looking at whole fifostr obj), and a callback_fn which is used if the pattern is detected

There is nothing really profound here -- one can argue its not worth its own repo. Originally  this was used in a python serial terminal program dioterm (which allowed the serial terminal to parse commands sent/received by both sides).  

Cheers-
MC

### Installation & usage
from fifostr import fifostr  #include this statement with a path to fifostr.py
fifostr.py is compatible (without mods) with both python 2.7+ and python 3+ as of this writing.

### Feature List
allows a string which is treated as a deque (fifo) object with:
  * add/remove chars or strings at either end 
  * use slices, lists, or tuples to retrieve members (just like a real str object) 
  * get head/tail (as a str)
  * match head/tail  --> match a supplied string to either the head or tail
  * add/del/get patterns  --> pattern can be string | regex | user_supplied_parser any of which triggers user supplied callback_fn
    * all patterns can look at either the whole fifostr or any subset e.g. addPattern("foo",myCallback,3,5) --> only looks for foo between positions 3 and 5 in the fifostr
    * all patterns have optional label which can be used for logging purposes (eg. when pattern found, in addition to callback, emit label)
  * clear all patterns --> removes patterns from processing
  * get/setPattern Active/Inactive  --> allows a stored pattern to set on or off
  * Python 2.7+, Python 3+ support with no mods

### Usage example 

See example.py -- same examples as here but more comments, more use cases
```
from fifostr import *
def main():
    myFifoStr=fifostr(5) #make a fifostr of length 5
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


```

### Notes
Absolutley *no* warranties on performance.  This is no replacement for a compiler/parser front end.  It just iterates over stored patterns every time something is added to the 
fifostr object.  If you do have a compiler front you wish to be called the just add one pattern in you pass your user-supplied-parser and let your own code do the work.

```
#let your own parser do the work
    myFifo = fifostr(10)
    myFifo.addPattern(myParser,myCallback) #myParser is passed the entire fifostr (as a python string) everytime character(s) are added

```

### Source code home
all source is at github:
http://github.com/deftio/fifostr

docs and other goodies at 
http://deftio.com/open-source

### Tests & Coverage
for quick usage see
see __main__ in example.py file

for test coverage look in the /tests directory

### Release History
* 0.1.0 Initial release

### License
Opensource for all purposes as long as attribution is given. 







