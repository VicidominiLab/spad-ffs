import numpy as np
import os
import argparse

import sys

"""
This set of functions allows to read a binary file containing SPAD measurements
using only the file name. The parameters are extracted from the matrix using
the tags. The assumpstion is that the parameters are constant and that all the
frames are complete.

Author: Sebastian Acuna

"""

def file_to_count(fname, datatype=np.uint16):
    """
    Read a bin file and returns an array with the decoded count for each measurement


    Args:
        fname: name of the file containing the data

    Returns:
        A numpy array of unsigned int16 os size N x 25 where N is the number of measurements 

    """
    try:
        raw = np.fromfile(fname, dtype=">u8")

    except:
        print("Error reading binary file")
        return None

    elements = raw.shape[0]
    print(f"Elements: {elements}")
    positions = int(elements/2)
    print(f"Positions: {positions}")

    raw_pos = np.reshape(raw, (positions, 2))
    print(f"data table: {raw_pos.shape}")

    time_per_pixel_tag = np.bitwise_and(raw_pos[:,1], 0b1)
    idx = np.argmax(time_per_pixel_tag != time_per_pixel_tag[0]) # positions per time
    time_per_pixel = int(idx)
    print(f"time per pixel: {time_per_pixel}")

    frame_tag = np.bitwise_and(np.right_shift(raw_pos[:,1], 2), 0b1)
    idx = np.argmax(frame_tag != frame_tag[0]) # positions per frame
    if idx == 0:
        print("Unique frame")
        frames = 1
    else:
        frames = positions/idx # TODO: check condition with larger dataset
        
    line_tag = np.bitwise_and(np.right_shift(raw_pos[:,1], 1), 0b1)
    idx = int(np.argmax(line_tag != line_tag[0])/time_per_pixel) # positions  per line
    print(f"Positions per lines: {idx}")    
    x = int(idx)
    y = int(positions/x/time_per_pixel)

    print(f"Dimensions: Y:{y}, X:{x}")

    out = np.zeros((positions , 25), dtype = datatype)

    matrix_to_count(raw_pos, out)

    return out, frames, y, x, time_per_pixel


def file_to_FCScount(fname, datatype=np.uint16, Npoints=-1, Noffset=0):
    """
    Read a bin file and returns an array with the decoded count for each measurement

    Args:
        fname: name of the file containing the data

    Returns:
        A numpy array of unsigned int16 os size N x 25 where N is the number of measurements 

    """
    try:
        Npoints = Npoints * 2
        NbytesOffset = 16 * Noffset
        raw = np.fromfile(fname, dtype=">u8", count=Npoints, offset=NbytesOffset)

    except:
        print("Error reading binary file")
        return None

    elements = raw.shape[0]
    print(f"Elements: {elements}")
    positions = int(elements/2)
    print(f"Positions: {positions}")

    print("Freeing memory")
    out = np.zeros((positions , 25), dtype = datatype)
    print("Done.")
    
    raw_pos = np.reshape(raw, (positions, 2))
    print(f"data table: {raw_pos.shape}")

    print("Converting data to counts")
    matrix_to_count(raw_pos, out)
    print("Done.")

    return out


def matrix_to_count(values, out):
    """
    Read an array of N measurements and write the count values in the out
    array

    Args:
        values: N x 2 unsigned int array with measurements
        out:    N x 25 unsigned int array for storing results

    Returns:
        The matrix out filled with the count
    """

    out[:,0] = np.bitwise_and(np.right_shift(values[:,0], 64 - 59), 0b1111) # 4 bits
    out[:,1] = np.bitwise_and(np.right_shift(values[:,0], 64 - 55), 0b1111) # 4 bits
    out[:,2] = np.bitwise_and(np.right_shift(values[:,0], 64 - 51), 0b1111) # 4 bits
    out[:,3] = np.bitwise_and(np.right_shift(values[:,0], 64 - 47), 0b1111) # 4 bits
    out[:,4] = np.bitwise_and(np.right_shift(values[:,0], 64 - 43), 0b1111) # 4 bits
    out[:,5] = np.bitwise_and(np.right_shift(values[:,0], 64 - 39), 0b1111) # 4 bits
    
    out[:,6] = np.bitwise_and(np.right_shift(values[:,1], 64 - 59), 0b11111) # 5 bits
    out[:,7] = np.bitwise_and(np.right_shift(values[:,1], 64 - 54), 0b111111) # 6 bits
    out[:,8] = np.bitwise_and(np.right_shift(values[:,1], 64 - 48), 0b11111) # 5 bits
    out[:,9] = np.bitwise_and(np.right_shift(values[:,1], 64 - 43), 0b1111) # 4 bits
    out[:,10] = np.bitwise_and(np.right_shift(values[:,1], 64 - 39), 0b1111) # 4 bits
    out[:,11] = np.bitwise_and(np.right_shift(values[:,1], 64 - 35), 0b111111) # 6 bits
    out[:,12] = np.bitwise_and(np.right_shift(values[:,1], 64 - 29), 0b1111111111) # 10 bits
    out[:,13] = np.bitwise_and(np.right_shift(values[:,1], 64 - 19), 0b111111) # 6 bits
    out[:,14] = np.bitwise_and(np.right_shift(values[:,1], 64 - 13), 0b1111) # 4 bits
    out[:,15] = np.bitwise_and(np.right_shift(values[:,1], 64 - 9), 0b1111) # 4 bits
    out[:,16] = np.right_shift(values[:,1], 64 - 5) # 5 bits
    
    out[:,17] = np.bitwise_and(np.right_shift(values[:,0], 64 - 35), 0b111111) # 6 bits 
    out[:,18] = np.bitwise_and(np.right_shift(values[:,0], 64 - 29), 0b11111) # 5 bits
    out[:,19] = np.bitwise_and(np.right_shift(values[:,0], 64 - 24), 0b1111) # 4 bits
    out[:,20] = np.bitwise_and(np.right_shift(values[:,0], 64 - 20), 0b1111) # 4 bits
    out[:,21] = np.bitwise_and(np.right_shift(values[:,0], 64 - 16), 0b1111) # 4 bits
    out[:,22] = np.bitwise_and(np.right_shift(values[:,0], 64 - 12), 0b1111) # 4 bits
    out[:,23] = np.bitwise_and(np.right_shift(values[:,0], 64 - 8), 0b1111) # 4 bits
    out[:,24] = np.bitwise_and(np.right_shift(values[:,0], 64 - 4), 0b1111) # 4 bits


def reshape_to_5d(count, frames, y, x, time_per_pixel):
    """
    Reshapes the 2D count matrix to a 5D array (frames, y, x, time, sensor)

    Args:
        count: N x 25 count matrix
        frames: number of frames contained in matrix
        y:
        x:
        time:

    Returns:
        A 5-D matrix with dimensions (frames, y, x, time, sensor) 
    """

    return np.reshape(count, (frames, y, x, time_per_pixel, 25))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Converter from binary file to measurement matrix"
    )

    parser.add_argument(
        "binary",
        help="binary file name")

    args = parser.parse_args()
    fname = args.binary
    count, frames, y, x, time_per_pixel = file_to_count(fname)

    if count is None:
        print("Failed to process data. Closing.")
        sys.exit(0)

    file_name, extension = os.path.splitext(fname) # Get filename without extension

    print("Saving 5D matrix...", sep="")
    count5d = reshape_to_5d(count, frames, y, x, time_per_pixel)
    np.save(file_name + ".npy", count5d)
    print("Done.")

    




