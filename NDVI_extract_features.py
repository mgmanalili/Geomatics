#Michael Andrew Manalili
#2003-96643
#GmE 205 - LabEx 4
#NDVI generation and Density Slicing using python and GDAL

from osgeo import gdal
from osgeo.gdalconst import *
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt

#M:\00_Geomatics\00_MSc Geomatics\GmE 205 - OOP for Geomatics Applications\00_LabEx\LabEx7\solano.tif

infn = raw_input('Enter multispectral / multiband raster: ')
outfn = raw_input('Enter output filename for classified image: ')
ds = gdal.Open(infn, GA_ReadOnly)
dsGT = ds.GetGeoTransform()
proj = ds.GetProjection()
cols = ds.RasterXSize
rows = ds.RasterYSize

#Computing for NDVI
red = ds.GetRasterBand(3).ReadAsArray(0,0, cols, rows).astype(np.float)
nir = ds.GetRasterBand(4).ReadAsArray(0,0, cols, rows).astype(np.float)
ndvi = (nir - red) / (nir + red)

#Computing for median Filtered NDVI
kernel_size = int(raw_input('Enter Kernel Size for smoothing (single value odd intiger only): '))        
ndviF = scipy.signal.medfilt2d(ndvi, kernel_size)

#Density Slicing
veg = np.where((ndviF >= 0.63),1.0,0)
veg = np.where((ndviF < 0.63),0,veg)

display = raw_input('Do you like to plot the raw NDVI and Filtered NDVI? [Y/N]: ')

if display == 'Y':
    plt.subplot(131)
    plt.title("Raw NDVI")
    plt.imshow(ndvi)
    plt.subplot(132)
    plt.title("Filtered NDVI (Kernel Size = %s)" %kernel_size)    
    plt.imshow(ndviF)
    plt.subplot(133)
    plt.title("Classified")
    plt.imshow(veg)
else:
    pass

print "Please check the output binary image at %s" %outfn

driver = gdal.GetDriverByName("GTiff") 
driver.Register()
outds = driver.Create(outfn, cols, rows, 1, GDT_Float32)
outds.SetGeoTransform(dsGT)
outds.SetProjection(proj)
outBand = outds.GetRasterBand(1)
outBand.WriteArray(veg, 0, 0)
outBand.FlushCache()
del outds
del ds
