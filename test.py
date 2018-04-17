import sys
import time
import numpy as np
from collections import deque
from gurobipy import *

from my_utils import *

import myNN
from mySECs import *

# x = np.arange(27.).reshape(3, 3,3)
# print(x)
# #y = np.where( x > 5 )
# #print (y)
# #print((x>5).nonzero())
# a = x.shape[1:]
# b = np.prod(a)
# print(b)

#get input
a = [1,2]
b = [3,4]

print a+b
