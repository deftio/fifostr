[![PyPi version](https://img.shields.io/pypi/v/fifostr.svg)](https://pypi.org/project/FIFOStr/)
[![Build Status](https://travis-ci.com/deftio/fifostr.svg?branch=master)](https://travis-ci.com/deftio/fifostr)
[![Coverage Status](https://coveralls.io/repos/github/deftio/fifostr/badge.svg?branch=master)](https://coveralls.io/github/deftio/fifostr?branch=master)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-blue.svg)](https://opensource.org/licenses/BSD-2-Clause)


# fifostr.py
    
FIFOStr - A python language string library designed to look for patterns in a stream, such as serial connection or look back parser.  FIFOStr works by allowing character(s) to be inserted in to a FIFOstr object which is treated as FIFO (First-In-First-Out) buffer.  The FIFOstr object can be set to a fixed size so that when a new character is inserted the last character is removed.  

Trigger patterns (either strings, regular experssions, or customer parsers written in Python) can be attached to a FIFOstr object.  If that pattern is deteced in a string, a callback function will is called to trigger an action.  There is no limit to the number of patterns that can be deteted and each pattern can have a separate callback.

Since a FIFOstr is a fixed length buffer it can be attached to any stream with predictable resource consumption.  FIFOstr also supports mutable character injection / mutable string support (used to inject / to test patterns). 


Example code and a full test suite with CI are provided.  See coverage and test section below.

Logically FIFOstr works as follows:

```python
from fifostr import FIFOStr

#initialize from a given string
myString = FIFOStr("this is a test") # initialize with a string
len(myString) == 14 #true

# The FIFOStr function head( int N) returns the the first N characters
myString.head(4) == "this"  #true

myString+= " more" # this addes the string " more" to myString, each character is fed in and the last character in the FIFOstr is removed.

#initialize with max fixed length
myString.head(4) == "is a"  #true because the string is also a true FIFO and keeps fixed length.  Look at example below for more on pattern matching (and multiple pattern matching for more details)

myString = FIFOStr(10)  # creates a blank FIFOStr max length FIFOStr of 10 chars
len(myString)  # returns 0, there is no data in FIFOstr yet
myString += "This"
len(myString) == 4  # true
myString += " is more stuff"  # add characters to end of string
len(myString) == 10  #true
myString == "more stuff"  # true, string is at max len of 10 chars

#mutable support
myString[2] == 'd' # in place modification (mutable string)
myString == "mode stuff" # string position[2] is changed 

#For pattern matching & triggers see examples section.

```

Originally a lighter version of this was used in a python serial terminal program which allowed the serial terminal to parse commands sent/received by both sides.  

## Pattern Triggering Features 

Built-in pattern matching and triggering:  simply add / remove patterns which then call a callback function (E.g. if the pattern is "seen" then trigger the function).  Patterns can be strings, regexes or user-supplied-functions (parsers written in python). A pattern consists of:  
  * pattern: string *or* compiled regex *or* user-supplied-parser-function  
  * label: user supplied 'name' for this pattern  
  * start index : position in fifostr to begin pattern match.  default is 0  (also accepts the character '^' as start anchor for those familiar with regexes)
  * stop index : position in fifostr to end pattern match.  default is end of fifostr.  the letter '$' has special meaning as end of string no matter the length  (again regex)
  * callback_fn : called if pattern is found, fifostr(start:end) and the label are passed to the callback function  (callback('thematchingstring','label'))
  * active : default is True, sets whether this pattern should be actively looked for  
  * mutable string support for changing the contents middle position characters to look at callback responses.


### Installation
```
pip install fifostr # or just pull fifostr.py from the source repository and put in your source path  
```

### Original Usage

Originally part of a terminal program called 'dioterm' (albeit in much more compact form), this library was used used to 'listen' to traffic in either direction on a serial port.  When certain patterns were found such as a command sent from the host or a special piece of data from the embedded microntroller client, fifostr would trigger a callback to do something.  This was very useful when sequences of commands had to be set up between the host and client.  Many of these sequences where conditional based on what either the host or client sent resulting in many variations of sequence-test cases, especially if this results in the host then having to make some other call to an unrelated process or hardware to reply correctly.


### Functionality   
FIFOStr is a string which is (derived from deque) with these properties:  
  * add/remove chars or strings at either end   
  * mutable (can set a char to any value like an array with [])
  * use slices, lists, or tuples to retrieve members (just like a real str object)   
  * get head/tail (returns as a str)  
  * match head/tail  --> match a supplied string to either the head or tail  
  * use patterns to trigger callbacks  --> pattern can be string | regex | user_supplied_parser any of which triggers user supplied callback_fn  
    * all patterns can look at either the whole fifostr or any subset e.g. addPattern("foo",myCallback,2,5,"bar") 
        --> only looks for "foo" between positions 2 and 5 in the fifostr and will call myCallback with ("foo","bar")  if found
    * all patterns have optional label which can be used for logging purposes (eg. when pattern found, in addition to callback, emit label)  
    * user supplied callback_fn is called with both the string-match section and the label  
    * patterns can be added/deleted from the list of patterns "watching" the fifostr content
    * all (active) patterns are always matched.  fifostr matches multiple different patterns over the same string.  
  * clear all patterns --> removes patterns from processing  
  * get/setPattern Active/Inactive  --> allows a stored pattern to set on or off  
  * Python 2.7+, Python 3+ support, derived from built-in deque package  
  * 100% test coverage in both 2.7 and 3.x 

### Usage example   

See example.py to run in tests dir -- same examples as here but more comments, more use cases  

```python
from fifostr import FIFOStr
def main():
    myFifoStr=FIFOStr(5) #make a fifostr of length 5 (for unlimited length omit number)
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

    #fifostr.testPattern() allows you to test if the pattern is present in the fifostr object
    #test a  string pattern directly
    myFifoStr.testPattern('67890') #False
    
    #test a regex pattern directly.  to do this pass any valid regex in compiled form
    r1=re.compile("[0-9]+")
    myFifoStr.testPattern(r1)   #True

    r2=re.compile("[a-z]+")
    myFifoStr.testPattern(r2)   #False

    #more generally we can add (and remove) patterns which will scan and trigger a call back everytime the fifostr 
    #internal content changes (whether adding or deleting chars from either end or even rotating/reversing the fifstr object)

    #adding patterns
    p1 = myFifoStr.addPattern("234",logf,label="234 was here") #integer index returned managing pattern 
    p2 = myFifoStr.addPattern("67890",logf,label="67890 detected")
    p3 = myFifoStr.addPattern(r1,logf,label="r1 detected")
    myFifoStr.addPattern(r2,logf,label="r2 hit")
    myFifoStr.addPattern(f1,logf,label="f1 hit")   
    myFifoStr.addPattern(f2,logf,label="f2 hit")    

    #patterns can be set active/inactive via pattern management fns 
    myFifoStr.setPatternActiveState(p1,False) #based on index returned from addPattern

    #now show searching for stored pattern matchers in the pattern dict
    #this is not searching the fifo-string itself, just the stored patterns that we have entered
    print("find pattern by label 'foo':",myFifoStr.findPatternByLabel("foo")) #no matches returns empty list
    print("find pattern by label '234 hit':",myFifoStr.findPatternByLabel("234 hit")) #shows match
    print("find pattern by label using regex '[rf][0-9]':")
    pp.pprint(myFifoStr.findPatternByLabel(re.compile("[rf][0-9]")))

    #and finally demonstrate that patterns auto-trigger when items inserted in fifostr .. which afterall
    #is the point of the whole thing.. ;)
    print("\n fifo operations ============")
    for c in '01234567890abcdefghijklmnop':  #show using inc which accomplishes same thing
        myFifoStr += c

    myFifoStr+= 'abcdefghi'
    print (myFifoStr.all())

```

### Notes   

FIFOstr is not meant replacement for a compiler/parser front end though it can be used as complex tokenizer.  Internally just iterates over stored patterns every time something is added to the fifostr object.  If you do have a parser you wish to be called then just add it as a callback function so that every time the fifostr is updated with a char(s) it will call your parser to do the work.   Your parser must return a boolean result if you wish to use the callback based triggering.  Multiple custom parsers can be run in along with static string patterns or regexes.


```python
#let your own parser do the work  
    myFifo = fifostr(20)  # make a 20 char fifostr
    myFifo.addPattern(myParser,myCallbk) #myParser passed entire fifostr (as str) when char(s) added
    myFifo.addPattern(myParser,myCallbk2,3,5) #myParser passed fifostr btw (3,5).  My Parser must return True if match found for callback to be invoked

```

### Source code 
all source is at github:  
https://github.com/deftio/fifostr  

### Project Home
https://deftio.com/fifostr

### Company Home
docs and other projects at   
https://deftio.com/  

### Tests & Coverage
for quick usage see  
see __main__ in example.py file  

for test coverage look in the /tests directory  
to run tests pytest needs to be installed.  

#### on Ubuntu 
```bash
pip install -U pytest pytest-cov 
pip install coveralls   
```
note: more info at pytest.org  for installation on other OSes  

```bash
# running basic tests
cd tests
pytest  #or py.test 

# coverage stats below
coverage run --source fifostr -m pytest 
coverage report -m
```
### Generating docs
Documenation is generated using pandoc and pydoc from the build scripts.

```bash
sudo apt-get install pandoc
```
documentation is in /docs directory (generated by pydoc)
to (re)generate the docs.  cd to the docs directory. then type:
```bash
pydoc -w ../fifostr.py  
```
note that as of this writing pydoc generates its output in the current directory and doesn't seem to be pipeable to another.  

### Release History  
* 1.1.19 added sys.displayhook chaining for interactive mode display
* 1.1.18 added Str constructor 
* 1.1.17 updated to support 3.9x
* 1.1.16 updated to support python 3.7 3.8 3.9 in tests
* 1.1.15 updated PyPi to use README.md instead of README.rst (no other changes)
* 1.1.10 Updated docs and related usage info for repo
* 1.1.9  rebuild for README.md to README.rst conversion using pandoc (no code changes) for PyPi
* 1.1.8  rebuild to make sure proper pkg loaded to PyPi (no code changes) 
* 1.1.7  updated MANIFEST.in to use README.rst 
* 1.1.6  added PyPi version badge in README.md
* 1.1.5  coverage to 100%, added badging, added README.rst
* 1.1.x  changed class name from fifostr to FIFOStr to make PEP8 compliant.  fixed bug in setup.py (package_dir)
* 1.0.x  documentation clean up
* 1.0.0  Initial release  


### README.md vs README.rst  
The README.rst is generated from the README.md using pandoc but the content is identical.  (used for PyPi in earlier releases)


### License
See LICENSE.txt file in this directory.   The license is the OSI approved "FreeBSD" 2 clause license.



(c) 2018 m a chatterjee
