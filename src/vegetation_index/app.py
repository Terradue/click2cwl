import os
import sys
import gdal
import numpy as np
import logging
import click
from pystac import *
from shapely.wkt import loads
from time import sleep
from .helpers import get_item, cog, set_env, get_assets, normalized_difference, generate_evi, generate_savi, generate_msavi, writeFile, getBands_and_Mask
import matplotlib.pyplot as plt
import matplotlib.colors as colors



logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

workflow = dict([('id', 'vegetation-index'),
                ('label', 'Vegetation index'),
                ('doc', 'Vegetation index processor')])

aoi = dict([('id', 'aoi'), 
              ('label', 'Area of interest'),
              ('doc', 'Area of interest in WKT'),
              ('value', 'POLYGON((136.508 -36.108,136.508 -35.654,137.178 -35.654,137.178 -36.108,136.508 -36.108))'), 
              ('type', 'string')])

input_reference = dict([('id', 'input_reference'), 
                        ('label', 'EO product for vegetation index'),
                        ('doc', 'EO product for vegetation index'),
                        ('value', '/workspace/application-chaining/68nl6_bz/s2-pre'), # this is created in the stage-in process
                        ('type', 'Directory'),
                        ('stac:collection', 'source'),
                        ('stac:href', 'catalog.json'),
                        ('scatter', 'True')])

scale_factor = 0.0001
range_min = -10000
range_max = 10000
nodata = -11111
datatype = np.int16

@click.command()
@click.option('--input_reference', '-i', 'e_input_reference', help=input_reference['doc'])
@click.option('--aoi', '-a', 'e_aoi', default=None, help=aoi['doc'])
def entry(e_input_reference, e_aoi):
    
    input_reference['value'] = e_input_reference # overwrites the "default" value with the one entered in the command line
    
    if e_aoi is not None: 
        aoi['value'] = e_aoi # replace with aoi entered
    else: 
        aoi['value'] = None
        
    main(input_reference, aoi)

