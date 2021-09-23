Geoprocessing helpers


```python
for i in range(100):
	print(i)
```

GDAL processing


```
gdalbuildvrt -separate -te xmin ymin xmax ymax -input_file_list /outdir/filelist.txt /outdir/outraster.vrt
```

gdal translate zero to no data

```
gdal_translate -of GTiff -a_nodata 0 input.tiff output.tiff -co "COMPRESS=LZW"
```

```
gdalbuildvrt /outdir/mosaic.vrt /dir/containing_all_tif/*.tif
```

```
gdal_translate -of Gtiff -ot Byte -co COMPRESS=LZW -co PREDICTOR=2 -co NUM_THREADS=ALL_CPUS -a_nodata 0 input.tif out.tif 
```

```
gdal_translate -of Gtiff -co COMPRESS=DEFLATE input.vrt out.tif
```

```
gdalwarp -cutline INPUT.shp -crop_to_cutline -dstalpha INPUT.tif OUTPUT.tif
```

```
gdalwarp -cutline /Users/michael/Desktop/gsw/adm0_d.shp -crop_to_cutline input.tif output.vrt --config GDALWARP_IGNORE_BAD_CUTLINE YES
```

```
gdaladdo INPUT.tif 2 4 8 16 32 64 128 256 1024 2048 -r average -ro --config COMPRESS_OVERVIEW LZW --config INTERLEAVE_OVERVIEW PIXEL
```

google drive image hosting for ArcGIS online

1. upload image to gdrive
2. make public
3. copy link
4. follow format (get ID from the end point)
https://drive.google.com/uc?export=view&id=1YaQu-s6wDnEdilnhvO8FIlFijOv-nAO5


HRSL on AWS

gdal_translate /vsicurl/https://dataforgood-fb-data.s3.amazonaws.com/hrsl-cogs/hrsl_general/hrsl_general-latest.vrt drc_hrsl.tif -projwin 22.172286 1.020213 24.394043 -1.601171 -projwin_srs EPSG:4326



min_lng max_lat max_lng min_lat


### R Cluster and Parallel processing

```R
gc()
rm(list = ls())
library(doParallel)
library(foreach)
library(parallel)
library(sf)
library(raster)
detectCores()
v_tf <- read_sf('/Users/michael/Desktop/gsw/admo_buffer0.shp')
r <- raster('/Users/michael/Desktop/gsw/out/mosaic_seas_jrc.tif')
beginCluster(n=11)
c <- crop(r, v_tf)
m <- mask(c,v_tf)
writeRaster(m, '/Users/michael/Desktop/gsw/out/mosaic_seas_jrc_clip.tif',overwrite=TRUE)
endCluster()
```