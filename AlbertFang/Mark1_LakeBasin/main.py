"""
Created on 2021-09-12

Author = ALbert Fang
"""
import pandas as pd

from watershed_stats_zonal import WatershedStatsZonal
from control_file import (STAT_CONTROL_DICT, OUTPUT_FP)
import control_file as cf
from  pprint import pprint

attribute_list = []
STAT_CONTROL_DICT = cf.mk_control_dict()
for attribute_name, control_dict in STAT_CONTROL_DICT.items():
    print('*'*10 + "Calculating {} ...".format(attribute_name) + '*'*10 )
    wshd_stat = WatershedStatsZonal(control_dict)
    attribute_list.append(wshd_stat.stat_main(attribute_name))
df_all = pd.concat(attribute_list, axis=1)
print(df_all)

df_all.to_excel(OUTPUT_FP)