import scipy.io
import pandas as pd
from itertools import *
import numpy as np
import os
from sklearn import linear_model

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '../../TSP')

print data_dir


os.chdir(data_dir)


for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
    for f in filenames:
        if f[-3:] == "txt":
            print "Reading file: " + f


#TODO: finish this project
#Commit test from GKH
