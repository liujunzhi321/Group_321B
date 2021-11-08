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
        'catchment' : r'J:\Data\shapefile\BaseData_20211107\LocalCatchment\local_catchment_albers.shp',
        'watershed' : r'J:\Data\shapefile\BaseData_20211107\UpstreamWatershed\upstream_watershed_albers.shp'
        }
    OUTPUT_FP = r'J:\WshdAttributes\Result\Updates\Updates-{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

elif platform.system() == 'Linux':
    fd = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Mark17_GetUpstreamAttri/Data/shapefile/BaseData_20211107'
    EXTENT_VEC_DICT = {
        'catchment' : os.path.join(fd, r'LocalCatchment/local_catchment_albers.shp'),
        'watershed' : os.path.join(fd, r'UpstreamWatershed/upstream_watershed_albers.shp'),
        }
    OUTPUT_FP = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Mark17_GetUpstreamAttri/Result/Updates/Updates-{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

# 计算比例的话应当注明 cmap, type_list，即原数据的土地利用类型和需要统计的土地利用类型
STAT_CONTROL_DICT = {
    # 'Elevation'                 : {'rst_fp': r'I:\Qinghai_Tibet_Plateau\DEM\TPDEM\tp_extent_dem.tif', 'categorical': False, 'c_stat_ways': ['mean', 'min', 'max'], 'w_stat_ways': ['mean']},
    'HFP'                       : {'rst_fp': r'J:\Data\ATLAS\anthropogenic\HumanFootprint\HFP2009.tif', 'categorical': False, 'c_stat_ways': ['mean', 'min', 'max'], 'w_stat_ways': ['mean']}
}


def mk_control_dict():
    if platform.system() == "Windows":
        fp = r'D:\Easy\my_code\Group_321B\AlbertFang\Mark1_LakeBasin\control_table_windows_20211108.csv'
    elif platform.system() == 'Linux':
        fp = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Mark17_GetUpstreamAttri/control_table_linux_20211108.csv'
    
    df = pd.read_csv(fp)
    control_table = df.set_index('attribute_name').T.to_dict('dict')
    # print(control_table)
    return control_table

if __name__ == '__main__':
    from pprint import pprint
    pprint(mk_control_dict())
    



