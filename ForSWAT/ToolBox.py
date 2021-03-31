# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 21:26:33 2021

@author: Albert
"""
import geopandas as gpd
import xarray as xr
import rioxarray as rioxr
import numpy as np
import os

workplace = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan'

def mk_mask(region_fp, raster_fp, output_fp):
    """
    在指定区域运行SWAT，需准备相应的数据有，气象强迫数据（降雨，相对湿度，短波辐射，风速，温度）：
    在气象数据的栅格数据中，以区域内每个栅格作为站点提取气象强迫数据序列。
    -------------------------------------------------------
    parameters:
        
    returns:
        
    """
    shapefile = gpd.GeoDataFrame.from_file(region_fp)      # 读取矢量文件
    raster_data = rioxr.open_rasterio(raster_fp)[0]           # 读取栅格文件
    raster_data.rio.set_crs(shapefile.crs)              # 统一坐标系
    clipped = raster_data.rio.clip(shapefile['geometry'], drop=False)   # 以矢量边界剪切栅格数据
    mask = np.where(clipped == clipped._FillValue, np.nan, 1)
    da= xr.DataArray(mask,
                      dims=('lat', 'lon'),
                      coords={"lat": np.arange(54.95, 15.05-0.01, -0.1),
                              "lon": np.arange(70.05, 139.95+0.01, 0.1)
                              })
    ds = xr.Dataset({'mask': da})
    ds.to_netcdf(output_fp)
    return
    
if __name__ == '__main__':
    region_fp   = os.path.join(workplace, r'studyArea/watershed_WGS1984/watershed_WGS1984.shp')
    raster_fp = r'I:\foring_data_of_China_1979-2018\Data_forcing_01dy_010deg\lrad_ITPCAS-CMFD_V0106_B-01_01dy_010deg_197901-197912.nc'
    output_fp   = os.path.join(workplace, r'studyArea\MaskForITPCAS\MaskForITPCAS.nc')
    
    mk_mask(region_fp, raster_fp, output_fp)
    