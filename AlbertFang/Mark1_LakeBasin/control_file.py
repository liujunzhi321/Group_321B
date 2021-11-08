"""
Created on 2021-09-09

Author = Albert Fang
"""

"""
输入需要统计的属性
"""

import os
from re import escape
import pandas as pd
import platform
import datetime


# 分类数据查找表
# cmaps
CMAP_DICT = {
    'cmap_lu_tp' : {
        10  : 'cropland',
        20	: 'forest',
        30	: 'grassland',
        40	: 'shrub',
        50	: 'wetland-water',
        60	: 'urban land',
        70	: 'desert sparse ',
        80	: 'tundra',
        90	: 'bare land',
        100	: 'glacier',},

    'VegType_cmap' : {
        1   :   'Tropical Evergreen Forest/Woodland',
        2   :	'Tropical Deciduous Forest/Woodland',
        3   :	'Temperate Broadleaf Evergreen Forest/Woodland',
        4   :	'Temperate Needleleaf Evergreen Forest/Woodland',
        5   :	'Temperate Deciduous Forest/Woodland',
        6   :	'Boreal Evergreen Forest/Woodland',
        7   :	'Boreal Deciduous Forest/Woodland',
        8   :	'Evergreen/Deciduous Mixed Forest/Woodland',
        9   :	'Savanna',
        10  :	'Grassland/Steppe',
        11  :	'Dense Shrubland',
        12  :	'Open Shrubland',
        13  :	'Tundra',
        14  :	'Desert',
        15  :	'Polar Desert/Rock/Ice',},

    'WetlandType_cmap' : {
        1   : 'Lake', 
        2   : 'Reservoir',
        3   : 'River', 
        4   : 'Freshwater Marsh, Floodplain', 
        5   : 'Swamp Forest, Flooded Forest', 
        6   : 'Coastal Wetland (incl. Mangrove, Estuary, Delta, Lagoon)', 
        7   : 'Pan, Brackish/Saline Wetland', 
        8   : 'Bog, Fen, Mire (Peatland)', 
        9   : 'Intermittent Wetland/Lake', 
        10  : '50-100% Wetland', 
        11  : '25-50% Wetland', 
        12  : 'Wetland Compex (0-25% Wetland)' },

    'Urban_cmap' : {
        30: 'Urban Centre grid cell',
        23: 'Dense Urban Cluster grid cell', 
        22: 'Semi-dense Urban Cluster grid cell',
        21: 'Suburban or per-urban grid cell', 
        13: 'Rural cluster grid cell', 
        12: 'Low Density Rural grid cell', 
        11: 'Very low density rural grid cell', 
        10: 'Water grid cell'}, 

    } # End CMAP_DICT

# 矢量范围， 湖泊的本地流域和完整流域
if platform.system() == "Windows":
    EXTENT_VEC_DICT = {
        'catchment' : r'J:\Data\shapefile\catchment\catchment.shp',
        'watershed' : r'J:\Data\shapefile\watershed\watershed.shp'
        }
    OUTPUT_FP = r'J:\WshdAttributes\Result\Updates\Updates-{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

elif platform.system() == 'Linux':
    EXTENT_VEC_DICT = {
        'catchment' : r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Mark17_GetUpstreamAttri/Data/shapefile/catchment/catchment.shp',
        'watershed' : r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Mark17_GetUpstreamAttri/Data/shapefile/watershed/watershed.shp'
        }
    OUTPUT_FP = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Mark17_GetUpstreamAttri/Result/Updates/Updates-{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))


# 计算比例的话应当注明 cmap, type_list，即原数据的土地利用类型和需要统计的土地利用类型
STAT_CONTROL_DICT = {
    # 'Land cover classes'      : [r'I:\Data\土地利用\china_v31.tif', 'majority'],
    # 'Soil erosion 1992'       : [r'I:\Data\土壤侵蚀\XDA200402022-QZGY1992E.tif', 'mean'],
    # 'Soil erosion 2005'       : [r'I:\Data\土壤侵蚀\XDA200402022-QZGY2005E.tif', 'mean'],
    # 'Soil erosion 2015'       : [r'I:\Data\土壤侵蚀\XDA200402022-QZGY2015E.tif', 'mean'],

    # 'Permafrost'              : [r'I:\Data\冻土\tif1.tif', 'mean'], # PFI_NoFringe1.tif,
    # 'Wetland'                 : [r'I:\Data\湿地\wetland2000s1.tif', 'percent', ['wetland_1', 'wetland_2']],
    #'TP_LC2015'               : [r'I:\Data\土地利用\TP\tpluc20151.tif', 'percent', cmap_lu_tp, 'all'],
    # 'TP_LC2015'                 : {'rst_fp': r'I:\Data\土地利用\TP\tpluc20151.tif', "categorical": True, 'cmap': cmap_lu_tp, 'stated_type_list': 'All'},
    # 'TP_LC2005'               : [r'I:\Data\土地利用\TP\tpluc20051.tif', 'percent', cmap_lu_tp, 'all'],
    # 'TP_LC1992'               : [r'I:\Data\土地利用\TP\tpluc19921.tif', 'percent', cmap_lu_tp, 'all'],
    # 'PET'                     : [r'I:\Data\PET\pet_he_yr1.tif', 'mean'],
    # 'AET'                     : [r'I:\Data\ActualEvapotranspiration\aet_yr1.tif', 'mean'],
    # 'LST_day_m2s'             : [r'I:\Data\LST\LST_Day_1km_mean.tif', 'mean'],
    # 'LST_night_m2s'           : [r'I:\Data\LST\LST_Night_1km_mean.tif', 'mean'],
    # 'LST_day_allYear'         : [r'I:\Data\LST\LST_Day_1km_AllYear_mean.tif', 'mean'],
    # 'LST_night_AllYear'       : [r'I:\Data\LST\LST_Night_1km_AllYear_mean.tif', 'mean'],
    # 'Wind_speed'              : [r'I:\foring_data_of_China_1979-2018\数据整合\wind_mean_TP.tif', 'mean']

    # 'Elevation'                 : {'rst_fp': r'I:\Qinghai_Tibet_Plateau\DEM\TPDEM\tp_extent_dem.tif', 'categorical': False, 'c_stat_ways': ['mean', 'min', 'max'], 'w_stat_ways': ['mean']},
    'HFP'                       : {'rst_fp': r'J:\Data\ATLAS\anthropogenic\HumanFootprint\HFP2009.tif', 'categorical': False, 'c_stat_ways': ['mean', 'min', 'max'], 'w_stat_ways': ['mean']}
}


def mk_control_dict():
    if platform.system() == "Windows":
        fp = r'D:\Easy\my_code\Mark17_GetUpstreamAttri\control_table_windows.csv'
    elif platform.system() == 'Linux':
        fp = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Mark17_GetUpstreamAttri/control_table_linux.csv'
    
    df = pd.read_csv(fp)
    control_table = df.set_index('attribute_name').T.to_dict('dict')
    # print(control_table)
    return control_table

if __name__ == '__main__':
    from pprint import pprint
    pprint(mk_control_dict())
    



