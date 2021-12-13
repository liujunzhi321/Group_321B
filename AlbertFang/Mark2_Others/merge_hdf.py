"""
Created on 2021-11-14
Author = Alber Fang
"""
import os
import xarray as xr
import rioxarray as rioxr
import gdal
from netCDF4 import Dataset
from xarray.backends.api import open_dataset


# def merge_hdf_1():
#     fd = r'E:\GroupMenbers\Qirong\modis'
#     filename_list = os.listdir(fd)
#     for fn in filename_list:
#         fp = os.path.join(fd, fn)
#         # hdf_file = gdal.Open(fp)
#         # subDatasets = hdf_file.GetSubDatasets()
#         # print(subDatasets)
#         # source_fp = r'"E:\GroupMenbers\Qirong\modis\MOD11A2.A2000057.h23v04.006.2015057173525.hdf"'
#         # source_fp = "HDF4_EOS:EOS_GRID:'{}':MODIS_Grid_8Day_1km_LST:{}".format(fp, 'LST_Day_1km')
#         source_fp = 'HDF4_EOS:EOS_GRID:"E:\\GroupMenbers\\Qirong\\modis\\MOD11A2.A2000057.h23v04.006.2015057173525.hdf":MODIS_Grid_8Day_1km_LST:QC_Day'
#         target_fp = os.path.join(fd, 'test.tif')
#         cmd = "gdal_translate -of GTiff " + source_fp + " " + target_fp
#         print(cmd)
#         os.system(cmd)
        
#         break

def merge_hdf():
    from pymodis import convertmodis_gdal
    import pprint
    import glob
    
    fd = r'E:\GroupMenbers\Qirong\modis_1'
    hdf_list = glob.glob(os.path.join(fd, r'*.hdf'))
    modis_mosaic = convertmodis_gdal.createMosaicGDAL(hdfnames = hdf_list, subset=[1, 0, 1], outformat='GTiff')
    modis_mosaic.run(os.path.join(fd, r'mosaic_hdf_1.tif'))


def transform_geotiff():
    pass




if __name__ == "__main__":
    merge_hdf()