# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 15:15:29 2021

@author: Administrator
"""

 
import geopandas as gpd
import pandas as pd
import os

def get_alpha(s):
    """
    过滤字符串中的数字
    """
    from string import digits
     
    remove_digits = str.maketrans('', '', digits)
    res = s.translate(remove_digits)
    return res
    # return list(filter(lambda x: x.isalpha(), s))

def mean_obs():
    """
    在观测的湖泊样点数据中每个湖泊可能会有多个采样点，因此需计算每个湖泊样点的平均值
    """
    base_dir = r'I:\Qinghai_Tibet_Plateau\LakeDOC\Data\Obs'
    filename = r'lakeDOC_groupby.xlsx'
    filepath = os.path.join(base_dir, filename)
    data = pd.read_excel(filepath)
    data_lakenames = data['LakenameNoDigits']
    data_lakename_withoutdigit = list(map(get_alpha, data_lakenames))
    data['LakenameNoDigits'] = data_lakename_withoutdigit
    data_groupby = data.groupby(['LakenameNoDigits']).mean()
    print(data_groupby)
    outfilepath = os.path.join(base_dir, 'lakeDOC_groupby.xlsx')
    data_groupby.to_excel(outfilepath)
    # print(data_lakename_withoutdigit)
    return 

def is_point_in_lake():
    """
    判断按照湖泊名称分类的点是否在湖泊内
    """
    #base_dir = r'I:\Qinghai_Tibet_Plateau\LakeDOC\Data'
    #lake_filename    = r'lakesShapefiles_dissolve/lakesShapefiles_dissolve.shp'
    #lakeDOC_filename = r'LakeCAR/LakeCAR_V2Matched.shp'
    
    base_dir = r'D:/Easy/my_code/Mark_XII_CSTest'
    lake_filename    = r'Data/lakeWithEnvs.shp'#湖泊
    lakeDOC_filename = r'Data/soil.shp'#样点
    lake_filepath    = os.path.join(base_dir, lake_filename)
    lakeDOC_filepath = os.path.join(base_dir, lakeDOC_filename)
    
    lake_data    = gpd.read_file(lake_filepath)
    lakeDOC_data = gpd.read_file(lakeDOC_filepath)
    lakeDOC_reproj = lakeDOC_data.to_crs(lake_data.crs)
    
    # print(lake_data)
    # print(lakeDOC_data)
    
    for pt in lakeDOC_reproj.iterrows():
        
        flag = lake_data.contains(pt[1].geometry)
        # print("Is point {} in:{}".format(pt[0], flag.any()))
           
        if not flag.any():
            print(pt[0], flag.any())
    return

def join_attribute_to_pt():
    """
    将湖泊的ID添加到采样点的属性中去
    """
    base_dir = r'D:/Easy/my_code/Mark_XII_CSTest'
    lake_filename    = r'Data/lakeWithEnvs.shp'#湖泊
    lakeDOC_filename = r'Data/soil.shp'#样点
    lake_filepath    = os.path.join(base_dir, lake_filename)
    lakeDOC_filepath = os.path.join(base_dir, lakeDOC_filename)
    
    lake_data    = gpd.read_file(lake_filepath)
    lakeDOC_data = gpd.read_file(lakeDOC_filepath)
    # lakeDOC_reproj = lakeDOC_data.to_crs(lake_data.crs)

    lake_with_envs = gpd.sjoin(lakeDOC_data, lake_data, how='left', op='within')
    print(lake_with_envs)
    outfilepath = r'D:/Easy/my_code/Mark_XII_CSTest/Data/SiteWithEnvs.shp'
    lake_with_envs.to_file(outfilepath, encoding='utf-8')
    return

if __name__ == "__main__":
    join_attribute_to_pt()
