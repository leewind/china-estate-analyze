from shapely import wkt
from shapely.geometry import Point
import geojson
import pandas as pd
import numpy as np
import keplergl
from odps.df import DataFrame
from util import GisTransform
import json
from shapely.geometry import MultiPoint, Polygon
import geopandas
import hashlib

hl = hashlib.md5()
gis = GisTransform('wgs84', 'gcj02')

def transfer(i, name):
    t = i.split('_')
    
    points = []
    
    for p in t:
        p2 = p.split(',')
        pair = gis.gcj02_to_wgs84(float(p2[0]), float(p2[1]))
        points.append([pair[0], pair[1]])
    
    return json.dumps({
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [points]
      },
      "properties": {
        "name": name
      }
    })

def create(row, odf):
    config = {'version': 'v1',
     'config': {'visState': {'filters': [],
       'layers': [{'id': '8m7d8xn',
         'type': 'geojson',
         'config': {'dataId': 'shop_loc',
          'label': 'shop_loc',
          'color': [195, 208, 57],
          'columns': {'geojson': '_geojson'},
          'isVisible': True,
          'visConfig': {'opacity': 0.95,
           'thickness': 0.5,
           'strokeColor': None,
           'colorRange': {'name': 'Global Warming',
            'type': 'sequential',
            'category': 'Uber',
            'colors': ['#5A1846',
             '#900C3F',
             '#C70039',
             '#E3611C',
             '#F1920E',
             '#FFC300']},
           'strokeColorRange': {'name': 'Global Warming',
            'type': 'sequential',
            'category': 'Uber',
            'colors': ['#5A1846',
             '#900C3F',
             '#C70039',
             '#E3611C',
             '#F1920E',
             '#FFC300']},
           'radius': 10,
           'sizeRange': [0, 10],
           'radiusRange': [0, 50],
           'heightRange': [0, 500],
           'elevationScale': 5,
           'stroked': False,
           'filled': True,
           'enable3d': False,
           'wireframe': False},
          'textLabel': [{'field': None,
            'color': [255, 255, 255],
            'size': 18,
            'offset': [0, 0],
            'anchor': 'start',
            'alignment': 'center'}]},
         'visualChannels': {'colorField': None,
          'colorScale': 'quantile',
          'sizeField': None,
          'sizeScale': 'linear',
          'strokeColorField': None,
          'strokeColorScale': 'quantile',
          'heightField': None,
          'heightScale': 'linear',
          'radiusField': None,
          'radiusScale': 'linear'}},
        {'id': 'njmuyyv',
         'type': 'geojson',
         'config': {'dataId': 'shop_delivery_area',
          'label': 'shop_delivery_area',
          'color': [254, 137, 26],
          'columns': {'geojson': '_geojson'},
          'isVisible': True,
          'visConfig': {'opacity': 0.24,
           'thickness': 0.5,
           'strokeColor': [130, 154, 227],
           'colorRange': {'name': 'Global Warming',
            'type': 'sequential',
            'category': 'Uber',
            'colors': ['#5A1846',
             '#900C3F',
             '#C70039',
             '#E3611C',
             '#F1920E',
             '#FFC300']},
           'strokeColorRange': {'name': 'Global Warming',
            'type': 'sequential',
            'category': 'Uber',
            'colors': ['#5A1846',
             '#900C3F',
             '#C70039',
             '#E3611C',
             '#F1920E',
             '#FFC300']},
           'radius': 10,
           'sizeRange': [0, 10],
           'radiusRange': [0, 50],
           'heightRange': [0, 500],
           'elevationScale': 5,
           'stroked': True,
           'filled': True,
           'enable3d': False,
           'wireframe': False},
          'textLabel': [{'field': None,
            'color': [255, 255, 255],
            'size': 18,
            'offset': [0, 0],
            'anchor': 'start',
            'alignment': 'center'}]},
         'visualChannels': {'colorField': None,
          'colorScale': 'quantile',
          'sizeField': None,
          'sizeScale': 'linear',
          'strokeColorField': None,
          'strokeColorScale': 'quantile',
          'heightField': None,
          'heightScale': 'linear',
          'radiusField': None,
          'radiusScale': 'linear'}},
        {'id': 'r0tp09r',
         'type': 'hexagon',
         'config': {'dataId': 'heatmap',
          'label': 'user',
          'color': [30, 150, 190],
          'columns': {'lat': 'user_latitude', 'lng': 'user_longitude'},
          'isVisible': True,
          'visConfig': {'opacity': 0.8,
           'worldUnitSize': 0.05,
           'resolution': 8,
           'colorRange': {'name': 'ColorBrewer Reds-6',
            'type': 'singlehue',
            'category': 'ColorBrewer',
            'colors': ['#fee5d9',
             '#fcbba1',
             '#fc9272',
             '#fb6a4a',
             '#de2d26',
             '#a50f15']},
           'coverage': 1,
           'sizeRange': [0, 500],
           'percentile': [0, 100],
           'elevationPercentile': [0, 100],
           'elevationScale': 5,
           'colorAggregation': 'sum',
           'sizeAggregation': 'count',
           'enable3d': False},
          'textLabel': [{'field': None,
            'color': [255, 255, 255],
            'size': 18,
            'offset': [0, 0],
            'anchor': 'start',
            'alignment': 'center'}]},
         'visualChannels': {'colorField': {'name': 'value', 'type': 'integer'},
          'colorScale': 'quantile',
          'sizeField': None,
          'sizeScale': 'linear'}}],
       'interactionConfig': {'tooltip': {'fieldsToShow': {'shop_delivery_area': [],
          'shop_loc': [],
          'heatmap': ['tracking_id', 'value']},
         'enabled': True},
        'brush': {'size': 0.5, 'enabled': False}},
       'layerBlending': 'normal',
       'splitMaps': [],
       'animationConfig': {'currentTime': None, 'speed': 1}},
      'mapState': {'bearing': 0,
       'dragRotate': False,
       'latitude': 25.046293545256706,
       'longitude': 102.68942390403629,
       'pitch': 0,
       'zoom': 12.65144314957595,
       'isSplit': False},
      'mapStyle': {'styleType': 'dark',
       'topLayerGroups': {},
       'visibleLayerGroups': {'label': True,
        'road': True,
        'border': False,
        'building': True,
        'water': True,
        'land': True,
        '3d building': False},
       'threeDBuildingColor': [9.665468314072013,
        17.18305478057247,
        31.1442867897876],
       'mapStyles': {}}}}


    shopmap = keplergl.KeplerGl(height=800)  
    shopmap.config = config

    shopmap.add_data(data=geopandas.GeoSeries([Polygon(row['polygon_points'])]).to_json(), name='shop_delivery_area')
    shopmap.add_data(data=geopandas.GeoSeries([MultiPoint(row['shop_lnglat_group'])]).to_json(), name='shop_loc')
    shopmap.add_data(data=odf, name='heatmap')
    
    hl.update(row['shop_id_set'].encode(encoding='utf-8'))
    shopmap.save_to_html(file_name='html/'+hl.hexdigest() + '.html')