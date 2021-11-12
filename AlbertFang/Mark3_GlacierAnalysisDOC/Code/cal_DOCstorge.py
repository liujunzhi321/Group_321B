
import geopandas as gpd
import numpy as np
import pandas as pd
from pygeos.constructive import centroid
import xarray as xr
import os 

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

# workplace = r'I:\Qinghai_Tibet_Plateau\GlcAnysis'
doc_fp = r'I:\Data\DOC\Shapefile\GlcDOCMean\GlcDOCMean.shp'
tn_fp  = r'I:\Data\DOC\Shapefile\GlcTNMean\GlcYNMean.shp'

doc_csv_fp = r'I:\Data\DOC\Data\All_type_doc_mean_without-nodata.csv'
tn_csv_fp  = r'I:\Data\DOC\Data\All_type_tn_mean_without-nodata.csv'

obs_dict ={
    'DOC' : 'DOC(mg/L)',
    'TN'  : 'TN(mg/L)'
}


def mk_shapefile(fp, obs_varname):
    from shapely import geometry
    df = pd.read_excel(fp)
    df.dropna(axis=0, subset=[obs_dict[obs_varname]], inplace=True)
    lats, lons = df.Lat, df.Lon
    points = zip(lons, lats)
    geo_points = [geometry.Point(pt) for pt in points]
    gdf = gpd.GeoDataFrame(df,
                            geometry=geo_points, crs='EPSG:4326')
    # gdf.to_file(r'I:\Data\DOC\Shapefile\GlcDOCMean_withoutNodata\GlcDOCMean_withoutNodata.shp', encoding='utf-8')
    return gdf





def mark_region():
    """
    标记冰川的类型，即按照冰川中心点的坐标来确定，大于32°为Westly, 小于32°N为Monsoon
    """
    glc_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile/GlacialDBATP/GlacialDBTPInfo.shp'
    glc_df = gpd.read_file(glc_fp).to_crs('EPSG:4326')
    regions = ['Westly' if per_glc.centroid.y>32 else 'Monsoon' for per_glc in glc_df.geometry]
    glc_df['Region'] = regions
    regions_list = ['Westly', 'Monsoon']

    total_area = np.sum(glc_df['Glc_Area'])
    print('Toal area: {}'.format(total_area))
    for region in regions_list:
        print(region)
        region_glc_data = glc_df[glc_df.Region==region]
        # glc_vol_A = np.sum(region_glc_data['Glc_Vol_A'])
        # glc_vol_B = np.sum(region_glc_data['Glc_Vol_B'])
        # print("\tA: {}".format(glc_vol_A))
        # print("\tB: {}".format(glc_vol_B))
        region_area = np.sum(region_glc_data['Glc_Area'])
        print('\t: {}'.format(region_area))
    return glc_df
 

