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

def combine_data(): 
    """
    将现有的的DOC数据与之前提取的环境因子合并为同一个表格
    """
    base_dir        =  r'C:\Users\Administrator\Desktop'
    lake_doc_join   = r'soil\LakeCARWithLakeName.shp'
    env_filename    = r'WatershedEnvs/watershed_attribution.xlsx'
    
    doc_join_filepath = os.path.join(base_dir, lake_doc_join)
    env_filepath      = os.path.join(base_dir, env_filename)
    
    doc_join  = gpd.read_file(doc_join_filepath)
    env_data = pd.read_excel(env_filepath)
    lnames = doc_join['lakeJoin'].values
    env_data_join = env_data.loc[lnames] 
    env_data_join['lakeJoin'] = lnames
    
    data_join = pd.merge(doc_join, env_data_join, on='lakeJoin', how='left')
    
    outfilepath = os.path.join(base_dir, r'WatershedEnvs\CARJoin_20210315\CARJoin.xlsx')
    outfilepath_2 = os.path.join(base_dir, r'WatershedEnvs\CARJoin_20210315\CARJoin_2.xlsx')
    print(data_join)
    env_data_join.to_excel(outfilepath)
    doc_join.to_excel(outfilepath_2)
    return

def lakeshp_envs():
    """
    将环境变量写入湖泊的shapefile数据中
    """
    
    envs_fp = r'I:/Qinghai_Tibet_Plateau/LakeDOC/Data/WatershedEnvs/watershed_attributes.xlsx'
    lake_fp = r'I:/Qinghai_Tibet_Plateau/LakeDOC/Data/lakesShapefiles_dissolve/lakesShapefiles_dissolve.shp'
    output_fp = r'I:\Qinghai_Tibet_Plateau\LakeDOC\Data\lakesShapefiles_dissolve\lakeWithEnvs.shp'
    envs_data = pd.read_excel(envs_fp)
    lake_data = gpd.read_file(lake_fp)
    lake_data = pd.concat([lake_data, envs_data], axis=1)
    print(envs_data)
    print(lake_data)
    lake_data.to_file(output_fp, encoding='utf-8')
    

if __name__ == "__main__":
    # mean_obs()
    # is_point_in_lake()
    # join_lakename_to_pt()
    # combine_data()
    join_attribute_to_pt()