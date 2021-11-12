"""
Create on 20210710

Author = Alber Fang
"""

import  pandas as pd
import numpy as np

type_list = ['snow', 'ice', 'snow_pit', 'ice_core', 'runoff']
def group_data():
    """
    整理计算各个冰川的数据，得到冰川的平均值
    """
    fp = r'Data\surface_snow_ice_20211103.xlsx'
    df = pd.read_excel(fp)
    # df.replace(['n.a.', '待测'], np.nan, inplace=True)
    # df.to_excel(r'I:\Data\DOC\Bin\test.xlsx')
    df.dropna(axis=1, how='all', inplace=True)
    df.drop(columns=['UnifiedID','GlacierID', 'SampleIDGeneral', 'SampleID', 'SampleIDUnified', 'SamplingTime', 
                     'SamplingPerson', 'Note', 'Latitude', 'Longitude', 'Elevation(m)', 'Source', 'Ref'],
            inplace=True)
    df_columns = df.columns
    df_mean_list = []
    df = df[df['Type'].isin(type_list)]
    for typename in type_list:
        df_type = df[df['Type']==typename]
        df_grouped = df_type.groupby(by='GlacierEn',)
        # grouped_count = df_grouped.mean()
        for a_grouped in df_grouped:
            a_grouped_values = a_grouped[1].values
            a_grouped_values_valid  = a_grouped_values[:, 3:]
            a_grouped_values_describe = a_grouped_values[0, :3]
            # a_grouped_values_valid = np.where(a_grouped_values_valid, a_grouped_values_valid, np.nan)
            a_grouped_mean = np.nanmean(a_grouped_values_valid, dtype=np.float64, axis=0)
            # print(np.concatenate([a_grouped_values_describe, a_grouped_mean], axis=0))
            df_mean_list.append(np.concatenate([a_grouped_values_describe, a_grouped_mean], axis=0)[np.newaxis, :])
    # print(df_mean_list)
    df_mean = np.concatenate(df_mean_list, axis=0)
    df_mean = pd.DataFrame(df_mean, columns=df_columns)
    print(df_mean)
    df_mean.to_excel(r'Result\surface_ice_snow_mean_1112.xlsx')
    return


if __name__ == '__main__':
    group_data()