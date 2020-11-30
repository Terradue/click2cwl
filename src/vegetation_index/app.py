import os
import sys
import gdal
import numpy as np
import logging
import click
from pystac import *
from shapely.wkt import loads
from time import sleep
from .helpers import get_item, cog, set_env, get_assets, normalized_difference, generate_evi, generate_savi, generate_msavi

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
                   srcNodata=0,
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
        min_lon, min_lat, max_lon, max_lat = 106.85, -7.30, 107.80, -6.35
        logging.info('- ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat))
        
    #logging.info('- ' + str(min_lon) + ' ' + str(min_lat) + ' ' + str(max_lon) + ' ' + str(max_lat))
    
    os.environ['PREFIX'] = '/opt/anaconda/envs/env_vi/'
    os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 'share/proj')
    os.environ['GPT_BIN'] = os.path.join(os.environ['PREFIX'], 'snap/bin/gpt')
    
    gdal.Translate(tif,
                   vrt,
                   outputType=gdal.GDT_Int16,
                   projWin=[min_lon, max_lat, max_lon, min_lat] if aoi['value'] else None, # in the format [ulx, uly, lrx, lry]
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
    
    blue = ds.GetRasterBand(1).ReadAsArray(); print('blue', np.nanmin(blue), np.nanmax(blue))
    green = ds.GetRasterBand(2).ReadAsArray() ; print('green', np.nanmin(green), np.nanmax(green))
    red = ds.GetRasterBand(3).ReadAsArray(); print('red', np.nanmin(red), np.nanmax(red))
    nir = ds.GetRasterBand(4).ReadAsArray(); print('nir', np.nanmin(nir), np.nanmax(nir))
    swir16 = ds.GetRasterBand(5).ReadAsArray(); print('swir16', np.nanmin(swir16), np.nanmax(swir16))
    swir22 = ds.GetRasterBand(6).ReadAsArray(); print('swir22', np.nanmin(swir22), np.nanmax(swir22))
    
    ds = None
    os.remove(tif)
    del(ds)
    
    #----------------------------------------------
    """Now calculate Spectral Indices. The list is:
    --> info here: https://www.usgs.gov/core-science-systems/nli/landsat/landsat-surface-reflectance-derived-spectral-indices?qt-science_support_page_related_con=0#qt-science_support_page_related_con)"""
    
    # Normalized Difference Vegetation Index (NDVI) = (NIR - R) / (NIR + R)
    ndvi = normalized_difference(nir, red)
    
    # Enhanced Vegetation Index (EVI) = 2.5 * G * ((NIR - R) / (NIR + C1 * R – C2 * B + L_evi)) # notice a 2.5 missing in Landsat reference. 
    evi = generate_evi(blue, red, nir, C1 = 6, C2 = 7.5, L_evi = 1) # these are values used in S2 example here: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/evi/#
    
    # Soil Adjusted Vegetation Index (SAVI) = ((NIR - R) / (NIR + R + L_savi)) * (1 + L_savi)
    savi = generate_savi(red, nir, L_savi = 0.5)
    
    # Modified Soil Adjusted Vegetation Index (MSAVI) = (2 * NIR + 1 – sqrt ((2 * NIR + 1)^2 – 8 * (NIR - R))) / 2
    msavi = generate_msavi(red, nir)
    
    # Normalized Difference Moisture Index (NDMI) or Normalized Burn Ratio (NBR) or Normalized Difference Water Index (NDWI) ==> # NDMI or NBR or NDWI = (NIR - SWIR) / (NIR + SWIR)
    ndmi = normalized_difference(nir, swir22)
    nbr = normalized_difference(nir, swir22)
    ndwi = normalized_difference(nir, swir22)
    
    # Normalized Burn Ratio 2 (NBR2) = (SWIR1 – SWIR2) / (SWIR1 + SWIR2)
    nbr2 = normalized_difference(swir16, swir22)
    
    # Normalized Difference Built-up Index (NDBI) (SWIR - NIR) / (SWIR + NIR)
    ndbi = normalized_difference(swir22, nir)
    
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
    
    eo_item = extensions.eo.EOItemExt(result_item) # from pystac https://pystac.readthedocs.io/en/latest/api.html
    
    # the following lines have been replaced by the for loop I think...
    #eo_item.common_metadata.set_gsd(10)

    #result_item = EOItem(id=item_name,
    #                     geometry=item.geometry,
    #                     bbox=item.bbox,
    #                     datetime=item.datetime,
    #                     properties={},
    #                     bands=bands,
    #                     gsd=10, 
    #                     platform=item.platform, 
    #                     instrument=item.instrument)
    
    bands = [] # what does this refer to?!?!
    
    for index, veg_index in enumerate(['NDVI', 'EVI', 'SAVI', 'MSAVI', 'NDMI', 'NBR', 'NDWI', 'NBR2', 'NDBI']): # ensure these are in the same order as default_bands
        print('- Working on:', index, veg_index)
        
        temp_name = '_{}_{}.tif'.format(veg_index, item.id)
        output_name = '{}_{}.tif'.format(veg_index, item.id)

        driver = gdal.GetDriverByName('GTiff')

        output = driver.Create(temp_name, 
                               width, 
                               height, 
                               1, 
                               gdal.GDT_Int16)

        output.SetGeoTransform(input_geotransform)
        output.SetProjection(input_georef)
        #output.GetRasterBand(1).WriteArray(nbr) # shouldnt this be the actual array of each SI ie key=veg_index.lower()
        
        output.GetRasterBand(1).WriteArray(locals()[veg_index.lower()]) # im using the variable given its name as str 
        
        output.FlushCache()

        sleep(2) # why this?

        output = None; del(output)

        os.makedirs(os.path.join('.', item_name),
                    exist_ok=True)
        
        cog(temp_name, os.path.join('.', item_name, output_name)) # takes temporary and output folder names)

        result_item.add_asset(key=veg_index.lower(),
                              asset=Asset(href='./{}'.format(output_name), 
                                          media_type=MediaType.GEOTIFF))
        
        asset = result_item.get_assets()[veg_index.lower()]                                   
        
        #description = bands[index]['name']
            
        stac_band = extensions.eo.Band.create(name=veg_index.lower(),
                                              common_name=default_bands[index]['common_name'],
                                              description=default_bands[index]['name'])
        bands.append(stac_band)
        
        eo_item.set_bands([stac_band], asset=asset)
        
    eo_item.set_bands(bands)
    print('- eo_bands complete:', bands)
    
    eo_item.apply(bands)    
    
        #result_item.add_asset(key=veg_index.lower(),
        #                      asset=EOAsset(href='./{}'.format(output_name), 
        #                      media_type=MediaType.GEOTIFF, 
        #                      title=bands[index]['name'],
        #                      bands=[bands[index]]))
        
    catalog.add_items([result_item])
    
    catalog.normalize_and_save(root_href='./',
                               catalog_type=CatalogType.SELF_CONTAINED)
    print('\nEnd.')
    stop
    
if __name__ == '__main__':
    entry()

            

    




