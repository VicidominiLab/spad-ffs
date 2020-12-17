from listFiles import listFiles
from FCS2Corr import correlations
import os
from csv2array import csv2array

def FCSLoadG(fnameRoot, folderName="", printFileNames=True):
    G = correlations()
    files = listFiles(folderName, "csv", fnameRoot)
    for file in files:
        setattr(G, stripGfname(file, fnameRoot, printFileNames), csv2array(file, ','))
    G.dwellTime = 1e6 * csv2array(file, ',')[1, 0] # in µs
    print('--------------------------')
    print(str(len(files)) + ' files found.')
    print('--------------------------')
    return G


def stripGfname(fname, fnameRoot, printFileNames=True):
    fname = os.path.basename(fname)
    dummy, file_extension = os.path.splitext(fname)
    index = fname.find(fnameRoot)
    fname = fname[index + len(fnameRoot):-len(file_extension)]
    if printFileNames:
        print(fname)
    return fname
    