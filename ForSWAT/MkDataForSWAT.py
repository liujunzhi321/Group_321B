# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 22:04:26 2021

@author: Albert
"""
import geopandas as gpd
import rioxarray as rioxr
import rasterio
import xarray as xr
import pandas as pd 
import numpy as np
import os
import re

def mk_tmp_data():
    """
    制作气温数据，需含最低最低最高气温与其他类型的数据并不相同
    """
    mask_filepath   = r'I:/Qinghai_Tibet_Plateau/swat_data/project_Changjiangyuan/studyArea/MaskForITPCAS/MaskForITPCAS.nc'
    tmax_folderpath = r"I:\foring_data_of_China_1979-2018\Tmp_min_max\Tmp_max"
    tmin_folderpath = r'I:\foring_data_of_China_1979-2018\Tmp_min_max\Tmp_min'
    outfolder_txt   = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\tmp_min_max'
    
    mask = xr.open_dataarray(mask_filepath)
    tmax_filename_list = os.listdir(tmax_folderpath)
    tmin_filename_list = os.listdir(tmin_folderpath)
    rows, cols= np.asarray(mask).shape
    for index, tmax_filename in enumerate(tmax_filename_list):
        tmin_filename = tmin_filename_list[index]
        print(tmax_filename, tmin_filename)
        tmax_filepath = os.path.join(tmax_folderpath, tmax_filename)
        tmin_filepath = os.path.join(tmin_folderpath, tmin_filename)
        tmax_data = np.asarray(xr.open_dataarray(tmax_filepath))
        tmin_data = np.asarray(xr.open_dataarray(tmin_filepath))
        no = 1
        for ii in range(rows):
            for jj in range(cols):
                if not np.isnan(mask[ii, jj]):
                    file_pathname = os.path.join(outfolder_txt, 'tmpTX{}.txt'.format(no))
                    _tmax_data = tmax_data[:,ii,jj] - 273.15 
                    _tmin_data = tmin_data[:,ii,jj] - 273.15
                    with open(file_pathname, 'a') as f:
                        np.savetxt(f, 
                                   np.hstack([_tmax_data[:, np.newaxis],
                                              _tmin_data[:, np.newaxis]]),
                                   fmt='%.3f',
                                   delimiter=',')
                    no += 1
                    print("NO.{}".format(no)) 
        print(no)
        
    return

def get_file_list(meteo):
    folderpath = r"I:\foring_data_of_China_1979-2018\Data_forcing_01dy_010deg"
    all_file_list = os.listdir(folderpath)
    the_file_list = []
    # print(len(all_file_list))
    for filename in all_file_list:
        if os.path.splitext(filename)[1] == '.nc':
            if filename.split('_')[0] == meteo:
                the_file_list.append(filename)
    return the_file_list

def switch_humidity(humidity):
    return humidity * 100.

def switch_sr(sr):
    return sr * 24 * 3600 / 1.0e6

def switch_prec(prec):
    return prec * 24

def mk_file_common(meteo):
    mask_filepath = r'I:/Qinghai_Tibet_Plateau/swat_data/project_Changjiangyuan/studyArea/MaskForITPCAS/MaskForITPCAS.nc'
    # raster_path = r'I:\foring_data_of_China_1979-2018\Data_forcing_01dy_010deg\prec_ITPCAS-CMFD_V0106_B-01_01dy_010deg_198001-198012.nc'
    raster_folderpath = r"I:\foring_data_of_China_1979-2018\Data_forcing_01dy_010deg"
    outfolder_txt = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\{}'.format(meteo)
    mask = xr.open_dataarray(mask_filepath)
    # meteo_data = np.asarray(xr.open_dataarray(raster_path))
    meteo_file_list = get_file_list(meteo)
    rows, cols= np.asarray(mask).shape
    for index, meteo_file in enumerate(meteo_file_list):
        print(meteo_file)
        meteo_filepath = os.path.join(raster_folderpath, meteo_file)
        meteo_data = np.asarray(xr.open_dataarray(meteo_filepath))
        no = 1
        for ii in range(rows):
            for jj in range(cols):
                if not np.isnan(mask[ii, jj]):
                    file_pathname = os.path.join(outfolder_txt, '{}TX{}.txt'.format(meteo, no))
                    with open(file_pathname, 'a') as f:
                        if meteo == 'prec':
                            print('prec')
                            np.savetxt(f, switch_prec(meteo_data[:, ii, jj]), fmt='%.3f')
                        elif meteo == 'shum':
                            print('shum')
                            np.savetxt(f, switch_humidity(meteo_data[:, ii, jj]), fmt='%.3f')
                        elif meteo == 'srad':
                            print('srad')
                            np.savetxt(f, switch_sr(meteo_data[:, ii, jj]), fmt='%.3f')
                        elif meteo == 'wind':
                            print('wind')
                            np.savetxt(f, meteo_data[:, ii, jj], fmt='%.3f')
                        elif meteo == 'pres':
                            print('pres')
                            np.savetxt(f, meteo_data[:, ii, jj], fmt='%.3f')
                        elif meteo == 'temp':
                            print('pres')
                            np.savetxt(f, meteo_data[:, ii, jj]-273.15, fmt='%.3f')
                    no += 1
                    print("NO.{}".format(no))
        print(no)

def cal_rh():
    """
    根据现有的气温，汽压和比湿计算相对湿度
    """
    temp_dir = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\temp'
    pres_dir = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\pres'
    shum_dir = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\shum'
    rh_dir   = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\rh'
    
    temp_namelist = os.listdir(temp_dir)
    pres_namelist = os.listdir(pres_dir)
    shum_namelist = os.listdir(shum_dir)
    for index, temp_filename in enumerate(temp_namelist):
        print(temp_filename, pres_namelist[index], shum_namelist[index])
        temp_data = pd.read_csv(os.path.join(temp_dir, temp_filename), header=None)
        pres_data = pd.read_csv(os.path.join(pres_dir, pres_namelist[index]), header=None)
        shum_data = pd.read_csv(os.path.join(shum_dir, shum_namelist[index]), header=None)*1e-2
        
        es = 6.112 * np.exp((17.67*temp_data) / (temp_data+243.5))
        pres_mb = pres_data * 1e-2
        e = (shum_data * pres_mb) / (0.378*shum_data+0.622)
        
        rh = e / es
        rh[0][rh[0] > 1] = 1 # 若相对湿度大于100%, 则置为100%
        rh = rh * 100
        import re
        number = ''.join(re.findall(r'\d', temp_filename))
        rh_filename = 'rhTX{}.txt'.format(number)
        print(rh_filename)
        rh.to_csv(os.path.join(rh_dir, rh_filename), index=None, header=None, float_format="%.3f")
    return

def insert_head(folderpath):
    
    filename_list = os.listdir(folderpath)
    # filename_list.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
    # print(filename_list)
    for filename in filename_list:
        filepath = os.path.join(folderpath, filename)
        print(filepath)
        with open(filepath, 'r+') as f:
            content = f.read()        
            f.seek(0, 0)
            f.write('19790101\n'+content)
    return

def extract_elevation_func(coords=[(95, 35)]):
    """
    根据经纬度从DEM数据中提取高程
    """
    ele_list = []
    for coord in coords:
        lon, lat = coord
        cjy_dem_filepath = r'I:/Qinghai_Tibet_Plateau/swat_data/project_Changjiangyuan/studyArea/CJY-DEM.tif'
        cjy_dem = rioxr.open_rasterio(cjy_dem_filepath)
        geoTF = cjy_dem.spatial_ref.GeoTransform
        geoTF = geoTF.split(' ')
        geoTF = [float(par) for par in geoTF]
        x_start, x_res, _, y_start, __, y_res = geoTF
        j = int((lon - x_start) / x_res)
        i = int((lat - y_start) / y_res)
        # print("行列号：", i, j)
        # print(cjy_dem)
        ele_list.append(cjy_dem[0, i, j].values)
    return ele_list
        
def extract_elevation():
    """
    提取范围内各个栅格的数据的高程值
    """
    mask_filepath    = r'I:/Qinghai_Tibet_Plateau/swat_data/project_Changjiangyuan/studyArea/MaskForITPCAS/MaskForITPCAS.nc'
    mask = xr.open_dataarray(mask_filepath)
    rows, cols= np.asarray(mask).shape
    coords = []
    for ii in range(rows):
        for jj in range(cols):
            if not np.isnan(mask[ii, jj]):
               coords.append([mask[ii, jj].lon.values, mask[ii, jj].lat.values])
               print(ii, jj)
        # if len(coords) > 10:
        #     break
    ele_list = extract_elevation_func(coords)
    coords = np.asarray(coords)
    df = pd.DataFrame()
    df['ID']        = range(1, len(ele_list)+1)
    df['NAME']      = ['<name>']*len(ele_list)
    df['LONG']      = np.around(coords[:, 0], decimals=3)
    df['LAT']       = np.around(coords[:, 1], decimals=3)
    df['ELEVATION'] = np.around(ele_list, decimals=3)
    
    output_filepath = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\auxiliary\fork_template.txt'
    df.to_csv(output_filepath, index=None)
    
    return

def mk_fork(meteo):
    fork_template_filepath = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\auxiliary\fork_template.txt'
    # meteo_folderpath = r'I:\Qinghai_Tibet_Plateau\forcing_data\{}'.format(meteo)
    meteo_folderpath = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\{}'.format(meteo)
    #out_filepath = r'I:\Qinghai_Tibet_Plateau\forcing_data\{}fork.txt'.format(meteo)
    out_filepath = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\{}fork.txt'.format(meteo)
    
    df = pd.read_csv(fork_template_filepath)
    filename_list = os.listdir(meteo_folderpath)
    # filename_digit_list = [re.findall('\d+', s)[0] for s in filename_list]
    filename_list.sort(key=lambda i: int(re.findall('\d+', i)[0])) #按字符串中的数字排序
    filename_list = [os.path.splitext(filename)[0] for filename in filename_list]
    df['NAME'] = filename_list
    
    df.to_csv(out_filepath, index=False)
    
    
if __name__ == '__main__':
    # mk_tmp_data()
    # meteos = ['temp']# ['prec', 'shum', 'srad', 'wind', 'pres'] #'shum', 
    # for meteo in meteos:
    #     mk_file_common(meteo)
    # cal_rh()
    # dir_templat = r'I:\Qinghai_Tibet_Plateau\swat_data\project_Changjiangyuan\meteos\{}'
    meteos = ['tmp_min_max', 'prec', 'rh', 'srad', 'wind']
    for meteo in meteos:
        # insert_head(dir_templat.format(meteo))
        mk_fork(meteo) 
    # extract_elevation()
    # extract_elevation()
