import numpy as np
from checkfname import checkfname
from tifffile import imsave

def array2tiff(data, fname):
    """
    Write 2D or 3D array to tiff image file

    ==========  ===============================================================
    Input       Meaning
    ----------  ---------------------------------------------------------------
    data        2D or 3D array with data (integer numbers)
    fname       Name of the file to write to
    ==========  ===============================================================

    ==========  ===============================================================
    Output      Meaning
    ----------  ---------------------------------------------------------------
    tiff image
    ==========  ===============================================================

    """
    
    # check file extension
    fname = checkfname(fname, "tiff")
    
    # check number of images in data
    ndim = data.ndim
    if ndim == 3:
        # transpose data
        data = np.transpose(data, (2, 0, 1))
    
    # add every image to same tiff file    
    imsave(fname, data)
    
    print("Done.")