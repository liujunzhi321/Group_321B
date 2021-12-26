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
import os
from control_file import (CMAP_DICT, EXTENT_VEC_DICT, STAT_CONTROL_DICT)

class WatershedStatsZonal():
    def __init__(self, arg_dict) -> None:
        self.key_word = 'LakeID'
        self.rst_fp = arg_dict['rst_fp']
        self.categorical = arg_dict['categorical']
        if self.categorical:
            self.stated_type_list = arg_dict['stated_type_list']
            self.cmap = CMAP_DICT[arg_dict['cmap']]
        else:
            # 列表
            self.c_stat_ways, self.w_stat_ways, self.l_stat_ways = arg_dict['c_stat_ways'], arg_dict['w_stat_ways'], arg_dict['l_stat_ways']
            self.c_stat_ways = self.check_statways(self.c_stat_ways)
            self.w_stat_ways = self.check_statways(self.w_stat_ways)
            self.l_stat_ways = self.check_statways(self.l_stat_ways)


    def check_statways(self, stat_ways):
        if pd.isna(stat_ways):
            stat_ways = []
        else:
            if isinstance(stat_ways, list):
                stat_ways = stat_ways
            elif isinstance(stat_ways, str):
                stat_ways = stat_ways.split(',')
            else:
                print(stat_ways)
                raise TypeError("'c_stat_ways'须是'list'或'str'")
      
        return stat_ways

    
    def stat_multiattributes(self, vec_fp, attribute_name, stat_ways):
        """
        计算多个统计量
        """
        # if os.path.basename(self.target_rst_fp) not in os.listdir(self.temp_rst_fd):
        #     self.transform_albers_rst()

        vec_data = gpd.read_file(vec_fp)
        key_word_list = vec_data[self.key_word].values

        stat_result = zonal_stats(vec_fp, self.rst_fp, stats=stat_ways, all_touched=True)
        
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
        # if os.path.basename(self.target_rst_fp) not in os.listdir(self.temp_rst_fd):
        #     self.transform_albers_rst()

        vec_data = gpd.read_file(vec_fp)
        key_word_list = vec_data[self.key_word].values
        if self.stated_type_list == 'All':
            type_list = [type_name for type_name in self.cmap.values()]
        else:
            type_list = self.stated_type_list.split(',')

        stat_result = zonal_stats(vec_fp, self.rst_fp, categorical=True, all_touched=True, category_map=self.cmap)
        count_sum   = zonal_stats(vec_fp, self.rst_fp, stats=['count', 'nodata'], all_touched=True, ) 

        stat_result_df = pd.DataFrame(stat_result, columns=type_list)
        count_sum_df   = pd.DataFrame(count_sum)
        stat_result_df = stat_result_df.div(np.array(count_sum_df.sum(axis=1)), axis=0).round(3)

        stat_result_df[self.key_word] = key_word_list
        rename_dict = {typename: '{}_{}'.format(attribute_name, typename) for typename in type_list}
        stat_result_df.rename(columns=rename_dict, inplace=True)
        # print(stat_result_df.set_index(self.key_word))
        return stat_result_df.set_index(self.key_word)


    def set_prefix(self, df, extent):
        """
        为变量设置前缀
        """
        if isinstance(df, pd.DataFrame):
            columns_list = df.columns
            if extent == 'catchment':
                rename_dict = {col_name: 'IC_{}'.format(col_name) for col_name in columns_list}
            elif extent == 'watershed':
                rename_dict = {col_name: 'FC_{}'.format(col_name) for col_name in columns_list}
            elif extent == 'lake':
                rename_dict = {col_name: 'Lk_{}'.format(col_name) for col_name in columns_list}
            return df.rename(columns=rename_dict)
        else:
            return None


    def stat_main(self, attribute_name):
        c_vec_fp = EXTENT_VEC_DICT['catchment']
        w_vec_fp = EXTENT_VEC_DICT['watershed']
        l_vec_fp = EXTENT_VEC_DICT['lake']
        if self.categorical:
            catchment_df = self.stat_percent(c_vec_fp, attribute_name)
            watershed_df = self.stat_percent(w_vec_fp, attribute_name)
            return pd.concat([self.set_prefix(catchment_df, 'catchment'), self.set_prefix(watershed_df, 'watershed')], axis=1)

        else:
            # IC
            if len(self.c_stat_ways) >= 1:
                catchment_df = self.stat_multiattributes(c_vec_fp, attribute_name, self.c_stat_ways)
            else:
                catchment_df = None

            # FC
            if len(self.w_stat_ways) >= 1:
                watershed_df = self.stat_multiattributes(w_vec_fp, attribute_name, self.w_stat_ways)
            else:
                watershed_df = None

            #Lake
            if len(self.l_stat_ways) >= 1:
                lake_df = self.stat_multiattributes(l_vec_fp, attribute_name, self.l_stat_ways)
            else:
                lake_df = None

            return pd.concat([self.set_prefix(catchment_df, 'catchment'), self.set_prefix(watershed_df, 'watershed'), self.set_prefix(lake_df, 'lake')], axis=1)
        

if __name__ == '__main__':
    control_dict = STAT_CONTROL_DICT['HFP']
    wsz = WatershedStatsZonal(control_dict)
    df = wsz.stat_main('HFP')
    print(df)