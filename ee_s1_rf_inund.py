import ee
from ee import batch

#Since we have already configured the python API for GEE
#We can directly call GEE from here
#earthengine authenticate
#4/AAApisicDiqCFChNmdArxbPTZp23ke2xFn7e1XtaKdRaONSkm5L9KPE
#Reference: https:#geoscripting-wur.github.io/Earth_Engine/

ee.Initialize()

geometry =[[[121.5966796875, 17.929089201618645],
          [121.59942626953125, 17.520963366230358],
          [121.81503295898438, 17.520963366230358],
          [121.80816650390625, 17.929089201618645]]]

cagayan = ee.Geometry.Rectangle([121.456,17.209,121.754,17.8077])

pt = cagayan

#Load Sentinel-1 C-band SAR Ground Range collection (log scaling, VV co-polar)
collection =  ee.ImageCollection('COPERNICUS/S1_GRD').filterBounds(pt).filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')).select('VV')

#Filter by date
before = collection.filterDate('2016-10-07', '2016-10-10').mosaic().clip(geometry)
after = collection.filterDate('2016-10-19', '2016-10-21').mosaic().clip(geometry)

#before = collection.filterDate('2017-10-01', '2017-10-05').mosaic().clip(geometry)
#after = collection.filterDate('2017-10-13', '2017-10-17').mosaic().clip(geometry)

#/LAWIN
#before = collection.filterDate('2016-10-19', '2016-10-21').mosaic()
#after = collection.filterDate('2016-10-30', '2016-11-04').mosaic()

#CLIP A REGION ONLY!!!
before_c = before.clip(geometry)
after_c = after.clip(geometry)

# Threshold smoothed radar intensities to identify "flooded" areas.
SMOOTHING_RADIUS = 100
DIFF_UPPER_THRESHOLD = -3 

diff_smoothed = after_c.focal_median(SMOOTHING_RADIUS, 'circle', 'meters').subtract(before_c.focal_median(SMOOTHING_RADIUS, 'circle', 'meters'))
diff_thresholded = diff_smoothed.lt(DIFF_UPPER_THRESHOLD)
  
# Create a geometry representing an export region.
export_geom = ee.Geometry.Rectangle([121.456,17.209,121.754,17.8077])

title = raw_input('Enter imagefile title: ')
# Export the image, specifying scale and region.
out = ee.batch.Export.image.toDrive(diff_thresholded,title,20,export_geom)

process = batch.Task.start(out)
print ("Process completed")