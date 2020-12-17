import matplotlib.pyplot as plt
import matplotlib.colors as pltcl
import numpy as np
import matplotlib.animation as animation
from checkfname import checkfname


def FCSdata2video(data, fname='data.mp4', ftime=100):
    """
    Convert SPAD-FCS data to video
    ===========================================================================
    Input       Meaning
    ----------  ---------------------------------------------------------------
    data        Data variable, i.e. output from binFile2Data
    fname       File name
    ftime       Frame time [ms]
    ===========================================================================
    Output      Meaning
    ----------  ---------------------------------------------------------------
    video
    ===========================================================================
    """
    
    Nt = np.size(data, 0)
    ims = []
    M = np.max(data[:,0:25])
    
    fig = plt.figure()
    for i in range(Nt):
        im = plt.imshow(np.reshape(data[i,0:25], (5, 5)))
        pltcl.Normalize(0, M, clip=True)
        ims.append([im])
    
    ani = animation.ArtistAnimation(fig, ims, interval=ftime, blit=True)
    
    fname = checkfname(fname, 'mp4')
    
    ani.save(fname)


def partPos2video(pos, fname='video.mp4', ftime=100):
    """
    Convert SPAD-FCS particle positions to video
    ===========================================================================
    Input       Meaning
    ----------  ---------------------------------------------------------------
    pos         [Np x 3 x Nf] data array with
                    Np  number of particles
                    3   x, y, z coordinates of the particle (float)
                    Nf  number of frames
    ===========================================================================
    Output      Meaning
    ----------  ---------------------------------------------------------------
    video
    ===========================================================================
    """
    
    Nf = np.shape(pos)[2]
    Np = np.shape(pos)[0]
    
    posShadow = np.copy(pos)
    posShadow[:, 2, :] = 0
    pos = np.concatenate((pos, posShadow), axis=0)
    
    colorList = np.zeros((2*Np, 3))
    colorList[0:Np, :] = np.tile(np.array([31/256, 121/256, 182/256]), (Np, 1))
    sizeList = np.zeros((2*Np, 1))
    sizeList[0:Np, :] = np.tile(np.array([3]), (Np, 1))
    sizeList[Np:2*Np, :] = np.tile(np.array([1]), (Np, 1))
    
    fig = plt.figure()
    ax = plt.axes(projection = "3d")
    
    ims = []
    for i in range(Nf):
        im = ax.scatter3D(pos[:, 0, i], pos[:, 1, i], pos[:, 2, i], color=colorList, s=sizeList)
        ims.append([im])
    
    ani = animation.ArtistAnimation(fig, ims, interval=ftime, blit=True)
    
    fname = checkfname(fname, 'mp4')
    
    ani.save(fname)
