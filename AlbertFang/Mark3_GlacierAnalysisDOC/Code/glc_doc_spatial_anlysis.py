"""
Create on 20210710

Revised on 20210813

Author = Alber Fang
"""
"""
完成一个目标：根据各个冰川的的属性来计算相关性，并作图，并整理相关性和可信度的表格
"""
import  pandas as pd
import numpy as np
from pandas.core.algorithms import factorize
import scipy.stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Global Variable
type_list = ['snow', 'ice', 'snow_pit', 'ice_core', 'runoff']
# regions
region_dict = {"S"      : 'South of 32°N',
               "N"      : 'North of 32°N',
               "Cross"  : 'Cross TBP' 
}
# observations
obs_varname_dict = {
    "DOC(mg/L)"     : 'DOC',
    'TN(mg/L)'      : 'TN'
}

# Functions
def scatter_plot(df, x_name, y_name, title, save_path):
    """
    绘制线性回归图
    Parameters:
    -------------------------------------------------
        df          : DataFrame, x和y组成的DataFrame;
        x_name      : str, x变量的名称；
        y_name      : str, y变量的名称；
        title       : str, 所绘图的标题；
        save_path   ：str, 所绘图的保存路径。
    Return:
    -------------------------------------------------
        None
    """
    import os
    sns.set_theme(color_codes=True)
    sns.set(rc={"figure.figsize":(6, 6)}) #width=3, #height=4
    g = sns.lmplot(data=df, x=x_name, y=y_name)
    plt.title(title)
    # plt.show()
    fd = os.path.dirname(save_path)
    if not os.path.exists(fd):
        os.makedirs(fd)
    g.savefig(fname = save_path,
              dpi = 300,
              bbox_inches='tight')
    return 

def significant_correlation(x, y, scatter_plot_flag, plot_save_path, **args):
    """
    计算两组数的相关性
    Params:
        x                   : list like, 自变量；
        y                   : list like, 因变量；
        scatter_plot_flag   : bool, 是否绘制变量之间的回归图；
        **args              : dict, 含自变量名称、因变量名称、点位所在区域、样点类型。
    Return:

    """
    mask = np.logical_not(x.isna() | y.isna())
    y, x = y[mask], x[mask]
    if len(x) < 3:
        print("样点数量不足（少于3个）！")
        return np.nan, np.nan

    pearson_r, p_value = scipy.stats.pearsonr(x, y)
    pearson_r, p_value = round(pearson_r, 3), round(p_value, 3)

    if p_value < 0.05:
        pearson_r = ''.join([str(pearson_r), '*'])
        if scatter_plot_flag:
            varname, smp_type, obs_varname, n32 = args['varname'], args['smp_type'], args['obs_varname'], args['n32']
            title = 'Scatter plot of {} and {}_{} @ {}\n $r = {}, p\_value = {}$'.format(varname, smp_type, obs_varname, 
                                                                                            region_dict[n32], pearson_r, p_value)
            # save_path = '{}_{}_{}_{}'.format(obs_varname_dict[args.obs_varname], args.varname, args.smp_type, args.n32)
            # save_path = save_path.replace('/', ' ')
            df = pd.concat([x, y], axis=1)
            scatter_plot(df, varname, obs_varname, title, plot_save_path)
    return pearson_r, p_value


