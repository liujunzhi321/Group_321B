"""
Created on 2021-11-09

Author = Albert Fang
"""

"""

"""

from posixpath import dirname
from numpy import dtype, uint
import rioxarray as rioxr
import geopandas as gpd
# import matplotlib.pyplot as plt
import os
import pandas as pd
import platform

def transform_albers_rst(rst_fp, target_rst_fp):
    """
    将clip栅格数据的范围，并将投影转化为Albers等面积投影，以方便比例的统计
    Params:
    Return:
        None
    """
    if platform.system() == "Windows":
        tp_fp = r'I:\Qinghai_Tibet_Plateau\青藏高原范围与界线数据\DBATP\DBATP\DBATP_Polygon.shp'
    elif platform.system() == 'Linux':
        tp_fp = r'/share/home/liujunzhi/liujunzhi/Albert/Data/DBATP/DBATP_Polygon.shp'
    rst = rioxr.open_rasterio(rst_fp)
    # print(rst.dtype)
    rst_crs = rst.rio.crs
    tp_df = gpd.read_file(tp_fp).to_crs(rst_crs)
    # print(tp_df.crs)
    clipped = rst.rio.clip(tp_df.envelope, from_disk=True).rio.reproject('ESRI:102025')
    clipped.rio.to_raster(target_rst_fp, compress='LZW')
    # # print(xds)
    return None


def compress(path, target_path, method="LZW"):
    """
    使用gdal进行文件压缩，
    LZW方法属于无损压缩，
    效果非常给力，4G大小的数据压缩后只有三十多M
    """
    from osgeo import gdal
    dataset = gdal.Open(path)
    driver = gdal.GetDriverByName('GTiff')
    driver.CreateCopy(target_path, dataset, strict=1, options=["TILED=YES", "COMPRESS={0}".format(method)])
    del dataset
    return


def main():
    if platform.system() == "Windows":
        fp = r'control_tablefiles_history\control_table_windows.csv'
        temp_fd = r'J:\Data\TempData\RasterClipedAlbers'
    elif platform.system() == 'Linux':
        fp = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Group_321B/AlbertFang/Mark1_LakeBasin/Control_tables/control_table_windows.csv'
        temp_fd = r'/share/home/liujunzhi/liujunzhi/Albert/Data/tempData/RasterClipedAlbers'
    
    df = pd.read_csv(fp).rst_fp
    for o_fp in df:
        print(o_fp)
        basename = os.path.splitext(os.path.basename(o_fp))[0]
        if basename == 'hdr':
            basename = os.path.dirname(o_fp).split(r'/')[-1]
        albers_fp = os.path.join(temp_fd, r'{}_clipped_albers.tif'.format(basename))
        # compress_fp = os.path.join(temp_fd, r"{}_com_clipped_albers.tif".format(basename))
        # print(compress_fp)
        # rst_fp = r'I:\foriaaang_data_of_China_1979-2018\数据整合\Monthly\temp_M01_Mean_20210913.tif'
        # target_fp = r'J:\Data\TempData\temp_M01_Mean_20210913_clip_albers.tif'
        # target_compressed_fp aaaaaa= r'J:\Data\TempData\temp_M01_Mean_20210913_clip_compressed_albers.tif'
        
        transform_albers_rst(o_fp, albers_fp)
        # compress(albers_fp, compress_fp)
        # os.remove(albers_fp)



if __name__ == "__main__":
   main()
