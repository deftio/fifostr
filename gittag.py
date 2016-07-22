import subprocess
PIPE = subprocess.PIPE

#get the package version from ... the package
import sys
sys.path.append('./fifostr')  #this is just to find fifostr which is in one up in the dir 
from fifostr import *

f = FIFOStr()
ver= f.ver()["version_str"]  # get version string 

process = subprocess.Popen(['git', '-a', ver])
#stdoutput, stderroutput = process.communicate()

if 'fatal' in stdoutput:
    # Handle error case
else:
    # Success!