def significant_correlation_std_main():
    factor = 'position'
    # Input parameters
    fp = r'Mean\All_type_data_mean_factors_20211112.xlsx'
    fp_output = r'Result\{}\与{}相关性_20211112.xlsx'.format(factor, factor)
    fd = os.path.dirname(fp_output)
    if not os.path.exists(fd):
        os.makedirs(fd)
    df = pd.read_excel(fp, header=[0, 1])
    df_selected = df[['Basic information', 'C_N', factor]]
    df_selected.columns = df_selected.columns.droplevel()

    df = df_selected

    colunm_list = df.columns.drop(['Glacier', 'GlacierEn', 'Type', 'N32', 'Regions'])
    obs_varname_list = ['DOC(mg/L)', 'TN(mg/L)',]
    smp_type_list = ['snow', 'ice', 'snow_pit', 'ice_core', 'runoff']
    n32_list = ['N', 'S', 'Cross']
    df_pearson_r_col_list, df_p_value_col_list = [], []
    for obs_varname in obs_varname_list:
        for smp_type in smp_type_list:
            for n32 in n32_list:
                if n32 != 'Cross':
                    df_ = df[(df['Type']==smp_type) & (df['N32']==n32)]
                else:
                    df_ = df[df['Type']==smp_type]
                pearson_r_list, p_value_list = [], []
                for varname in colunm_list:
                    if obs_varname == varname:
                        pearson_r, p_value = np.nan, np.nan
                        pearson_r_list.append(pearson_r)
                        p_value_list.append(p_value)
                        continue
                    x = df_[varname]
                    y = df_[obs_varname]
                    plot_save_fd = os.path.dirname(fp_output)
                    plot_save_path = os.path.join(plot_save_fd, 'Plot-{}-{}-{}-{}.png'.format(n32, smp_type, obs_varname, varname))
                    plot_save_path = plot_save_path.replace('/', ' ')
                    args = {
                        'varname'      : varname,
                        'obs_varname'  : obs_varname,
                        'n32'          : n32,
                        'smp_type'     : smp_type
                    }
                    # print(plot_save_path)
                    pearson_r, p_value = significant_correlation(x, y, scatter_plot_flag=True, plot_save_path=plot_save_path, **args)
                    pearson_r_list.append(pearson_r)
                    p_value_list.append(p_value)
                df_pearson_r_col = pd.DataFrame(np.array(pearson_r_list).T, columns=[[obs_varname], [smp_type], [region_dict[n32]]], index=colunm_list)
                df_p_value_col   = pd.DataFrame(np.array(p_value_list).T, columns=[[obs_varname], [smp_type], [region_dict[n32]]], index=colunm_list)
                df_pearson_r_col_list.append(df_pearson_r_col)
                df_p_value_col_list.append(df_p_value_col)
    df_pearson_r_result = pd.concat(df_pearson_r_col_list, axis=1)
    df_p_value_result   = pd.concat(df_p_value_col_list, axis=1)
    print(df_pearson_r_result)
    print(df_p_value_result)
    
    with pd.ExcelWriter(fp_output) as writer:
        df_pearson_r_result.to_excel(writer, sheet_name='pearson_r')
        df_p_value_result.to_excel(writer, sheet_name='p_value')                    
    return


def classfied(fp, sheet_name, factor):
    """
    对土地利用的结果按行名进行排序
    """
    import re
    
    df_r = pd.read_excel(fp, sheet_name=sheet_name, header=None)
    df_head = df_r.iloc[:5, :]
    df_body = df_r.iloc[5:, :]
    if factor == 'LU':
        df_body['factor_type'] = [str(s).split('_')[-1] for s in df_body[0].values]
    if factor == 'meteos':
        df_body['factor_type'] = ['_'.join(str(s).split('_')[:2]) for s in df_body[0].values]
    df_grouped = df_body.groupby(by='factor_type')
    df_grouped_list = [df_head]
    for g in df_grouped:
        df_grouped_list.append(g[1])
    df_grouped_ = pd.concat(df_grouped_list, axis=0)
    return df_grouped_

def classfied_main(factor):
    fp = r'I:\Data\DOC\Result\Runoff\meteos\与meteos相关性_runoff_20210902.xlsx'
    sheet_name = 'pearson_r'
    fd = os.path.dirname(fp)
    fp_output = os.path.join(fd, '与{}相关性_20210902_classfied.xlsx'.format(factor))
    df_pearson_r_result = classfied(fp, sheet_name='pearson_r', factor=factor)
    df_p_value_result   = classfied(fp, sheet_name='p_value', factor=factor)
    with pd.ExcelWriter(fp_output) as writer:
        df_pearson_r_result.to_excel(writer, sheet_name='pearson_r', index=None, header=None)
        df_p_value_result.to_excel(writer, sheet_name='p_value', index=None, header=None)  

if __name__ == '__main__':
    significant_correlation_std_main()
    # classfied_main('meteos')