# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:10:59 2021

@author: Albert
"""
import os 

def genrate_downloadlist(left, right, bottom, top):
    """
    这段代码会生成所需土地利用数据的下载链接。
    先确定所要提取土地利用比例的点簇的范围。
    """
    template = r'http://data.ess.tsinghua.edu.cn/data/fromglc10_2017v01/fromglc10v01_{}_{}.tif'

    exist_files = os.listdir(r'J:\Data\TP\land_cover\tiles')
    filepath = r'J:\Data\TP\land_cover\downloadList.txt'
    with open(filepath, 'w') as fobj:
        for lon in range(left, right, 2):
            for lat in range(bottom, top, 2):
                filename = 'fromglc10v01_{}_{}.tif'.format(lat, lon)
                if filename not in exist_files:
                    fobj.writelines(template.format(lat, lon) + '\n')
    return


if __name__ == '__main__':
    genrate_downloadlist(68, 106, 24, 42)