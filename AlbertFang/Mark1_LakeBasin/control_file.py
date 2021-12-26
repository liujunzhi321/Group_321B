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
        12  : 'Wetland Compex (0-25% Wetland)' }, # END 'WetlandType_cmap'

    'WetlandTP_cmap' : {
        0  : '0',
        10 : '10',
        20 : '20',
        30 : '30',
    }, # END 'WetlandTP_cmap'    

    'Urban_cmap' : {
        30: 'Urban Centre grid cell',
        23: 'Dense Urban Cluster grid cell', 
        22: 'Semi-dense Urban Cluster grid cell',
        21: 'Suburban or per-urban grid cell', 
        13: 'Rural cluster grid cell', 
        12: 'Low Density Rural grid cell', 
        11: 'Very low density rural grid cell', 
        10: 'Water grid cell'}, # End Urban_cmap

    'soil_erosion_cmap': {
        1: 'slight',
        2: 'mild',
        3: 'moderate',
        4: 'intense',
        5: 'extremely intense',
        6: 'severe',
    }, # End soil_erosion_cmap

    'Lithological_cmap':{
        1   : "su",
        2   : "vb",
        3   : "ss",
        4   : "pb",
        5   : "sm",
        6   : "sc",
        7   : "va",
        8   : "mt",
        9   : "pa",
        10  : "vi",
        11  : "wb",
        12  : "py",
        13  : "pi",
        14  : "ev",
        15  : "nd",
        16  : "ig",
    }, #End Lithological_cmap


    } # End CMAP_DICT

# 矢量范围， 湖泊的本地流域和完整流域
if platform.system() == "Windows":
    fd = r'J:\Data\shapefile\BaseData_201111118'
    EXTENT_VEC_DICT = {
        'lake'      : os.path.join(fd, r'Lakes\Lakes.shp'),
        'catchment' : os.path.join(fd, r'LocalCatchment\LocalCatchment.shp'),
        'watershed' : os.path.join(fd, r'UpstreamWatershed\UpstreamWatershed.shp'),
        }
    OUTPUT_FP = r'J:\WshdAttributes\Result\Updates\Updates-{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

elif platform.system() == 'Linux':
    fd = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Group_321B/AlbertFang/Mark1_LakeBasin/Data/BaseData_201111118'
    EXTENT_VEC_DICT = {
        'lake'      : os.path.join(fd, r'Lakes/Lakes.shp'),
        'catchment' : os.path.join(fd, r'LocalCatchment/LocalCatchment.shp'),
        'watershed' : os.path.join(fd, r'UpstreamWatershed/UpstreamWatershed.shp'),
        }
    OUTPUT_FP = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Group_321B/AlbertFang/Mark1_LakeBasin/Result/Updates/Updates-{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

# 计算比例的话应当注明 cmap, type_list，即原数据的土地利用类型和需要统计的土地利用类型
STAT_CONTROL_DICT = {
    # 'Elevation'                 : {'rst_fp': r'I:\Qinghai_Tibet_Plateau\DEM\TPDEM\tp_extent_dem.tif', 'categorical': False, 'c_stat_ways': ['mean', 'min', 'max'], 'w_stat_ways': ['mean']},
    'HFP'                       : {'rst_fp': r'J:\Data\ATLAS\anthropogenic\HumanFootprint\HFP2009.tif', 'categorical': False, 'c_stat_ways': ['mean', 'min', 'max'], 'w_stat_ways': ['mean']}
}


def mk_control_dict():
    if platform.system() == "Windows":
        # fp = r'control_tablefiles_history\timeseries\control_table_lrad.csv'
        fp = r'control_tablefiles_history\control_table_windows.csv'
    elif platform.system() == 'Linux':
        # fp = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Group_321B/AlbertFang/Mark1_LakeBasin/Control_tables/control_table_windows.csv'
        fp = r'/share/home/liujunzhi/liujunzhi/Albert/mycode/Group_321B/AlbertFang/Mark1_LakeBasin/Control_tables/timeseries/control_table_prec.csv'
    df = pd.read_csv(fp)
    control_table = df.set_index('attribute_name').T.to_dict('dict')
    # print(control_table)
    return control_table

if __name__ == '__main__':
    from pprint import pprint
    pprint(mk_control_dict())
    



