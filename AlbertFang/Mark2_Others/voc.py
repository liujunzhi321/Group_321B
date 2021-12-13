from numpy import append, printoptions
import pandas as pd
import numpy as np

def voc():
    fp = r'Data\中科三清-【数据分析岗-南京】校招试题20211116.xlsx'
    df = pd.read_excel(fp, sheet_name='物质总和', header=[0,1])
    column_names = set(df.columns.droplevel(1))
    print(column_names)
    df_list = []
    df_column_L1 = []
    for column_name in column_names:
        df_column = df[column_name]
        df_column_L1.extend([column_name]*len(df_column.T))
        df_list.append(df_column)
    df_all = pd.concat(df_list, axis=1)
    df_column_L2 = df_all.columns
    new_df = pd.DataFrame(np.asarray(df_all), columns=[df_column_L1, df_column_L2])
    print(new_df)
    new_df.to_excel(r'Data\Grouped_data_1.xlsx')

def voc_1():
    fp = r'Data\Grouped_data_1.xlsx'
    df = pd.read_excel(fp, header=[0,1])
    date_time =pd.to_datetime(df['Time'], unit='s')
    df_with_time = pd.concat((date_time, df), axis=1)
    df_with_time.to_csv(r'Data\data_with_time.csv')


def voc_join():
    import datetime
    fp_1 = r'Data\data_with_time.xlsx'
    fp_2 = r'Data\中科三清-【数据分析岗-南京】校招试题20211116.xlsx'
    df_voc = pd.read_excel(fp_1, header=[0, 1])
    df_voc.columns = df_voc.columns.droplevel()
    df_meteo = pd.read_excel(fp_2, sheet_name='气象数据-大气预警站环境监测查询',)
    # time = [t.replace('/', '-')+':00' for t in df_voc['时间']]
    # df_voc['time_id'] = time
    print(df_voc['时间'].dt.floor('H'))
    df_voc['时间_1'] = df_voc['时间'].dt.floor('H')
    df_meteo['时间_1'] =  pd.to_datetime(df_meteo['时间'])
    print(df_meteo['时间_1'])
    df_merged = pd.merge(df_voc, df_meteo, left_on='时间_1', right_on='时间_1', how='left')
    print(df_merged)

    df_merged.to_excel(r'Data\data_with_meteos.xlsx')


def analysis():
    fp = r'Data\data_with_meteos.xlsx'
    df = pd.read_excel(fp, header=[0, 1])
    df_selected = df[['时间', 'Meteos']]
    print(df_selected)

if __name__ == '__main__':
    analysis()