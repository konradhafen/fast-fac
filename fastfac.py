import gdal
import numpy as np
import os

def flowDirection(dem):
    """
    Quick flow direction implementation with ESRI coding. Does not accurately sort out flow direction in flat areas, or
    raster edges.

    Args:
        dem: Numpy array of elevation values

    Returns:
        numpy array with ESRI flow directions

    """
    fdir = np.empty((dem.shape[0], dem.shape[1]))
    fdir.fill(0)
    gradient = np.empty((8, dem.shape[0]-2, dem.shape[1]-2), dtype = np.float)
    code = np.empty(8, dtype=np.int)
    for k in range(8):
        theta = -k * np.pi / 4
        code[k] = 2 ** k
        j, i = np.int(1.5 * np.cos(theta)), -np.int(1.5 * np.sin(theta))
        d = np.linalg.norm([i, j])
        gradient[k] = (dem[1 + i: dem.shape[0] - 1 + i, 1 + j: dem.shape[1] - 1 + j] - dem[1: dem.shape[0] - 1, 1: dem.shape[1] - 1]) / d

    direction = (-gradient).argmax(axis=0)
    fdir[1:-1, 1:-1] = code.take(direction)

    return fdir

def flowDirectionTest(dem):
    temp = np.empty((dem.shape[0]+2, dem.shape[1]+2)) #create temp array with buffer around dem
    temp.fill(-9.0) #fill with value greater than the dem max
    temp[1:-1, 1:-1] = dem #fill in dem values (creates wall so all cells will flow inward)
    dem = temp #set new dem
    mask = np.where(dem==-9.0, 0, 1)

    dem[dem == -9.0] = np.nanmax(dem)+2.0


    fdir = np.empty((dem.shape[0], dem.shape[1]))
    fdir.fill(0)
    gradient = np.empty((8, dem.shape[0] - 2, dem.shape[1] - 2), dtype=np.float)
    code = np.empty(8, dtype=np.int)
    for k in range(8):
        theta = -k * np.pi / 4
        code[k] = 2 ** k
        j, i = np.int(1.5 * np.cos(theta)), -np.int(1.5 * np.sin(theta))
        d = np.linalg.norm([i, j])
        gradient[k] = (dem[1 + i: dem.shape[0] - 1 + i, 1 + j: dem.shape[1] - 1 + j] - dem[1: dem.shape[0] - 1,
                                                                                       1: dem.shape[1] - 1]) / d

    direction = (-gradient).argmax(axis=0)
    fdir[1:-1, 1:-1] = code.take(direction)

    # print "dem"
    # print dem
    return fdir[1:-1, 1:-1] * mask[1:-1, 1:-1]