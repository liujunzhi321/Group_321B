"""
一般利用land use遥感图，提取每个站位的土地利用 (可以分500m, 1km, 2km, 5km, 10km,
25km buffer zones)，具体分为built-up land, corpland, woodland, shrubland, 
grassland, bareland和water bodies。
"""
__author__ = "Albert Fang"

from rasterstats import zonal_stats
import rioxarray as rioxr
import geopandas as gpd
import numpy as np
import pandas as pd
import os

cmap = {10: 'cropland',
        20: 'forest',
        30: 'grassland',
        40: 'shrubland',
        50: 'wetland',
        60: 'water',
        70: 'tundra',
        80: 'impervious surface',
        90: 'bareland',
        100: 'snow/ice', }

def mk_buffer(pt_shpData, radius):
    """
    制做缓冲区
    """
    buffer_geometry = pt_shpData.buffer(radius)
    d = {'sName'   : pt_shpData.SmpName,
         'sNo'     : range(1, len(pt_shpData)+1),
         'geometry': buffer_geometry}
    return gpd.GeoDataFrame(d, crs='ESRI:102025')


def stat_percent(vec_fp, rst_fp, attribute_name, key_word, stated_type_list='All', ):
    """
    计算土地利用数据中，各个类型的面积
    
    Params:
        vec_fp:   
            str, 需要进行统计的矢量数据的路径；
        rst_fp：
            str，土地利用数据，需是GDAL可读的数据格式，如tif
        attribute_name, 
            str, 这个变量用以在最后输出结果时，区分缓冲区的范围
        key_word:
            str, 提取点的id
            
    Return:
        stat_result_df.set_index(key_word):
            DataFame, 输出的结果

    """
    vec_data = gpd.read_file(vec_fp)
    key_word_list = vec_data[key_word].values
    if stated_type_list == 'All':
        type_list = [type_name for type_name in cmap.values()]
    else:
        type_list = stated_type_list.split(',')

    stat_result = zonal_stats(vec_fp, rst_fp, categorical=True, all_touched=True, category_map=cmap)
    count_sum   = zonal_stats(vec_fp, rst_fp, stats=['count', 'nodata'], all_touched=True, ) 

    stat_result_df = pd.DataFrame(stat_result, columns=type_list)
    count_sum_df   = pd.DataFrame(count_sum)
    stat_result_df = stat_result_df.div(np.array(count_sum_df.sum(axis=1)), axis=0).round(3)

    stat_result_df[key_word] = key_word_list
    rename_dict = {typename: '{}_{}'.format(attribute_name, typename) for typename in type_list}
    stat_result_df.rename(columns=rename_dict, inplace=True)
    # print(stat_result_df.set_index(self.key_word))
    return stat_result_df.set_index(key_word)


def different_buffer_stat_percent():
    albert_fd = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Group_321B/AlbertFang'
    pt_shapeData_fp = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Group_321B/AlbertFang/Mark2_Others/landcover_percent/Data/2018_ZangdongnanRiver.shp'
    rst_fp = r'/share/home/liujunzhi/liujunzhi/Albert/landcover/TempData/fromglc10v01_24_34_82_98Albers.tif'
    pt_shapeData_df = gpd.read_file(pt_shapeData_fp)
    result_list = []
    buffer_list = [0.5, 1, 2, 5, 10, 25]
    for radius in buffer_list:
        print("Make buffer radius {}km".format(radius))
        buffer_output_fd = os.path.join(albert_fd, r'Mark2_Others/landcover_percent/Data/ptBuffer{}km'.format(radius))
        if not os.path.exists(buffer_output_fd):
            os.mkdir(buffer_output_fd)
        buffer_output_fp = os.path.join(buffer_output_fd, r'ptBuffer{}km.shp'.format(radius))
        mk_buffer(pt_shapeData_df, radius*1e3).to_file(buffer_output_fp)
        stat_result_df = stat_percent(buffer_output_fp, rst_fp, 'buffer-{}'.format(radius), 'sName')
        result_list.append(stat_result_df, )
    result_df = pd.concat(result_list, axis=1)
    output_fp = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Group_321B/AlbertFang/Mark2_Others/landcover_percent/Result/Landcover_buffers.xlsx'
    result_df.to_excel(output_fp)
    return


def fillna():
    fp = r'J:\Marks\Mark1_landcover\Landcover_buffers.xlsx'
    df = pd.read_excel(fp)
    df.fillna(0).to_excel(r'J:\Marks\Mark1_landcover\Landcover_buffers_fillna.xlsx')

if __name__ == '__main__':
    fillna()
    
    # different_buffer_stat_percent()

    # get_info()

    # stat_percent()
    
    # zonal_statistics_2()
    # fp = r'I:\Qinghai_Tibet_Plateau\land_cover\Gongpeng\Task_20210507\Result\Buffer_500.xlsx'
    # cal_ratio(fp)
    # data_postProcessing()