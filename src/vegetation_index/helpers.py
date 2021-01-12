from pystac import *
import gdal 
from urllib.parse import urlparse
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors


scale_factor = 0.0001
range_min = -10000
range_max = 10000
nodata = -11111
datatype = np.int16

gdal.UseExceptions()

def set_env():
    
    if not 'PREFIX' in os.environ.keys():
    
        os.environ['PREFIX'] = '/opt/anaconda/envs/env_vi'

        os.environ['GDAL_DATA'] =  os.path.join(os.environ['PREFIX'], 'share/gdal')
        os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 'share/proj')
    
def fix_asset_href(uri):
    parsed = urlparse(uri)
    
    if parsed.scheme.startswith('http'):
        
        return '/vsicurl/{}'.format(uri)
    
    else:
        
        return uri
        
def get_item(catalog):
    
    cat = Catalog.from_file(catalog) 
    
    try:
        
        collection = next(cat.get_children())
        item = next(collection.get_items())
        
    except StopIteration:

        item = next(cat.get_items())
        
    return item

def get_assets(item):
    
    eo_item = extensions.eo.EOItemExt(item)
    
    # Get bands
    if (eo_item.bands) is not None:
        for index, band in enumerate(eo_item.bands):
            #print(index, band, band.common_name, band.name) # eg --> 1 <Band name=B02> blue B02
            if band.common_name in ['blue']: 
                asset_blue = fix_asset_href(item.assets[band.name].get_absolute_href())
            
            if band.common_name in ['green']: 
                asset_green = fix_asset_href(item.assets[band.name].get_absolute_href())
            
            if band.common_name in ['red']: 
                asset_red = fix_asset_href(item.assets[band.name].get_absolute_href())
            
            if band.common_name in ['nir']: 
                asset_nir = fix_asset_href(item.assets[band.name].get_absolute_href())
            
            if band.common_name in ['swir16']: 
                asset_swir16 = fix_asset_href(item.assets[band.name].get_absolute_href())
            
            if band.common_name in ['swir22']: 
                asset_swir22 = fix_asset_href(item.assets[band.name].get_absolute_href())

    else:
        asset_blue = fix_asset_href(item.assets['B02'].get_absolute_href())
        asset_green = fix_asset_href(item.assets['B03'].get_absolute_href())
        asset_red = fix_asset_href(item.assets['B04'].get_absolute_href())
        asset_nir = fix_asset_href(item.assets['B08'].get_absolute_href())
        asset_swir16 = fix_asset_href(item.assets['B11'].get_absolute_href())
        asset_swir22 = fix_asset_href(item.assets['B12'].get_absolute_href())
    
    return asset_blue, asset_green, asset_red, asset_nir, asset_swir16, asset_swir22

def truncate_nodata(arr, a_min, a_max):
    arr2 = np.where(arr==nodata,nodata,np.where(arr < a_min, nodata, arr))
    arr2 = np.where(arr==nodata,nodata,np.where(arr > a_max, nodata, arr2))
    arr2 = np.where(np.logical_or(np.isnan(arr),np.isinf(arr)), nodata, arr2) 
    
    return arr2
    
def getBands_and_Mask(ds):
    
    blue1 = ds.GetRasterBand(1).ReadAsArray().astype(np.float32) * scale_factor; #print('blue1', np.nanmin(blue1), np.nanmax(blue1))
    green1 = ds.GetRasterBand(2).ReadAsArray().astype(np.float32) * scale_factor; #print('green1', np.nanmin(green1), np.nanmax(green1))
    red1 = ds.GetRasterBand(3).ReadAsArray().astype(np.float32) * scale_factor; #print('red1', np.nanmin(red1), np.nanmax(red1))
    nir1 = ds.GetRasterBand(4).ReadAsArray().astype(np.float32) * scale_factor; #print('nir1', np.nanmin(nir1), np.nanmax(nir1))
    swir161 = ds.GetRasterBand(5).ReadAsArray().astype(np.float32) * scale_factor; #print('swir161', np.nanmin(swir161), np.nanmax(swir161))
    swir221 = ds.GetRasterBand(6).ReadAsArray().astype(np.float32) * scale_factor; #print('swir221', np.nanmin(swir221), np.nanmax(swir221))

    # Create Mask of nodata
    mask = np.where( (blue1 == 0) | (green1 == 0) | (red1 == 0) | (nir1 == 0) | (swir161 == 0) | (swir221 == 0), True, False)
    
    blue2 = np.where(mask,nodata,truncate_nodata(blue1,a_min=0,a_max=1)); print('blue2', np.min(blue2), np.max(blue2));
    green2 = np.where(mask,nodata,truncate_nodata(green1,a_min=0,a_max=1)); print('green2', np.min(green2), np.max(green2));
    red2 = np.where(mask,nodata,truncate_nodata(red1,a_min=0,a_max=1)); print('red2', np.min(red2), np.max(red2));
    nir2 = np.where(mask,nodata,truncate_nodata(nir1,a_min=0,a_max=1)); print('nir2', np.min(nir2), np.max(nir2));
    swir162 = np.where(mask,nodata,truncate_nodata(swir161,a_min=0,a_max=1)); print('swir162', np.min(swir162), np.max(swir162));
    swir222 = np.where(mask,nodata,truncate_nodata(swir221,a_min=0,a_max=1)); print('swir222', np.min(swir222), np.max(swir222));

    return blue2, green2, red2, nir2, swir162, swir222, mask
    