def get_colsest_ptDOC(doc_glc_data, obs_varname='DOC'):
    """
    计算每个冰川条目距离 有DOC观测值的最近站点。
    根据采样点的类型，将推测每个冰川的冰和雪DOC含量的方法各分为三种：
    ice:
        - 只利用ice;
        - 利用ice_core + ice
        - 只利用ice_core
    snow:
        - 只利用snow;
        - 利用snow + snow_pit
        - 只利用snow_pit
    """
    # doc_glc_rfp      = r'SiteData/GlcPtDOC/GlcPtDOC_20210203/GlcPtDOC/GlcPtDOC.shp'
    # doc_glc_filepath = os.path.join(workplace, doc_glc_rfp)
    # glc_rfp          = r'I:/Qinghai_Tibet_Plateau/doc_ice/glacia_doc_info_v1.shp' # r'Shapefile/GlacialDBATP/GlacialDBTPInfo.shp'
    glc_fp       = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile/GlacialDBATP/GlacialDBTPInfo.shp'
    # glc_fp = r'I:\Data\DOC\Shapefile\GlcMean\GlcMean.shp'

    # doc_glc_data = gpd.read_file(sample_fp, encoding='utf-8')
    glc_data     = gpd.read_file(glc_fp, encoding='utf-8')
    
    doc_type_list = {"core"     : ['ice_core'],
                     'ice'      : ['ice'],
                     'core_U_ice' : ['ice','ice_core'],
                     'snow'     : ['snow'],
                     'pit'      : ['snow_pit'],
                     'snow_U_pit' : ['snow', 'snow_pit']}
    for doc_type in doc_type_list.keys():   
        doc_type_data = doc_glc_data[doc_glc_data['Type'].isin(doc_type_list[doc_type])]
        # 将DOC采样点数据的坐标系与冰川数据的坐标系置为相同
        doc_type_data = doc_type_data.to_crs(glc_data.crs)
        
        # 计算冰川中心点到就近DOC站点的距离
        glacia_centers  = np.asarray([glc_data.centroid.x, glc_data.centroid.y]).T
        doc_ice_centers = np.asarray([doc_type_data.centroid.x, doc_type_data.centroid.y]).T
        doc_point_num = doc_ice_centers.shape[0]
        # a_tile = np.tile(a[np.newaxis, :,:], (2, 1, 1))
        dis_matrix = np.linalg.norm(np.tile(glacia_centers[np.newaxis, :, :], (doc_point_num, 1, 1)) 
                                    - doc_ice_centers[:, np.newaxis, :], axis=2)
        
        # 得到最近站点的编号
        no_list = np.argmin(dis_matrix, axis=0)
        
        # 赋值
        obs_varname_in_table = obs_dict[obs_varname]
        glc_data['{}Idx'.format(doc_type)] = no_list
        doc_list = [doc_type_data.iloc[no][obs_varname_in_table]  for no in no_list]
        # type_list = [doc_glc_data.iloc[no].type  for no in no_list]
        glc_data['{}_{}'.format(doc_type, obs_varname)] = doc_list
        # glc_data['doc_type'] = type_list
        tdocA = np.sum(glc_data['Glc_Vol_A'] * glc_data['{}_{}'.format(doc_type, obs_varname)] * 0.9)
        tdocB = np.sum(glc_data['Glc_Vol_B'] * glc_data['{}_{}'.format(doc_type, obs_varname)] * 0.9) # 单位Gg
        # print("T{}_A_{}: {}".format(obs_varname, doc_type, tdocA))
        # print("T{}_B_{}: {}".format(obs_varname, doc_type, tdocB))

        # 标记冰川的南北
        glc_df_proj = glc_data.to_crs('EPSG:4326')
        regions = ['Westly' if per_glc.centroid.y>32 else 'Monsoon' for per_glc in glc_df_proj.geometry]
        glc_data['Region'] = regions
        regions_list = ['Westly', 'Monsoon']
        for region in regions_list:
            print(region)
            region_glc_data = glc_data[glc_data.Region==region]
            tdocA = np.sum(region_glc_data['Glc_Vol_A'] * region_glc_data['{}_{}'.format(doc_type, obs_varname)] * 0.9)
            tdocB = np.sum(region_glc_data['Glc_Vol_B'] * region_glc_data['{}_{}'.format(doc_type, obs_varname)] * 0.9) # 单位Gg
            print("\t{}-T{}_A_{}: {}".format(region, obs_varname, doc_type, tdocA))
            print("\t{}-T{}_B_{}: {}".format(region, obs_varname, doc_type, tdocB))


        """
        TDOCAcore: 1941.65674127955
        TDOCBcore: 1792.37775551688
        
        TDOCAice: 3930.9849408038403
        TDOCBice: 3630.7824485580004
        
        TDOCAcoreUice: 2412.72684214254
        TDOCBcoreUice: 2261.25694984959
        """
        # TN
        """
        TDOCAcore: 484.8474934682798
        TDOCBcore: 454.952950409988

        TDOCAice: 522.8816951175714
        TDOCBice: 485.35151194694424
        
        TDOCAcoreUice: 502.3920969426857
        TDOCBcoreUice: 469.0683503485709
        """
        # Upadate 20210808
        ## TN
        """
        TTN_A_core:512.5714930638001
        TTN_B_core:482.73508198260004
        TTN_A_ice:881.0314930940607
        TTN_B_ice:810.1983592529991

        TTN_A_core_U_ice:580.305312557892
        TTN_B_core_U_ice:547.5162283631292
        TTN_A_snow:958.033961798804
        TTN_B_snow:899.9935791973151
        TTN_A_pit:578.4539897933364
        TTN_B_pit:539.168831139443
        TTN_A_snow_U_pit:901.3557193413169
        TTN_B_snow_U_pit:846.2971617552487
        """
        ## DOC
        """
        TDOC_A_core: 1994.8794020451
        TDOC_B_core: 1849.7655433106997
        TDOC_A_ice: 2728.848577286717
        TDOC_B_ice: 2532.1879201622382
        TDOC_A_core_U_ice: 2215.7249073949115
        TDOC_B_core_U_ice: 2070.3388658485355
        TDOC_A_snow: 2186.6744670685825
        TDOC_B_snow: 2082.609637769513
        TDOC_A_pit: 2932.4254226044536
        TDOC_B_pit: 2713.8263693472713
        TDOC_A_snow_U_pit: 2210.6991800845944
        TDOC_B_snow_U_pit: 2096.205501457316
        """
        ## update 20210822
        ## DOC (Gg)
        """
        TDOC_A_core: 1994.8794020451
        TDOC_B_core: 1849.7655433106997
        TDOC_A_ice: 2892.8062186232155
        TDOC_B_ice: 2698.739731776052
        """
        ## TN (Gg)
        """
        TN_A_core: 512.5714930638001
        TTN_B_core: 482.73508198260004
        TTN_A_ice: 892.6007515924746
        TTN_B_ice: 822.3930712656801
        """
        # 202-08-23
        """
        Westly
                Westly-TTN_A_core: 355.5860317506
                Westly-TTN_B_core: 331.76776259250005
        Monsoon
                Monsoon-TTN_A_core: 156.98546131320003
                Monsoon-TTN_B_core: 150.96731939010002

        Westly
                Westly-TTN_A_ice: 734.9482462455541
                Westly-TTN_B_ice: 669.1105574838916
        Monsoon
                Monsoon-TTN_A_ice: 157.65250534692044
                Monsoon-TTN_B_ice: 153.28251378178845

        Westly(Gg)
                Westly-TDOC_A_core: 1131.9127108866
                Westly-TDOC_B_core: 1032.8732896995
        Monsoon
                Monsoon-TDOC_A_core: 862.9666911585
                Monsoon-TDOC_B_core: 816.8922536112
        Westly
                Westly-TDOC_A_ice: 2064.041806751522
                Westly-TDOC_B_ice: 1894.7906589360828
        Monsoon
                Monsoon-TDOC_A_ice: 828.7644118716938
                Monsoon-TDOC_B_ice: 803.9490728399692
        """
        # 2021-11-13
        """
        Westly
            Westly-TTN_A_core: 355.5860317506
            Westly-TTN_B_core: 331.76776259250005
        Monsoon
            Monsoon-TTN_A_core: 156.98546131320003
            Monsoon-TTN_B_core: 150.96731939010002
        Westly
            Westly-TTN_A_ice: 741.860497863448
            Westly-TTN_B_ice: 677.8029192779969
        Monsoon
            Monsoon-TTN_A_ice: 157.65250537056008
            Monsoon-TTN_B_ice: 153.2825138096339
            
        Westly
                Westly-TDOC_A_core: 1131.9127108866
                Westly-TDOC_B_core: 1032.8732896995
        Monsoon
                Monsoon-TDOC_A_core: 862.9666911585
                Monsoon-TDOC_B_core: 816.8922536112
        Westly
                Westly-TDOC_A_ice: 2062.0539417856517
                Westly-TDOC_B_ice: 1891.6003171118691
        Monsoon
                Monsoon-TDOC_A_ice: 828.7644118791891
                Monsoon-TDOC_B_ice: 803.949072849644

        """
    output_rfp = r'Shapefile\GlcWithInfo_20210327\GlcInfo_v2.1.shp'
    # output_fp  = os.path.join(workplace, output_rfp)
    # glc_data.to_file(output_fp, encoding='utf-8')
    
    return

if __name__ == '__main__':
    fp = r'D:\Easy\my_code\Group_321B\AlbertFang\Mark3_GlacierAnalysisDOC\Mean\All_type_data_mean.xlsx'
    get_colsest_ptDOC(mk_shapefile(fp, 'DOC'), 'DOC')
    # gdf = mk_shapefile(doc_csv_fp, 'DOC')
    # mark_region()