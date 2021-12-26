"""
Created on 2021-12-26

Author = Albert Fang
"""


import multiprocessing as mp
import pandas as pd

from watershed_stats_zonal import WatershedStatsZonal
from control_file import (STAT_CONTROL_DICT, OUTPUT_FP)
import control_file as cf
import time
from pprint import pprint


def execute_sigal_duty(args):
    attribute_name, control_dict = args
    print('*'*10 + "Calculating {} ...".format(attribute_name) + '*'*10 )
    wshd_stat = WatershedStatsZonal(control_dict)
    return wshd_stat.stat_main(attribute_name)


def multicores_duties():
    STAT_CONTROL_DICT = cf.mk_control_dict()
    STAT_CONTROL_LIST = list(STAT_CONTROL_DICT.items())
    pool = mp.Pool(processes=12)
    res = pool.map(execute_sigal_duty, STAT_CONTROL_LIST)
    df_all = pd.concat(res, axis=1)
    print(df_all)

    df_all.to_excel(OUTPUT_FP)

    
if __name__ == "__main__":    
    start_time = time.time()
    
    multicores_duties()
    
    end_time = time.time()
    
    print(end_time - start_time)


