#Michael Andrew Manalili
#2003-96643
#GmE 205 - Final Project
#Flood delineation of SAR dataset using python

#------------------------------------------------------------------------------
from matplotlib import pyplot as plt
import time, os
import gdal, ogr, osr, os
import numpy as np
import scipy.signal
import pylab as pl
#------------------------------------------------------------------------------
def array2raster(array):
    infn = raw_input('Enter image as reference to geotransoform(master.tif): ')
    outfn = raw_input('Enter output raster location of array to convert: ')
    raster = gdal.Open(infn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(outfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

def raster2array():
    infn = raw_input('Enter raster to convert to array: ')
    raster = gdal.Open(infn)
    band = raster.GetRasterBand(1)
    return band.ReadAsArray()

def gdalslope():
    inDEM = raw_input("Enter the DEM path: ")    
    unit = "-p" #for slope in percent
    out_slope_fn = raw_input("Save output slope raster to file: ")
    print "Computing SLOPE do not exit..."
    return os.system("gdaldem slope" +' '+ inDEM +' '+ out_slope_fn +' '+unit)
    
def gdaltiles():
    infn = raw_input("Enter the raster to conver to GDAL2TILES: ")    
    outfol = raw_input("Enter the output folder location: ")    
    return os.system("gdal2tiles -z 12"+' '+infn+' '+outfol)
    
def getResolution(infn):
    raster = gdal.Open(infn)
    geotransform = raster.GetGeoTransform()
    res = {"x-pixel": abs(geotransform[1]), 
           "y-pixel": abs(geotransform[5])}
    return res

def getNoDataValue(infn):
    raster = gdal.Open(infn)
    band = raster.GetRasterBand(1)
    return band.GetNoDataValue()
    
def getstat(infn):
    stat = infn.GetStatistics(0,1)
    print stat

#------------------------------------------------------------------------------
startTime = time.time()
#m = r"\data\master.tif"
#s = r"\data\slave.tif"
#d = r"\data\dem.tif"

master = raster2array()
slave = raster2array()

#mnodata = getNoDataValue(m)
#mres = getResolution(m)
#snodata = getNoDataValue(s)
#sres = getResolution(s)
#getstat(m)

num_rows = master.shape[0]
num_cols = master.shape[1]

#Histogram Plot
print "WARNING, printing histogram can take a very long time.."
ans1 = raw_input("Would you like to print the histogram? [Y/N]: ")
if ans1 == 'Y':    
    n, bins, patches = plt.hist(slave.ravel(), 100, facecolor='green', alpha=0.75)
    pl.hist(master, bins = 100 ** np.linspace(np.log10(MIN), np.log10(MAX), 50))
    pl.gca().set_xscale("log")
    #pl.show()
    try: 
        print np.size(master), np.size(slave)
        if np.size(master) != np.size(slave):
            print "Master and Slave images have different columns and row sizes. Please resize."
    except:
        pass
    if ans1 == 'N':
        print "Lets proceed with the processing."
    else:
        pass

#------------------------------------------------------------------------------
#Implements the NDSI computation
NDSI = (master - slave) / (master + slave)

ans2 = raw_input("Would you like to save the raw NDSI image? [Y/N]: ")
if ans2 == 'Y':
    array2raster(NDSI)
    if ans2 == 'N':
        print "Lets proceed with the processing."
    else:
        pass
#Implements the flood delineation condition
flood = np.where((NDSI>=0.3) & (NDSI<=0.50),1.0,0)
flood = np.where((NDSI<0.30),0.0,1.0)

ans3 = raw_input("Would you like to save the Flood image? [Y/N]: ")
if ans3 == 'Y':
    array2raster(flood)
    if ans3 == 'N':
        print "Lets proceed with the processing."
    else:
        pass

slope = gdalslope()
print "Enter the slope raster file you generated just now:"
slope_array = raster2array()

#Create Slope Mask 
slope_mask_val = 18 #slope greater than 18% will be masked out
slopemask= np.where((slope_array>= slope_mask_val),0,1)
slopemask = np.where((slope_array < slope_mask_val),1,0)

print "Computing... do not exit..."
#Smooths out the slope result = This is because the resulting slope looks\
#Appears to be gridded due to the nature of the data.
#The output grid looks like this: https://goo.gl/LhL7SU
#Thus filtering reduces the effect..
slope_kernel_size = 5
slopefilter = scipy.signal.medfilt(slopemask, slope_kernel_size)

ans4 = raw_input("Would you like to save the slope filtered image? [Y/N]: ")
if ans4 == 'Y':
    array2raster(slopefilter)
    if ans4 == 'N':
        print "Lets proceed with the processing."
    else:
        pass

#Computes for the intersection of flooded and slope mask area
flood_kernel_size = int(raw_input("Enter single value kernel size for flood output(e.g. 3 or 5): "))
print "Computing... do not exit..."
result = slopefilter * flood
resultfilter = scipy.signal.medfilt(result, flood_kernel_size)
#Writing final output
print "Writing final outout to raster."
array2raster(resultfilter)

ans5 = raw_input("Would you like to convert array to gdal tiles? [Y/N]: ")
if ans5 == 'Y':
    gdaltiles()
    if ans5 == 'N':
        print "Lets proceed with the processing."
    else:
        pass

endTime = time.time()
print 'It took ' + str(endTime - startTime) + ' seconds'
#------------------------------------------------------------------------------
#END OF SCRIPT
