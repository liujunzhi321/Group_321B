"""
将下载的土地利用栅格片段进行拼接
"""

import rioxarray as rioxr
from rioxarray.merge import merge_arrays
import os
from osgeo import gdal

def merge_data():
    lc_fd = r'/share/home/liujunzhi/liujunzhi/Albert/landcover/landcoverData'
    lc_fnList = os.listdir(lc_fd)
    raster_list = []
    for fn in lc_fnList:
        fp = os.path.join(lc_fd, fn)
        da = rioxr.open_rasterio(fp)
        raster_list.append(da)
    print("Data loaded!")
    merged = merge_arrays(raster_list)
    merged_albers = merged.rio.reproject('ESRI:102025')
    # print("投影转换完成！")
    output_fp = r'/share/home/liujunzhi/liujunzhi/Albert/landcover/TempData/mergedLandcoverData_extent.tif'
    merged_albers.rio.to_raster(output_fp, compress='LZW')

def compress(path, target_path, method="LZW"): #
    """使用gdal进行文件压缩，
          LZW方法属于无损压缩，
          效果非常给力，4G大小的数据压缩后只有三十多M"""
    dataset = gdal.Open(path)
    driver = gdal.GetDriverByName('GTiff')
    driver.CreateCopy(target_path, dataset, strict=1, options=["TILED=YES", "COMPRESS={0}".format(method)])
    del dataset

if __name__ == '__main__':
    merge_data()