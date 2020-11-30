from pystac import *
import gdal 
from urllib.parse import urlparse
import os
import numpy as np

# Define parameters
scale_factor = 1.0 / 0.0001
a_min = -10000
a_max = 10000
nodata = -11111


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

def truncate(arr):
    
    arr2 = np.where(arr < a_min, a_min, arr)
    arr2 = np.where(arr > a_max, a_max, arr2)
    arr2 = np.where(np.logical_or(np.isnan(arr),np.isinf(arr)), nodata, arr2) # perhaps I should also add those pixels that are already no_data from original image?

    return arr2
    
def normalized_difference(band_1, band_2):
    
    width = np.shape(band_1)[0] 
    height = np.shape(band_1)[1]
    
    norm_diff = np.zeros((height, width), dtype=np.int16)
    norm_diff = scale_factor * ((band_1 - band_2) / (band_1 + band_2))
    
    print('norm_diff', np.nanmin(norm_diff), np.nanmax(norm_diff))
    #logging.info('- norm_diff shape: ' + str(np.shape(norm_diff)))
    
    norm_diff_tr = truncate(norm_diff)
    print('norm_diff_tr', np.nanmin(norm_diff_tr), np.nanmax(norm_diff_tr))
       
    return norm_diff_tr

def generate_evi(blue, red, nir, C1=6, C2=7.5, L_evi=1):
    #C1 = 6; C2 = 7.5; L_evi = 1 # these are values used in S2 example here: https://custom-scripts.sentinel-hub.com/sentinel-2/evi/#. 
    
    width = np.shape(blue)[0] 
    height = np.shape(blue)[1]
    
    evi = np.zeros((height, width), dtype=np.int16)
    evi = scale_factor * 2.5 * (nir - red) / (nir + C1*red - C2*blue + L_evi) 
    print('evi', np.nanmin(evi), np.nanmax(evi))
    #logging.info('- evi shape: ' + str(np.shape(evi)))
    
    evi_tr = truncate(evi)
    print('evi_tr', np.nanmin(evi_tr), np.nanmax(evi_tr))
    
    return evi_tr
    
def generate_savi(red, nir, L_savi = 0.5): 
    
    width = np.shape(red)[0] 
    height = np.shape(red)[1]

    savi = np.zeros((height, width), dtype=np.int16)
    savi = scale_factor * ((nir - red) / (nir + red + L_savi)) * (1 + L_savi)
    #logging.info('- savi shape: ' + str(np.shape(savi)))
    print('savi', np.nanmin(savi), np.nanmax(savi))
    
    savi_tr = truncate(savi)
    print('savi_tr', np.nanmin(savi_tr), np.nanmax(savi_tr))
    
    return savi_tr

def generate_msavi(red, nir):
    
    width = np.shape(red)[0] 
    height = np.shape(red)[1]

    msavi = np.zeros((height, width), dtype=np.int16)
    msavi = scale_factor * (2*nir + 1 - np.sqrt((2*nir + 1)**2 - 8*(nir - red))) / 2
    #logging.info('- msavi shape: ' + str(np.shape(msavi)))
    print('msavi', np.nanmin(msavi), np.nanmax(msavi))
    
    msavi_tr = truncate(msavi)
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