def normalized_difference(mask, band_1, band_2):
    """ used to calculate:
    - NDVI = (NIR - R) / (NIR + R)
    - Normalized Difference Moisture Index (NDMI) = (NIR - SWIR16) / (NIR + SWIR16)
    - Normalized Burn Ratio (NBR) = (NIR - SWIR22) / (NIR + SWIR22)
    - Normalized Burn Ratio 2 (NBR2) = (SWIR16 – SWIR22) / (SWIR16 + SWIR22)
    - Normalized Difference Water Index (NDWI) = (NIR - SWIR16) / (NIR + SWIR16)
    - Normalized Difference Built-up Index (NDBI) = (SWIR16 - NIR) / (SWIR16 + NIR)"""

    width = np.shape(band_1)[0]; height = np.shape(band_1)[1]
    
    norm_diff = np.zeros((height, width), dtype=datatype)
    norm_diff = np.where(mask, nodata, ((band_1 - band_2) / (band_1 + band_2)) / scale_factor)
    
    # print('norm_diff', np.nanmin(norm_diff), np.nanmax(norm_diff))
    
    norm_diff_tr = np.where(mask,nodata,truncate_nodata(norm_diff,range_min,range_max)).astype(datatype)
    print('norm_diff_tr', np.nanmin(norm_diff_tr), np.nanmax(norm_diff_tr))
    
    return norm_diff_tr

def generate_evi(mask, blue, red, nir, C1=6, C2=7.5, L_evi=1):
    # EVI = 2.5 * ((NIR - R) / (NIR + C1 * R – C2 * B + L_evi))
    #C1 = 6; C2 = 7.5; L_evi = 1 # these are values used in S2 example here: https://custom-scripts.sentinel-hub.com/sentinel-2/evi/#. 
    
    width = np.shape(blue)[0]; height = np.shape(blue)[1]
    
    evi = np.zeros((height, width), dtype=datatype)
    evi = np.where(mask, nodata, (2.5 * (nir - red) / (nir + C1*red - C2*blue + L_evi)) / scale_factor)
    
    # print('evi', np.nanmin(evi), np.nanmax(evi))
    
    evi_tr = np.where(mask,nodata,truncate_nodata(evi,range_min,range_max)).astype(datatype)
    print('evi_tr', np.nanmin(evi_tr), np.nanmax(evi_tr))
    
    return evi_tr
    
def generate_savi(mask, red, nir, L_savi = 0.5): 
    # SAVI = ((NIR - R) / (NIR + R + L_savi)) * (1 + L_savi): calculated with S2: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/savi/#
    
    width = np.shape(red)[0]; height = np.shape(red)[1]

    savi = np.zeros((height, width), dtype=datatype)
    savi = np.where(mask, nodata, ((nir - red) / (nir + red + L_savi) * (1 + L_savi)) / scale_factor)
    
    #print('savi', np.nanmin(savi), np.nanmax(savi))
    
    savi_tr = np.where(mask,nodata,truncate_nodata(savi,range_min,range_max)).astype(datatype)
    print('savi_tr', np.nanmin(savi_tr), np.nanmax(savi_tr))
    
    return savi_tr

def generate_msavi(mask, red, nir):
    # MSAVI = (2 * NIR + 1 – sqrt ((2 * NIR + 1)^2 – 8 * (NIR - R))) / 2
    
    width = np.shape(red)[0]; height = np.shape(red)[1]

    msavi = np.zeros((height, width), dtype=datatype)
    msavi = np.where(mask, nodata, ((2*nir + 1 - np.sqrt((2*nir + 1)**2 - 8*(nir - red))) * 0.5) / scale_factor)
    
    #print('msavi', np.nanmin(msavi), np.nanmax(msavi))
    
    msavi_tr = np.where(mask,nodata,truncate_nodata(msavi,range_min,range_max)).astype(datatype)
    print('msavi_tr', np.nanmin(msavi_tr), np.nanmax(msavi_tr))
    
    return msavi_tr

def cog(input_tif, output_tif,no_data=None):
    
    translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
                                                                    '-co COPY_SRC_OVERVIEWS=YES ' \
                                                                    '-co COMPRESS=DEFLATE '))
    
    if no_data != None:
        translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
                                                                        '-co COPY_SRC_OVERVIEWS=YES ' \
                                                                        '-co COMPRESS=DEFLATE '\
                                                                        '-a_nodata {}'.format(no_data)))
    ds = gdal.Open(input_tif, gdal.OF_READONLY)

    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    ds.BuildOverviews('NEAREST', [2,4,8,16,32])
    
    ds = None

    del(ds)
    
    ds = gdal.Open(input_tif)
    gdal.Translate(output_tif,
                   ds, 
                   options=translate_options)
    ds = None

    del(ds)
    
    os.remove('{}.ovr'.format(input_tif))
    os.remove(input_tif)

    
def writeFile(filename,geotransform,geoprojection,data,width,height):
    #print('Writing file to GTiff')
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(filename,
                           height,
                           width,
                           1,
                           gdal.GDT_Int16)
    dst_ds.GetRasterBand(1).SetNoDataValue(nodata)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds.FlushCache()
    #sleep(2) # why this?
    dst_ds = None
    del(dst_ds)

