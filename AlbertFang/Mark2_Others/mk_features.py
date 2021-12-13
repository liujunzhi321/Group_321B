"""
Create on 2021-11-10

Author = Albert Fang
"""
from shapely import geometry
import numpy as np
import pandas as pd
import geopandas as gpd
import os

def mk_line():
    cq = gpd.GeoSeries([geometry.LineString([(lon, 32) for lon in np.arange(-180, 180, 0.1)])],
                         crs='EPSG:4326',
                         index=['32N'])

    print(cq)
    cq.to_file(r'J:\Data\shapefile\32N\32N.shp')
    return

def mk_point(df, lon_id, lat_id):
    from shapely import geometry
    # df = pd.read_excel(fp)
    lats, lons = df[lat_id], df[lon_id]
    points = zip(lons, lats)
    geo_points = [geometry.Point(pt) for pt in points]
    gdf = gpd.GeoDataFrame(df,
                            geometry=geo_points, crs='EPSG:4326')
    # gdf.to_file(r'I:\Data\DOC\Shapefile\GlcDOCMean_withoutNodata\GlcDOCMean_withoutNodata.shp', encoding='utf-8')
    return gdf

def main():
    # fp = r'E:\liu\冰川\distribution\mean\All_type_data_mean_abundance.xlsx'
    fp = r'E:\liu\2018年藏东南河流.xlsx'
    df = pd.read_excel(fp)

    gdf = mk_point(df, 'longtitude', 'latitude').to_crs('ESRI:102025')
    output_fp = r'landcover_percent\Data\2018_ZangdongnanRiver.shp'
    gdf.to_file(output_fp)

if __name__ == '__main__':
    main()

