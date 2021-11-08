"""
Created on 2021-09-12

Author = Albert Fang
"""
from functools import cmp_to_key
from re import escape
from pandas.io.stata import stata_epoch
from rasterstats import zonal_stats
import geopandas as gpd
import pandas as pd
from six import reraise
import xarray as xr
import rioxarray as rioxr
import numpy as np
import platform
from control_file import (CMAP_DICT, EXTENT_VEC_DICT, STAT_CONTROL_DICT)

class WatershedStatsZonal():
    def __init__(self, arg_dict) -> None:
        self.key_word = 'lakeid'
        self.rst_fp = arg_dict['rst_fp']
        self.categorical = arg_dict['categorical']
        if self.categorical:
            self.stated_type_list = arg_dict['stated_type_list']
            self.cmap = CMAP_DICT[arg_dict['cmap']]
        else:
            # 列表
            c, w = arg_dict['c_stat_ways'], arg_dict['w_stat_ways']
            if pd.isna(c):
                self.c_stat_ways = []
            else:
                if isinstance(c, list):
                    self.c_stat_ways = c
                elif isinstance(c, str):
                    self.c_stat_ways = c.split(',')
                else:
                    raise TypeError("'c_stat_ways'须是'list'或'str'")
            
            if pd.isna(w):
                self.w_stat_ways = []
            else:
                if isinstance(w, list):
                    self.w_stat_ways = w
                elif isinstance(c, str):
                    self.w_stat_ways = w.split(',')
                else:
                    raise TypeError("'c_stat_ways'须是'list'或'str'")

        # self.catchment_vec_fp = r'J:\Data\shapefile\catchment\catchment.shp'
        # self.watershed_vec_fp = r'J:\Data\shapefile\watershed\watershed.shp'
        # 将矢量的数据投影坐标系转化为与栅格相同的投影
        if platform.system() == "Windows":
            self.temp_vec_fp = r'I:\Data\Temp\ProjSameWithRaster.shp'
        elif platform.system() == 'Linux':
            self.temp_vec_fp = r'/share/home/liujunzhi/liujunzhi/Albert/Data/tempData/ProjSameWithRaster.shp'


    def transform(self, vec_fp):
        """
        将矢量数据的坐标系转化为和栅格数据相同的坐标系统。
        params:
            vec_fp: 矢量数据的存储路径
            rst_fp: 栅格数据的存储路径
            tmp_vec_fp: 坐标系统转换过后的矢量数据的存储路径
        """
        vec = gpd.read_file(vec_fp)
        rst = rioxr.open_rasterio(self.rst_fp)
        rst_crs = rst.rio.crs
        vec = vec.to_crs(rst_crs)
        vec.to_file(self.temp_vec_fp)
        return

    
    def stat_multiattributes(self, vec_fp, attribute_name, stat_ways):
        """
        计算多个统计量
        """
        self.transform(vec_fp)        
        vec_data = gpd.read_file(self.temp_vec_fp)
        key_word_list = vec_data[self.key_word].values

        stat_result = zonal_stats(self.temp_vec_fp, self.rst_fp, stats=stat_ways, all_touched=True)
        
        stat_result_df = pd.DataFrame(stat_result)
        rename_dict = {stat_way: '{}_{}'.format(attribute_name, stat_way) for stat_way in stat_ways}
        stat_result_df.rename(columns=rename_dict, inplace=True)
        stat_result_df[self.key_word] = key_word_list
        # print(stat_result_df.set_index(self.key_word))
        return stat_result_df.set_index(self.key_word)

    
    def stat_percent(self, vec_fp, attribute_name):
        """
        计算土地利用数据中，各个类型的面积
        """
        self.transform(vec_fp) 
        vec_data = gpd.read_file(self.temp_vec_fp)
        key_word_list = vec_data[self.key_word].values
        if self.stated_type_list == 'All':
            type_list = [type_name for type_name in self.cmap.values()]
        else:
            type_list = self.stated_type_list.split(',')

        stat_result = zonal_stats(self.temp_vec_fp, self.rst_fp, categorical=True, all_touched=True, category_map=self.cmap)
        count_sum   = zonal_stats(self.temp_vec_fp, self.rst_fp, stats=['count', 'nodata'], all_touched=True, ) 

        stat_result_df = pd.DataFrame(stat_result, columns=type_list)
        count_sum_df   = pd.DataFrame(count_sum)
        stat_result_df = stat_result_df.div(np.array(count_sum_df.sum(axis=1)), axis=0).round(3)

        stat_result_df[self.key_word] = key_word_list
        rename_dict = {typename: '{}_{}'.format(attribute_name, typename) for typename in type_list}
        stat_result_df.rename(columns=rename_dict, inplace=True)
        # print(stat_result_df.set_index(self.key_word))
        return stat_result_df.set_index(self.key_word)

    def set_prefix(self, df, extent):
        if isinstance(df, pd.DataFrame):
            columns_list = df.columns
            if extent == 'catchment':
                rename_dict = {col_name: 'C_{}'.format(col_name) for col_name in columns_list}
            elif extent == 'watershed':
                rename_dict = {col_name: 'W_{}'.format(col_name) for col_name in columns_list}
            return df.rename(columns=rename_dict)
        else:
            return None


    def stat_main(self, attribute_name):
        c_vec_fp = EXTENT_VEC_DICT['catchment']
        w_vec_fp = EXTENT_VEC_DICT['watershed']
        if self.categorical:
            catchment_df = self.stat_percent(c_vec_fp, attribute_name)
            watershed_df = self.stat_percent(w_vec_fp, attribute_name)
            return pd.concat([self.set_prefix(catchment_df, 'catchment'), self.set_prefix(watershed_df, 'watershed')], axis=1)

        else:
            if len(self.c_stat_ways) >= 1:
                catchment_df = self.stat_multiattributes(c_vec_fp, attribute_name, self.c_stat_ways)
            else:
                catchment_df = None

            if len(self.w_stat_ways) >= 1:
                watershed_df = self.stat_multiattributes(w_vec_fp, attribute_name, self.w_stat_ways)
            else:
                watershed_df = None
            return pd.concat([self.set_prefix(catchment_df, 'catchment'), self.set_prefix(watershed_df, 'watershed')], axis=1)
        

if __name__ == '__main__':
    control_dict = STAT_CONTROL_DICT['HFP']
    wsz = WatershedStatsZonal(control_dict)
    df = wsz.stat_main('HFP')
    print(df)