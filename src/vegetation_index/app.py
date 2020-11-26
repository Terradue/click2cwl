import os
import sys
import gdal
import numpy as np
import logging
import click
from pystac import *
from shapely.wkt import loads
from time import sleep
from .helpers import get_item, cog, set_env, get_assets, normalized_difference#, generate_evi, generate_savi, generate_msavi


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
        aoi['value'] = e_aoi # replace with aoi entered, otherwise use default
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
    print('- vrt name:', vrt)
    
    ds = gdal.BuildVRT(vrt,
                   [asset_blue, asset_green, asset_red, asset_nir, asset_swir16, asset_swir22],
                   srcNodata=0,
                   xRes=10, 
                   yRes=10,
                   separate=True)
    print('- ds loaded correctly')
    
    ds.FlushCache() 
    

    ds = None; del(ds)
    
    print('- now preparing tif')
    tif = '{0}.tif'.format(item.id)
    print('- tif name', tif)
    
    #print(aoi['value'])
    if aoi['value']:
        
        min_lon, min_lat, max_lon, max_lat = loads(aoi['value']).bounds
        print('-', min_lon, min_lat, max_lon, max_lat)
        print('- check bbox of item:', item.bbox) # 106.80765, -7.32209, 107.80392, -6.324961

        # manually define new bounds to fit the temporary image
        min_lon, min_lat, max_lon, max_lat = [106.85, -7.30, 107.80, -6.35]
        print('-', min_lon, min_lat, max_lon, max_lat)
    else: 
        
        min_lon, min_lat, max_lon, max_lat = None, None, None, None
    #os.environ['PREFIX'] = '/opt/anaconda/envs/env_vi/'
    #os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 'share/proj')
    #os.environ['GPT_BIN'] = os.path.join(os.environ['PREFIX'], 'snap/bin/gpt')
    print('- envi updated')
    
    gdal.Translate(tif,
                   vrt,
                   outputType=gdal.GDT_Int16,
                   projWin=[min_lon, max_lat, max_lon, min_lat] if aoi['value'] else None, # in the format [ulx, uly, lrx, lry]
                   projWinSRS='EPSG:4326')
    
    print('- translate ok')
    os.remove(vrt)
    print('- tiff created successfully.\nNow load with gdal.Open')
    
    ds = gdal.Open(tif)
    width = ds.RasterXSize
    height = ds.RasterYSize

    input_geotransform = ds.GetGeoTransform()
    input_georef = ds.GetProjectionRef()
    
    blue = ds.GetRasterBand(1).ReadAsArray()
    green = ds.GetRasterBand(2).ReadAsArray()
    red = ds.GetRasterBand(3).ReadAsArray()
    nir = ds.GetRasterBand(4).ReadAsArray()
    swir16 = ds.GetRasterBand(5).ReadAsArray()
    swir22 = ds.GetRasterBand(6).ReadAsArray()
    
    ds = None
    os.remove(tif)
    del(ds)
    
    #----------------------------------------------
    """Now calculate Spectral Indices. The list is:
    Normalized Difference Vegetation Index (NDVI)
    Enhanced Vegetation Index (EVI)
    Soil Adjusted Vegetation Index (SAVI)
    Modified Soil Adjusted Vegetation Index (MSAVI)
    Normalized Difference Moisture Index (NDMI)
    Normalized Burn Ratio (NBR)
    Normalized Burn Ratio 2 (NBR2)
    Normalized Difference Water Index
    Normalized Difference Built-up Index
    --> info here: https://www.usgs.gov/core-science-systems/nli/landsat/landsat-surface-reflectance-derived-spectral-indices?qt-science_support_page_related_con=0#qt-science_support_page_related_con)"""
    stop
    # Normalized Difference Vegetation Index (NDVI) = (NIR - R) / (NIR + R)
    ndvi = normalized_difference(nir, red)
    
    # Enhanced Vegetation Index (EVI) = G * ((NIR - R) / (NIR + C1 * R – C2 * B + L_evi))
    #asset_evi = G*( (NIR - R) / (NIR + C1*R - C2*B + L_evi) )
    evi = generate_evi(blue, green, red, nir, C1 = 6, C2 = 7.5, L_evi = 1) # these are values used in S2 example here: https://custom-scripts.sentinel-hub.com/sentinel-2/evi/#. 
    
    # Soil Adjusted Vegetation Index (SAVI) = ((NIR - R) / (NIR + R + L_savi)) * (1 + L_savi)
    #asset_savi = ((NIR - R) / (NIR + R + L_savi)) * (1 + L_savi)
    savi = generate_savi(red, nir, L_savi = 0.5)
    
    # Modified Soil Adjusted Vegetation Index (MSAVI) = (2 * NIR + 1 – sqrt ((2 * NIR + 1)^2 – 8 * (NIR - R))) / 2
    #asset_msavi = (2*NIR + 1 – np.sqrt((2 * NIR + 1)**2 – 8*(NIR - R))) / 2
    msavi = generate_msavi(red, nir)
    
    # Normalized Difference Moisture Index (NDMI) or Normalized Burn Ratio (NBR) or Normalized Difference Water Index (NDWI)
    # NDMI or NBR or NDWI = (NIR - SWIR) / (NIR + SWIR)
    ndmi = normalized_difference(nir, swir22)
    nbr = normalized_difference(nir, swir22)
    ndwi = normalized_difference(nir, swir22)
    
    # Normalized Burn Ratio 2 (NBR2) = (SWIR1 – SWIR2) / (SWIR1 + SWIR2)
    nbr2 = normalized_difference(swir16, swir22)
    
    # Normalized Difference Built-up Index (NDBI) (SWIR - NIR) / (SWIR + NIR)
    ndbi = normalized_difference(swir22, nir)
    #----------------------------------------------
    
    # Now delete bands as not in use anymore
    blue = green = red = nir = swir16 = swir22 = None
    del(blue); del(green); del(red); del(nir); del(swir16); del(swir22) 
    
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
    
    result_item = Item(id=item_name,
                       geometry=item.geometry,
                       bbox=item.bbox,
                       datetime=item.datetime,
                       properties=item.properties)
    
    result_item.common_metadata.set_gsd(10) # replace '10' with 'item.properties['eo:gsd']'
    
    eo_item = extensions.eo.EOItemExt(result_item) # from pystac https://pystac.readthedocs.io/en/latest/api.html
    
    #eo_item.set_bands(bands) # if I want to set the bands I calculated (thought I must not delete them!)
    
    #eo_item.common_metadata.set_gsd(10)

                     #                     result_item = EOItem(id=item_name,
                     #    geometry=item.geometry,
                     #    bbox=item.bbox,
                     #    datetime=item.datetime,
                     #    properties={},
                     #    bands=bands,
                     #    gsd=10, 
                     #    platform=item.platform, 
                     #    instrument=item.instrument)
    bands = []
    
    for index, veg_index in enumerate(['NDVI', 'EVI', 'SAVI', 'MSAVI', 'NDMI', 'NBR', 'NDWI', 'NBR2', 'NDBI']): # ensure these are in the same order as default_bands

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
        output.GetRasterBand(1).WriteArray(nbr),

        output.FlushCache()

        sleep(5)

        output = None; del(output)

        os.makedirs(os.path.join('.', item_name),
                    exist_ok=True)

        cog(temp_name, os.path.join('.', item_name, output_name))

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
          
    eo_item.apply(bands)    
    
        #result_item.add_asset(key=veg_index.lower(),
        #                      asset=EOAsset(href='./{}'.format(output_name), 
        #                      media_type=MediaType.GEOTIFF, 
        #                      title=bands[index]['name'],
        #                      bands=[bands[index]]))
        
    catalog.add_items([result_item])
    
    catalog.normalize_and_save(root_href='./',
                               catalog_type=CatalogType.SELF_CONTAINED)
    
    
if __name__ == '__main__':
    print('ciao')
    #entry()

            

    




