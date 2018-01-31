import gdal
import numpy as np
import os


def setGlobals():
    global FLOW_DIR
    FLOW_DIR = np.array([32, 64, 128, 16, 0, 1, 8, 4, 2])
    global ROW_OFFSET
    ROW_OFFSET= np.array([-1, -1, -1, 0, 0, 0, 1, 1, 1])
    global COL_OFFSET
    COL_OFFSET = np.array([-1, 0, 1, -1, 0, 1, -1, 0, 1])

def drainsToMe(index, fdir):

    if index == 4:
        return False
    elif index == 0 and fdir == FLOW_DIR[8]:
        return True
    elif index == 1 and fdir == FLOW_DIR[7]:
        return True
    elif index == 2 and fdir == FLOW_DIR[6]:
        return True
    elif index == 3 and fdir == FLOW_DIR[5]:
        return True
    elif index == 5 and fdir == FLOW_DIR[3]:
        return True
    elif index == 6 and fdir == FLOW_DIR[2]:
        return True
    elif index == 7 and fdir == FLOW_DIR[1]:
        return True
    elif index == 8 and fdir == FLOW_DIR[0]:
        return True
    else:
        return False

def facgroup(dem, fdir, nodata):
    setGlobals()
    group = np.empty((dem.shape[0]+2, dem.shape[1]+2))
    group.fill(0)
    demnew = np.empty((group.shape))
    demnew.fill(nodata)
    demnew[1:-1, 1:-1] = dem
    fdirnew = np.empty((group.shape))
    fdirnew.fill(nodata)
    fdirnew[1:-1, 1:-1] = fdir
    while np.nanmax(demnew) != nodata:
        cells = np.swapaxes(np.where(demnew == np.nanmax(demnew)), 0, 1)
        for cell in cells:
            demWin = demnew[cell[0]-1:cell[0]+2, cell[1]-1:cell[1]+2].reshape(1, 9)
            fdirWin = fdirnew[cell[0]-1:cell[0]+2, cell[1]-1:cell[1]+2].reshape(1, 9)
            gathers = 0
            maxgather = 0
            for i in range(0, 9):
                if drainsToMe(i, fdirWin[0, i]):
                    gathers += 1
                    if group[cell[0] + ROW_OFFSET[i], cell[1] + COL_OFFSET[i]] > maxgather:
                        maxgather = group[cell[0] + ROW_OFFSET[i], cell[1] + COL_OFFSET[i]]

            if gathers > 0: group[cell[0], cell[1]] = maxgather + 1
            else: group[cell[0], cell[1]] = 1
            demnew[cell[0], cell[1]] = nodata

    return group[1:-1, 1:-1]



def fastfac(dem, fdir, group):
    fac = np.array(dem.shape)

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

def flowDirectionTest(dem, nodata):
    temp = np.empty((dem.shape[0]+2, dem.shape[1]+2)) #create temp array with buffer around dem
    temp.fill(nodata) #fill with value greater than the dem max
    temp[1:-1, 1:-1] = dem #fill in dem values (creates wall so all cells will flow inward)
    dem = temp #set new dem
    mask = np.where(dem==-9.0, 0, 1)

    dem[dem == nodata] = np.nanmax(dem)+2.0

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

    return fdir[1:-1, 1:-1] * mask[1:-1, 1:-1]