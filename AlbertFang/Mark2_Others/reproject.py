import rioxarray as rioxr

def reproject(rst_fp, target_rst_fp):
    rst = rioxr.open_rasterio(rst_fp)
    rst.rio.reproject('ESRI:102025').rio.to_raster(target_rst_fp, compress='LZW')
    return None

if __name__ == "__main__":
    rst_fp = r'/share/home/liujunzhi/liujunzhi/Albert/landcover/TempData/mergedLandcoverData_extent_compress.tif'
    target_rst_fp = r'/share/home/liujunzhi/liujunzhi/Albert/landcover/TempData/mergedLandcoverData_extent_Albers_compress.tif'
    reproject(rst_fp, target_rst_fp)