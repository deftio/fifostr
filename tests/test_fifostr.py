"""
Test Harness for fifostr.py library class
"""

import sys
sys.path.insert(0, '..')

from fifostr import *


def testTypeStr_IsInt():
	myFifoStr = fifostr(5)
	assert myFifoStr.typeStr(123) == "int"
