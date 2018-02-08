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
#print flowDirection(dem)
nodata = -9.0
fdir = flowDirectionTest(dem3, nodata)
print fdir
flowto = flowsTo(fdir, nodata)
# group, fac = facgroup(dem3, fdir, nodata)
# print group
# print "fac"
# print fac
# print "fdir"
# print fdir

# dempath = "C:/temp/fil10m.tif"
# ds = gdal.Open(dempath)
# nodata = ds.GetRasterBand(1).GetNoDataValue()
# demdata = ds.GetRasterBand(1).ReadAsArray()
# starttime = time.time()
# fdir = flowDirectionTest(demdata, nodata)
# fdirtime = time.time()
# print "fdir", fdirtime-starttime
# group, fac = facgroup(demdata, fdir, nodata)
# factime = time.time()
# print "fac", factime-fdirtime
# print "total", factime-starttime