def main(input_reference, aoi):
    
    set_env()
    
    item = get_item(os.path.join(input_reference['value'], 'catalog.json'))
    
    cat = Catalog.from_file(os.path.join(input_reference['value'], 'catalog.json')) # Catalog is saved in the input_reference['value'] path (filename catalog.json)
    
    # Extract your assets (ie input data bands)
    asset_blue, asset_green, asset_red, asset_nir, asset_swir16, asset_swir22 = get_assets(item)
    
    vrt = '{0}.vrt'.format(item.id)
    logging.info('- vrt name: ' + vrt)
    
    ds = gdal.BuildVRT(vrt,
                   [asset_blue, asset_green, asset_red, asset_nir, asset_swir16, asset_swir22],
                   srcNodata=nodata,
                   xRes=10, 
                   yRes=10,
                   separate=True)
    #logging.info('- ds loaded correctly')
    
    ds.FlushCache() 
    

    ds = None; del(ds)
    
    #logging.info('- now preparing tif')
    tif = '{0}.tif'.format(item.id)
    logging.info('- tif name: ' + tif)
    
    if not aoi['value']: # in case aoi['value'] is Null
        
        min_lon, min_lat, max_lon, max_lat = None, None, None, None
    
    else:
        
        min_lon, min_lat, max_lon, max_lat = loads(aoi['value']).bounds
        logging.info('- ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat))
        logging.info('- check bbox of item: ' + str(item.bbox)) # 106.80765, -7.32209, 107.80392, -6.324961

        # manually define new bounds to fit the temporary image
        #min_lon, min_lat, max_lon, max_lat = 106.85, -7.30, 107.80, -6.35
        #logging.info('- ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat))
        
    #logging.info('- ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat))
    
    os.environ['PREFIX'] = '/opt/anaconda/envs/env_vi/'
    os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 'share/proj')
    os.environ['GPT_BIN'] = os.path.join(os.environ['PREFIX'], 'snap/bin/gpt')
    
    gdal.Translate(tif,
                   vrt,
                   outputType=gdal.GDT_Int16,
                   projWin=[min_lon, max_lat, max_lon, min_lat] if aoi['value'] != None else None,
                   projWinSRS='EPSG:4326')
    
    #logging.info('- translate ok')
    os.remove(vrt)
    logging.info('- tiff created successfully. Now load with gdal.Open')
    
    ds = gdal.Open(tif)
    width = ds.RasterXSize
    height = ds.RasterYSize
    logging.info('- width & height: ' + str(width) + ' ' + str(height))
    
    input_geotransform = ds.GetGeoTransform()
    input_georef = ds.GetProjectionRef()
    
    blue, green, red, nir, swir16, swir22, mask = getBands_and_Mask(ds)
    
    ds = None
    os.remove(tif)
    del(ds)
    
    #----------------------------------------------
    """Now calculate Spectral Indices. The list is:
    --> info here: https://www.usgs.gov/core-science-systems/nli/landsat/landsat-surface-reflectance-derived-spectral-indices?qt-science_support_page_related_con=0#qt-science_support_page_related_con)"""

    # Normalized Difference Vegetation Index (NDVI)
    ndvi = normalized_difference(mask, nir, red)

    # Enhanced Vegetation Index (EVI) 
    evi = generate_evi(mask, blue, red, nir, C1 = 6, C2 = 7.5, L_evi = 1) 

    # Soil Adjusted Vegetation Index (SAVI)
    savi = generate_savi(mask, red, nir, L_savi = 0.428)

    # Modified Soil Adjusted Vegetation Index (MSAVI)
    msavi = generate_msavi(mask, red, nir)

    # Normalized Difference Moisture Index (NDMI) or Burn Ratio (NBR) or Water Index (NDWI) 
    ndmi = normalized_difference(mask, nir, swir22)
    nbr = normalized_difference(mask, nir, swir22)
    ndwi = normalized_difference(mask, nir, swir22)

    # Normalized Burn Ratio 2 (NBR2)
    nbr2 = normalized_difference(mask, swir16, swir22)

    # Normalized Difference Built-up Index (NDBI)
    ndbi = normalized_difference(mask, swir22, nir)

    logging.info('- Spectral Indices calculated successfully.')
    #----------------------------------------------
    
    # Delete bands as not in use anymore
    blue = green = red = nir = swir16 = swir22 = None
    del(blue); del(green); del(red); del(nir); del(swir16); del(swir22) 
    
    # Create a new Item (of EO extenstion class) with same metadata as original Item, but with all Spectral Indices as separate bands 
    default_bands = [{'name': 'NDVI', 'common_name': 'ndvi'},
                     {'name': 'EVI', 'common_name': 'evi'},
                     {'name': 'SAVI', 'common_name': 'savi'},
                     {'name': 'MSAVI', 'common_name': 'msavi'},
                     {'name': 'NDMI', 'common_name': 'ndmi'},
                     {'name': 'NBR', 'common_name': 'nbr'}, 
                     {'name': 'NDWI', 'common_name': 'ndwi'},
                     {'name': 'NBR2', 'common_name': 'nbr2'}, 
                     {'name': 'NDBI', 'common_name': 'ndbi'}]
    
    catalog = Catalog(id='catalog-{}'.format(item.id),
                      description='Results')

    catalog.clear_items()
    catalog.clear_children()
    
    item_name = 'INDEX_{}'.format(item.id)
    
    item.properties.pop('eo:bands', None)
    item.properties['eo:gsd'] = 10
    item.properties['eo:platform'] = item.properties['platform']
    item.properties['eo:instrument'] = 'MSI'
    
    # create an object of pystac.Item clas, from which I can use the add_asset() and get_assets methods: https://pystac.readthedocs.io/en/latest/_modules/pystac/item.html  
    result_item = Item(id=item_name,
                       geometry=item.geometry,
                       bbox=item.bbox,
                       datetime=item.datetime,
                       properties=item.properties)
    
    result_item.common_metadata.set_gsd(item.properties['eo:gsd']) 
    
    # Define my Item with EOItemExt from pystac https://pystac.readthedocs.io/en/latest/api.html
    eo_item = extensions.eo.EOItemExt(result_item)
    
    bands = [] 
    
    for index, veg_index in enumerate(['NDVI', 'EVI', 'SAVI', 'MSAVI', 'NDMI', 'NBR', 'NDWI', 'NBR2', 'NDBI']): # ensure these are in the same order as default_bands
        print('- Working on:', index, veg_index)
        
        temp_name = '_{}_{}.tif'.format(veg_index, item.id)
        output_name = '{}_{}.tif'.format(veg_index, item.id)

        vi_arr = veg_index.lower()
      
        writeFile(temp_name,input_geotransform,input_georef,locals()[vi_arr],width,height)

        os.makedirs(os.path.join('.', item_name),
                    exist_ok=True)
        
        cog(temp_name, os.path.join('.', item_name, output_name)) # takes temporary and output folder names)

        result_item.add_asset(key=vi_arr,
                              asset=Asset(href='./{}'.format(output_name), 
                                          media_type=MediaType.GEOTIFF))
        
        asset = result_item.get_assets()[vi_arr]                                   
        
        #description = bands[index]['name']
            
        stac_band = extensions.eo.Band.create(name=vi_arr,
                                              common_name=default_bands[index]['common_name'],
                                              description=default_bands[index]['name'])
        bands.append(stac_band)
        
        eo_item.set_bands([stac_band], asset=asset)
        
    eo_item.set_bands(bands) # isnt this redundant given the line above in hte for loop?   
    
    eo_item.apply(bands) # would be good to apply a cloud mask here as additional attribute: cloud_cover=(None default)
        
    catalog.add_items([result_item])
    
    catalog.normalize_and_save(root_href='./',
                               catalog_type=CatalogType.SELF_CONTAINED)
    print('\nEnd.')
    stop
    
if __name__ == '__main__':
    
    entry()

            

    




