from pystac import *
from osgeo import gdal
from urllib.parse import urlparse
import os
import numpy as np

gdal.UseExceptions()


def set_env():
    if 'PREFIX' not in os.environ.keys():
        os.environ['PREFIX'] = '/opt/anaconda/envs/env_vi'
        os.environ['GDAL_DATA'] = os.path.join(os.environ['PREFIX'], 'share/gdal')
        os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 'share/proj')


def fix_asset_href(uri):
    # print('-', uri)
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
    # print(eo_item)

    # Get bands
    if eo_item.bands is not None:
        for index, band in enumerate(eo_item.bands):
            # print(index, band, band.common_name, band.name) # eg --> 1 <Band name=B02> blue B02
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


def normalized_difference(band_1, band_2):
    width = np.shape(band_1.shape)[0]  # is this correct?!? or just np.shape(band1)[0] probably?
    height = np.shape(band_1)[1]

    norm_diff = np.zeros((height, width), dtype=np.uint)
    norm_diff = 10000 * ((band_1 - band_2) / (band_1 + band_2))

    return norm_diff


"""
def generate_evi(blue, green, red, nir, C1=6, C2=7.5, L_evi=1):
    #C1 = 6; C2 = 7.5; L_evi = 1 # these are values used in S2 example here: https://custom-scripts.sentinel-hub.com/sentinel-2/evi/#. 
    
    width = np.shape(blue.shape)[0] # check shape. not sure this is correct.
    height = np.shape(blue)[1]

    evi = np.zeros((height, width), dtype=np.uint)
    
    evi = green*( (nir - red) / (nir + C1*red - C2*blue + L_evi) )
    
    return evi
    
def generate_savi(red, nir, L_savi = 0.5): 
    
    width = np.shape(red.shape)[0] # check shape. not sure this is correct.
    height = np.shape(red)[1]

    savi = np.zeros((height, width), dtype=np.uint)
    
    savi = ((nir - red) / (nir + red + L_savi)) * (1 + L_savi)
    return savi

def generate_msavi(red, nir):
    
    width = np.shape(red.shape)[0] # check shape. not sure this is correct.
    height = np.shape(red)[1]

    msavi = np.zeros((height, width), dtype=np.uint)
    
    msavi = (2*nir + 1 – np.sqrt((2 * nir + 1)**2 – 8*(nir - red))) / 2
    return msavi
"""


def cog(input_tif, output_tif, no_data=None):
    translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
                                                                    '-co COPY_SRC_OVERVIEWS=YES ' \
                                                                    '-co COMPRESS=DEFLATE '))

    if no_data != None:
        translate_options = gdal.TranslateOptions(gdal.ParseCommandLine('-co TILED=YES ' \
                                                                        '-co COPY_SRC_OVERVIEWS=YES ' \
                                                                        '-co COMPRESS=DEFLATE ' \
                                                                        '-a_nodata {}'.format(no_data)))
    ds = gdal.Open(input_tif, gdal.OF_READONLY)

    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    ds.BuildOverviews('NEAREST', [2, 4, 8, 16, 32])

    ds = None

    del (ds)

    ds = gdal.Open(input_tif)
    gdal.Translate(output_tif,
                   ds,
                   options=translate_options)
    ds = None

    del (ds)

    os.remove('{}.ovr'.format(input_tif))
    os.remove(input_tif)
