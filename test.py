from fastfac import *
import time

dem = np.array([[30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0],
                [30.0, 29.0, 28.5, 29.0, 30.0, 29.0, 30.0],
                [30.0, 29.0, 27.5, 28.0, 30.0, 28.0, 30.0],
                [30.0, 29.0, 28.0, 26.5, 29.0, 27.0, 29.0],
                [29.0, 28.0, 28.0, 25.5, 28.0, 26.0, 28.0],
                [28.0, 28.0, 27.0, 26.0, 25.0, 28.0, 28.0],
                [28.0, 27.0, 27.0, 24.0, 27.0, 27.5, 28.0]
                ])

dem2 = np.array([[-9.0, -9.0, -9.0, -9.0, -9.0, -9.0, -9.0],
                [-9.0, 29.0, 28.5, 29.0, 30.0, 29.0, -9.0],
                [-9.0, -9.0, 27.5, 28.0, 30.0, 28.0, -9.0],
                [-9.0, 29.0, 28.0, 26.5, 29.0, 27.0, -9.0],
                [29.0, 28.0, 28.0, 25.5, 28.0, 26.0, -9.0],
                [28.0, 28.0, 27.0, 26.0, 25.0, 28.0, -9.0],
                [28.0, 27.0, 27.0, 24.0, 27.0, 27.5, -9.0]
                ])

dem3 = np.array([[9.0, 8.0, 7.0, 8.0, 9.0],
                 [8.0, 7.0, 6.0, 7.0, 8.0],
                 [7.0, 6.0, 5.0, 6.0, 7.0],
                 [6.0, 5.0, 4.0, 5.0, 6.0],
                 [5.0, 4.0, 3.0, 4.0, 5.0]])

# a = np.array([16, 16, 16, 19, 19, 24, 24, 16, 31, 24, 29, 31, 39, 43, 37, 45, 39, 43, 45, 39])
# b = np.array([ 1., 1., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
# i = np.array([16, 19, 24, 29, 31, 37, 39, 43, 45])

# nodata = -9.0
# fdir = flowDirectionTestInward(dem2, nodata)
# flowto = flowsTo(fdir, nodata)
# group1 = firstGroup(flowto, nodata)
# groupold, facold = facgroup(dem2, fdir, nodata)
# print groupold.astype(int)
# facnew, groupnew = flowaccum(flowto, group1, nodata)
# #print groupold.astype(int)
# print "GROUPS"
# print groupnew
# print facold
# print facnew
# print fdir

# print "fac"
# print fac
# print "fdir"
# print fdir

dempath = "C:/temp/fil10m.tif"
ds = gdal.Open(dempath)
nodata = ds.GetRasterBand(1).GetNoDataValue()
demdata = ds.GetRasterBand(1).ReadAsArray()
starttime = time.time()
fdir = flowDirectionTestInward(demdata, nodata)
fdirtime = time.time()
print "fdir", fdirtime-starttime
flowto = flowsTo(fdir, nodata)
group1 = firstGroup(flowto, nodata)
fac, group = flowaccum(flowto, group1, nodata)
factime = time.time()
print "fac", factime-fdirtime
print "total", factime-starttime