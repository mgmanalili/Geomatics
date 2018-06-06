import ee
from ee import batch

#Since we have already configured the python API for GEE
#We can directly call GEE from here
#earthengine authenticate
#4/AAApisicDiqCFChNmdArxbPTZp23ke2xFn7e1XtaKdRaONSkm5L9KPE
#Reference: https://geoscripting-wur.github.io/Earth_Engine/

ee.Initialize()
srtm = ee.Image('srtm90_v4')

#Returns the metadata of landsat information 
l8 = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')
#print(l8.getInfo())

#Select date range
from_date = raw_input("Select start date (YYYY-MM-DD): ")
to_date = raw_input("Select end date (YYYY-MM-DD): ")

## Initialize connection to server
ee.Initialize()
## Define your image collection 
collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA')
## Define time range
collection_time = collection.filterDate(from_date, to_date) #YYYY-MM-DD
## Select location based on location of tile
path = collection_time.filter(ee.Filter.eq('WRS_PATH', 198))
pathrow = path.filter(ee.Filter.eq('WRS_ROW', 24))
# or via geographical location:
#point_geom = ee.Geometry.Point(5, 52) #longitude, latitude
#pathrow = collection_time.filterBounds(point_geom)
## Select imagery with less then 5% of image covered by clouds
clouds = pathrow.filter(ee.Filter.lt('CLOUD_COVER', 5))
## Select bands
bands = clouds.select(['B4', 'B3', 'B2'])
## Make 8 bit data
def convertBit(image):
    return image.multiply(512).uint8()  
## Convert bands to output video  
outputVideo = bands.map(convertBit)
title = raw_input('Enter video title: ')
print("Starting to create a video")
## Export video to Google Drive
out = batch.Export.video.toDrive(outputVideo, description=title, dimensions = 720, framesPerSecond = 1, region=([5.588144,51.993435], [5.727906, 51.993435],[5.727906, 51.944356],[5.588144, 51.944356]), maxFrames=10000)
## Process the image
process = batch.Task.start(out)
print("Conversion done! Please access you google drive")


