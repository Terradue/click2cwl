from pystac import *
import gdal 
import os
import numpy as np

gdal.UseExceptions()

def set_env():
    
    if not 'PREFIX' in os.environ.keys():
    
        os.environ['PREFIX'] = '/opt/anaconda/envs/env_vi'

        os.environ['GDAL_DATA'] =  os.path.join(os.environ['PREFIX'], 'share/gdal')
        os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 'share/proj')

def get_item(catalog):
    
    cat = Catalog.from_file(catalog) 
    
    try:
        
        collection = next(cat.get_children())
        item = next(collection.get_items())
        
    except StopIteration:

        item = next(cat.get_items())
        
    return item

def get_assets(item):
    
    for index, band in enumerate(item.bands):
   
        if band.common_name in ['swir16']:

            asset_swir16 = item.assets[band.name].get_absolute_href()

        if band.common_name in ['swir22']:

            asset_swir22 = item.assets[band.name].get_absolute_href()

        if band.common_name in ['nir']:

            asset_nir = item.assets[band.name].get_absolute_href()

        if band.common_name in ['red']:

            asset_red = item.assets[band.name].get_absolute_href()
            
    return asset_red, asset_nir, asset_swir16, asset_swir22
   
def normalized_difference(band_1, band_2):
    
    width = np.shape(band_1.shape)[0]
    height = np.shape(band_1)[1]

    norm_diff = np.zeros((height, width), dtype=np.uint)

    norm_diff = 10000 * ((band_1 - band_2) / (band_1 + band_2))
    
    return norm_diff
    

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
