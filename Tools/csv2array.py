import numpy as np
from numpy import genfromtxt

def csv2array(file, dlmt='\t'):
    data = genfromtxt(file, delimiter=dlmt)
    return data
