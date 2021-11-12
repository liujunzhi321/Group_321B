from re import S, split
import pandas as pd
# from pprint import PrettyPrinter, pprint
import xarray as xr
import rioxarray as rioxr
# import matplotlib.pylab as plt
import geopandas as gpd
import numpy as np
import os


def get_meteo_filename_list(meteo):
    """
    因为有不同的气象要素需要提取，故需首先准备需要的数据的路径。
    后面需要进行求均值的处理
    """
    folderpath = r"/home/liujz/data/Forcing_data_of_China(1979-2018)/Data_forcing_03hr_010deg/{}".format(meteo)
    all_file_list = os.listdir(folderpath)
    the_file_list = []
    # print(len(all_file_list))
    for filename in all_file_list:
        if os.path.splitext(filename)[1] == '.nc':
            the_file_list.append(filename)
    filepath_list = [os.path.join(folderpath, filename) for filename in the_file_list]
    return filepath_list


def cal_prec_daily():
    fd = r'I:\foring_data_of_China_1979-2018\Data_forcing_01dy_010deg'
    prec_yearly_list = []
    for year in range(1979, 1980):
        prec_fp = r'prec_ITPCAS-CMFD_V0106_B-01_01dy_010deg_{}01-{}12.nc'.format(year, year)
        print(prec_fp)
        prec_filepath = os.path.join(fd, prec_fp)
        prec_ds = xr.open_dataarray(prec_filepath)
        prec_yearly = prec_ds.resample(time='1Y').sum(min_count=1)*24
        prec_yearly_list.append(prec_yearly)
    prec_yearly_all = xr.concat(prec_yearly_list, dim='time')
    prec_yearly_mean = prec_yearly_all.mean(dim='time')
    prec_yearly_mean.to_netcdf(r'C:\Users\Albert\Desktop\hh\prec_yearly_mean_d_1979.nc')
    return


def mk_shapefile(fp):
    from shapely import geometry
    df = pd.read_excel(fp)
    lats, lons = df.Lat, df.Lon
    points = zip(lons, lats)
    geo_points = [geometry.Point(pt) for pt in points]
    gdf = gpd.GeoDataFrame(df, geometry=geo_points, crs='EPSG:4326')
    # gdf.to_file(r'I:\Data\DOC\Shapefile\GlcDOCMean_withoutNodata\GlcDOCMean_withoutNodata.shp', encoding='utf-8')
    return gdf


def attach_prec_glacier():
    """
    为每一个冰川附上降水数据
    """
    fp = r'I:\Data\DOC\Result\storge\glacier_prec_0901.xlsx'
    glc_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile/GlacialDBATP/GlacialDBTPInfo.shp'
    df = pd.read_excel(fp)
    glc_data = gpd.read_file(glc_fp, encoding='utf-8')
    glc_data = pd.merge(glc_data, df, left_on='GLIMS_ID', right_on='GLIMS_ID', how='left')
    print(glc_data)
    glc_data.to_file(r'I:\Data\Glacier\GlacialDBTP.shp', encoding='utf-8')
    return


def get_cloest_point_value(sample_df, glc_df, attach_varname):
    """
    将冰川样点的值按照就近原则赋到就近的冰川上
    Case:
        这里是将表面冰样点的值赋到就近的冰川上
        和    将文献中的冰川损失量的值赋到就近的冰川上
    Parameters:
        sample_df  : GeoDataFrame, 是样点的数据；
        glc_df     : GeoDataFrame, 是冰川的数据；
        attach_varname: str, 来自样点数据，是想要往冰川数据上赋的属性。
    Return:
        glc_df     : GeoDataFrame, 是赋了值之后的冰川数据
    """
    sample_df = sample_df.to_crs(glc_df.crs)
    # 计算冰川中心点到就近DOC站点的距离
    glacia_centers  = np.asarray([glc_df.centroid.x, glc_df.centroid.y]).T
    sample_points = np.asarray([sample_df.centroid.x, sample_df.centroid.y]).T
    doc_point_num = sample_points.shape[0]
    dis_matrix = np.linalg.norm(np.tile(glacia_centers[np.newaxis, :, :], (doc_point_num, 1, 1)) - sample_points[:, np.newaxis, :], axis=2)
    # 得到最近站点的编号
    no_list = np.argmin(dis_matrix, axis=0)
    
    # 赋值
    glc_df['{}Idx'.format(attach_varname)] = no_list
    sample_value_list = [sample_df.iloc[no][attach_varname]  for no in no_list]
    glc_df[attach_varname] = sample_value_list
    return glc_df


def cal_lost_doc(obs_varname='TN(mg/L)'):
    """
    计算冰川中储存DOC/TN的损失量：
        delt S = sum(conc_i * M_i * S_i)
        Mass balance的单位是：kg m-2 yr-1
    """
    glc_fp    = r'Shapefile\GlacialDBTP.shp'
    mass_balance_fp = r'mass_balance.xlsx'
    sample_fp = r'Mean\All_type_data_mean.xlsx'

    glc_df  = gpd.read_file(glc_fp, encoding='utf-8')
    mass_balance_df = mk_shapefile(mass_balance_fp).to_crs(glc_df.crs)
    sample_df = mk_shapefile(sample_fp).to_crs(glc_df.crs)
    sample_df.dropna(axis=0, subset=[obs_varname], inplace=True)
    sample_specified_df = sample_df[sample_df.Type=='ice']

    # 赋值
    cn_attached_df = get_cloest_point_value(sample_specified_df, glc_df, obs_varname)
    mass_balance_attached_df = get_cloest_point_value(mass_balance_df, cn_attached_df, 'average Mass balances')
    conc = mass_balance_attached_df[obs_varname]
    mass = mass_balance_attached_df['average Mass balances']
    s = mass_balance_attached_df['Glc_Area']

    total_mass_balance = np.sum(conc * mass * s) * 1e-12 # Gg

    print(total_mass_balance)
    return


def cal_snow_doc_flux(obs_varname='DOC(mg/L)'):
    """
    计算雪的碳通量：
        D = sum(conc(i)*p(i)*s(i))
    """
    glc_fp    = r'Shapefile\GlacialDBTP.shp'
    sample_fp = r'Mean\All_type_data_mean.xlsx'

    glc_df  = gpd.read_file(glc_fp, encoding='utf-8')
    sample_df = mk_shapefile(sample_fp).to_crs(glc_df.crs)
    sample_df.dropna(axis=0, subset=[obs_varname], inplace=True)
    sample_specified_df = sample_df[sample_df.Type=='snow']

    # 赋值
    cn_attached_df = get_cloest_point_value(sample_specified_df, glc_df, obs_varname)
    conc = cn_attached_df[obs_varname]
    s = cn_attached_df['Glc_Area']
  
    # 计算通量
    D = np.sum(cn_attached_df[obs_varname] * cn_attached_df['prec'] * cn_attached_df['Glc_Area']) * 1e-12 # Gg yr-1
    print(D)
    return


if __name__ == '__main__':
    # cal_lost_doc()
    cal_snow_doc_flux()