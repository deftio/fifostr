# fifostr.py

a small python lib for treating strings as fifos with callback-based pattern matching

(c) 2011 manu chatterjee    deftio (at) deftio.com


fifostr (First In First Out String) is a small python originally used for combining  deque & string based operations for an embedded terminal program.  It allows pieces of a string to be treated in a mutable way with operations that you would expect from a bi-directional list such as insertion at either end and adding/removing N chars from either end.

fifostr also allows you to add / remove patterns which can trigger a user supplied function (E.g. if the pattern is "seen" then trigger the function).  Patterns can be strings, regexes or user-supplied-functions. A pattern consists of:
  * pattern: string <or> compiled regex <or> user-supplied-parser-function
  * label: user supplied 'name' for this pattern
  * start index : position in fifostr to begin pattern match.  default is 0
  * stop index : position in fifostr to end pattern match.  default is end of fifostr
  * callback_fn : called if pattern is found, fifostr(start:end) is passed to the callback fn
  * active : default is True, sets whether this pattern should be actively looked for

There is nothing really profound here -- one can argue its not worth its own repo. Originally a lighter version of this was used in a python serial terminal program dioterm (which allowed the serial terminal to parse commands sent/received by both sides).  

Cheers-
MC

### Installation & usage
from fifostr import fifostr  #include this statement with a path to fifostr.py
fifostr.py is compatible (without mods) with both python 2.7+ and python 3.* 

### Functionality List
allows a string which is treated as a deque (fifo) object with:
  * add/remove chars or strings at either end 
  * use slices, lists, or tuples to retrieve members (just like a real str object) 
  * get head/tail (as a str)
  * match head/tail  --> match a supplied string to either the head or tail
  * add/del/get patterns  --> pattern can be string | regex | user_supplied_parser any of which triggers user supplied callback_fn
    * all patterns can look at either the whole fifostr or any subset e.g. addPattern("foo",myCallback,2,5) --> only looks for "foo" between positions 2 and 5 in the fifostr
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

    myFifoStr.eqhead("3456")    #True
    myFifoStr.eqhead("567")     #False
    myFifoStr.eqtail("4567")    #True
    myFifoStr.eqtail("abc")     #False

    #test a  string pattern directly
    myFifoStr.testPattern('67890') #False
    
    #test a regex pattern directly
    r1=re.compile("[0-9]+")
    myFifoStr.testPattern(r1)   #True

    r2=re.compile("[a-z]+")
    myFifoStr.testPattern(r2)   #False

    #adding patterns
    p1 = myFifoStr.addPattern("234",logf,label="234 was here") #integer index returned managing pattern 
    p2 = myFifoStr.addPattern("67890",logf,label="67890 detected")
    p3 = myFifoStr.addPattern(r1,logf,label="r1 detected")
    myFifoStr.addPattern(r2,logf,label="r2 hit")
    myFifoStr.addPattern(f1,logf,label="f1 hit")   
    myFifoStr.addPattern(f2,logf,label="f2 hit")    

    #patterns can be set active/inactive via pattern management fns 
    myFifoStr.setPatternActiveState(p1,False) #based on index returned from addPattern
```

### Notes
Absolutley *no* warranties on performance.  This is not replacement for a compiler/parser front end!  It just iterates over stored patterns every time something is added to the 
fifostr object.  If you do have a compiler front you wish to be called the just add one pattern in you pass your user-supplied-parser and let your own code do the work.

```
#let your own parser do the work
    myFifo = fifostr(20)  # make a 20 char fifostr
    myFifo.addPattern(myParser,myCallbk) #myParser passed entire fifostr (as str) when char(s) added
    myFifo.addPattern(myParser,myCallbk2,3,5) #myParser passed fifostr btw (3,5).  My Parser must return boolean

```

### Source code home
all source is at github:
http://github.com/deftio/fifostr

docs and other projects at 
http://deftio.com/open-source

### Tests & Coverage
for quick usage see
see __main__ in example.py file

for test coverage look in the /tests directory
to run tests you will need pytest installed.
#### on Ubuntu:
    pip install -U pytest # or
    easy_install -U pytest
    #more info at pytest.org  for installation on other OSes

    cd to the tests directory
    run
    py.test

### Release History
*1.0.0 Initial release

### License
Opensource for all purposes as long as attribution is given. 







