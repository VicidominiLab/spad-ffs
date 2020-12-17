import numpy as np
from checkfname import checkfname
from tifffile import imwrite

def array2tiff(data, fname, pxsize=1, dim="yxz", transpose3=True):
    """
    Write 2D or 3D array to tiff image file
    ===========================================================================
    Input       Meaning
    ---------------------------------------------------------------------------
    data        2D or 3D array with data (integer numbers int16)
                    order: TZCYXS
                    with    t   time
                            c   channel
    fname       Name of the file to write to
    pxsize      Pixel size [µm]
    dim         String with dimensions in image
                    e.g. z stack of planar images: dim = "yxz"
                    The order must be "tzcyxs". The same order must be used
                    for data
                    E.g. for a xy time series: dim="tyx" and 'data' is a 3D
                    array with time, y, and x as 1st, 2nd, and 3r dimension
                    The only exception is that for a 3D array also "yxz" is ok
                    in combination with transpose3=True
                    (which moves the 3rd dimension to the first to correct the
                     order)
    ===========================================================================
    Output      Meaning
    ---------------------------------------------------------------------------
    tiff image
    ===========================================================================
    """
    
    # check file extension
    fname = checkfname(fname, "tiff")
    
    # check number of images in data
    ndim = data.ndim
    if ndim >= 3 and transpose3:
        # transpose data to make 3rd dimension first
        data = np.transpose(data, (2, 0, 1))
    
    # order of dimensions is now TZCYXS
    dimAll = "tzcyxs"
    N = [1, 1, 1, 1, 1, 1]
    d = 0
    Ishape = np.shape(data)
    for i in range(6):
        if dimAll[i] in dim:
            N[i] = Ishape[d]
            d += 1
    
    data.shape = N  # dimensions in TZCYXS order
    data = data.astype('int16')
    imwrite(fname, data, imagej=True, resolution=(1./pxsize, 1./pxsize), metadata={'unit': 'um'})
    
    # add every image to same tiff file    
    #imsave(fname, data)
    
    print("Done.")
    