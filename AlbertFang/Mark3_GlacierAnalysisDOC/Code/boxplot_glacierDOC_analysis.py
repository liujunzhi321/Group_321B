"""
Create on 2021.0515

Author == Albert
"""

import numpy as np
from numpy.core.arrayprint import printoptions
import pandas as pd
from scipy.stats.stats import KurtosistestResult
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import pylab
import seaborn as sns
import os
import scipy

# workplace = 'I:\Qinghai_Tibet_Plateau\GlcAnysis\SiteData\GlcPtDOC\GlcPtDOC_20210203\GlcPtDOCWithTsAt'
# workplace = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\SiteData'
# fp = os.path.join(workplace, r'GlcPtDOCWithAttributes.xlsx')
# doc_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\SiteData\观测数据\GlcDOC.xlsx'
# tn_fp  = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\SiteData\观测数据\GlcTN.xlsx'
# doc_df = pd.read_excel(doc_fp)
# tn_df  = pd.read_excel(tn_fp)
# print(df)
    
def correlation_anlysis(df, typename, n32=None):
    """
    对不同类型的冰川DOC进行相关性分析
    """
    var_list = ['TN(mg/L)', 'DOC', 'CorrPt_x', 'CorrPt_y', 'Temp_K_', 'Prec_mm_yr', 'srad_W_m2_', 
                'Wind_m_s_', 'Ele_m', 'EVI_1km', 'EVI_5km', 'EVI_10km', 'EVI_20km']
    if n32:
        data = df[(df.Type==typename)&(df.N32d==n32)][var_list]
    else:
        data = df[df.Type==typename][var_list]
    
    # print(data)
    corr_matrix = data.corr()
    
    # 绘制heatmap
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(240, 10, as_cmap=True)
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)
    plt.title("{}&{} \n Numbers{}".format(typename, region_dict[n32], len(data)))
    plt.show()
    return

region_dict = {"S" : 'South of 32°N',
               "N" : 'North of 32°N',
               None: 'TP' 
}

obs_varname_dict = {
    "DOC"     : 'DOC',
    'TN(mg/L)': 'TN'
}

def significant_correlation(df, obs_varname, typename, n32=None):
    """
    列出有显著相关性的关系
    """
    var_list = [obs_varname, 'CorrPt_x', 'CorrPt_y', 'Temp_K_', 'Prec_mm_yr', 'srad_W_m2_', 
                'Wind_m_s_', 'Ele_m', 'EVI_1km', 'EVI_5km', 'EVI_10km', 'EVI_20km']
    if n32:
        data = df[(df.Type==typename)&(df.N32d==n32)][var_list]
    else:
        data = df[df.Type==typename][var_list]

    if len(data) < 3:
        print("样点数量不足（少于3个）！")
    else:
        for varname in var_list[1:]:
            y = data[obs_varname]
            x = data[varname]
            r, p_value = scipy.stats.pearsonr(x, y)
            promote_message = 'Correlation between {} {} and {} @ {} \n r={}, p_value={}'
            promote_message = promote_message.format(typename, obs_varname_dict[obs_varname], varname, region_dict[n32], round(r, 3), round(p_value, 3))
            if p_value < 0.05:
                print(promote_message)
                scatter_plot(data, x=varname, y=obs_varname, title=promote_message, fname=varname)
    return

def scatter_plot(df, x, y, title, fname):
    """
    绘制散点图
    """
    
    sns.set_theme(color_codes=True)
    sns.set(rc={"figure.figsize":(8, 10)}) #width=3, #height=4
    g = sns.lmplot(data=df, x=x, y=y)
    plt.title(title)
    plt.show()
    g.savefig(fname = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Result_0531\图\{}.png'.format(fname),
                dpi = 300,
                bbox_inches='tight')
    return 


def box_plot(df, obs_varname='DOC', plot_type=1):
    """
    """
    # fig, ax = plt.figure(figsize=[6.4, 4.8])
    plt.figure(figsize=(8, 6))
    sns.set_theme(style="ticks", palette="pastel")

    # Draw a nested boxplot to show bills by day and time
    if plot_type == 2:
        ax = sns.boxplot(x="Type", y=obs_varname, hue='N32', palette=["m", "g"], data=df[df.Type!='runoff'])
        ax = sns.swarmplot(x="Type", y=obs_varname, hue='N32', palette="Set1", data=df[df.Type!='runoff'], dodge=True)
    if plot_type == 1:
        ax = sns.boxplot(x="Type", y=obs_varname, order=['ice', 'ice_core', 'snow', 'snow_pit'], data=df[df.Type!='runoff'])
        ax = sns.swarmplot(x="Type", y=obs_varname, order=['ice', 'ice_core', 'snow', 'snow_pit'], data=df[df.Type!='runoff'], color='.25')
    # 
    sns.despine(offset=10, trim=True)
    
    plt.show()
    return

def box_multiplot(obsname='TN(mg/L)'):
    """
    绘制多幅box_plot
    """
    fp = r'I:\Data\DOC\Data\All_type_data_mean.xlsx'
    df = pd.read_excel(fp)
    # print(sorted_df)
 
    df_dropna  = df.dropna(subset=[obsname])
    sorted_df = df_dropna.sort_values(by='Type')
    grid = sns.FacetGrid(sorted_df, col='Type',)
    grid.map(sns.boxplot, 'Regions', obsname, palette="Set2", order=['Westerly', 'Monsoon', ])
    grid.map(sns.swarmplot, 'Regions', obsname,  color='.25', order=['Westerly', 'Monsoon', ])
    grid.set_axis_labels(" ", "${}$".format(obsname))
    grid.set_titles(col_template="{col_name}",)
    grid.tight_layout()
    grid_1 = sns.FacetGrid(sorted_df, col='Type',)
    plt.show()

    # grid.map(sns.boxplot, )
    # grid.set(xticks=np.arange(5), yticks=[-3, 3],
    #      xlim=(-.5, 4.5), ylim=(-3.5, 3.5))
    # # Adjust the arrangement of the plots
    # grid.fig.tight_layout(w_pad=1)


def boxplot_plt():
    # fp = r'I:\Data\DOC\Data\All_type_data_mean.xlsx'
    fp = r'D:\Easy\my_code\Group_321B\AlbertFang\Mark3_GlacierAnalysisDOC\Mean\All_type_data_mean.xlsx'
    df = pd.read_excel(fp)

    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(style="ticks", rc=custom_params)
    fig = plt.figure(figsize=(12, 5), )
    gs = fig.add_gridspec(1, 2, hspace=0.2, wspace=0.2)
    axes = gs.subplots(sharex='col')
    # fig, axes = plt.subplots(2, 4, figsize=(12, 6), sharey=True, sharex=True)
    obs_varname_list = ['DOC(mg/L)', 'TN(mg/L)']
    type_list = ['ice', 'ice_core', 'snow', 'snow_pit',]
    type_dict = {'ice'      : 'Surface ice', 
                 'ice_core' : 'Ice core', 
                 'snow'     : 'Surface snow', 
                 'snow_pit' : 'Snow pit', 
                 'runoff'   : 'Runoff'}
    title_list = ['(a)', '(b)', '(c)', '(d)', '(e)']
    labels = [type_dict[typename] for typename in type_list]
    print(labels)
    kwargs = {'labels': labels}
    for i, obs_varname in enumerate(obs_varname_list):
        df_dropna  = df.dropna(subset=[obs_varname])
        bp = sns.boxplot(ax=axes[i], x="Type", y=obs_varname, order=['ice', 'ice_core', 'snow', 'snow_pit', ], data=df_dropna, 
                    # **kwargs,
                    )
        bp.set_xticklabels(labels)

        sp = sns.swarmplot(ax=axes[i], x="Type", y=obs_varname, order=['ice', 'ice_core', 'snow', 'snow_pit', ], data=df_dropna, color='.25',
                    # **kwargs,
                    )
        sp.set_xticklabels(labels)

        axes[i].set_ylabel('${}$'.format(obs_varname))
        axes[i].set_title(title_list[i], loc='left')
        axes[i].set_xlabel(' ')
    fig.savefig(fname = r'I:\Data\DOC\Result\样点概况\全体样点_分类_20211113.png',
        dpi = 300,
        bbox_inches='tight')
    plt.show()
    return


def box_multiplot_plt():
    fp = r'D:\Easy\my_code\Group_321B\AlbertFang\Mark3_GlacierAnalysisDOC\Mean\All_type_data_mean.xlsx'
    df = pd.read_excel(fp)

    doc_MannwhitneyuResult = [0.500, 0.430, 0.370, 0.087, 0.131]
    tn_MannwhitneyuResult  = [0.056, 0.056, 0.483, 0.468, 0.002]

    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(style="ticks", rc=custom_params)

    fig = plt.figure(figsize=(20, 5), )
    gs = fig.add_gridspec(2, 5, hspace=0.2, wspace=0.1)
    axes = gs.subplots(sharex='col', sharey='row')
    # fig, axes = plt.subplots(2, 4, figsize=(12, 6), sharey=True, sharex=True)
    obs_varname_list = ['DOC(mg/L)', 'TN(mg/L)']
    type_list = ['ice', 'ice_core', 'snow', 'snow_pit', 'runoff']
    type_dict = {'ice'      : 'Surface ice', 
                 'ice_core' : 'Ice core', 
                 'snow'     : 'Surface snow', 
                 'snow_pit' : 'Snow pit', 
                 'runoff'   : 'Runoff'}
    title_list_1 = ['(a)', '(b)', '(c)', '(d)', '(e)']
    title_list_2 = ['(f)', '(g)', '(h)', '(i)', '(j)']
    for i, obs_varname in enumerate(obs_varname_list):
        df_dropna  = df.dropna(subset=[obs_varname])
        for j, typename in enumerate(type_list):
            sns.boxplot(ax=axes[i,j], x="Regions", y=obs_varname, order=['Westerly', 'Monsoon'], data=df_dropna[df_dropna.Type==typename], palette="Set2")
            sns.swarmplot(ax=axes[i,j], x="Regions", y=obs_varname, order=['Westerly', 'Monsoon'], data=df_dropna[df_dropna.Type==typename], color='.25')
            
            if i == 0:
                axes[i, j].set_title(title_list_1[j], loc='left')
                axes[i, j].set_xlabel(' ')
                axes[i, j].annotate("Mann-Whitney U,\n       p={}".format(doc_MannwhitneyuResult[j]), xy=(0, 2),  fontsize=11)
            else:
                axes[i, j].set_title(title_list_2[j], loc='left')
                axes[i, j].set_xlabel(type_dict[typename])
                axes[i, j].annotate("Mann-Whitney U,\n       p={}".format(tn_MannwhitneyuResult[j]), xy=(0, 0.600), fontsize=11)
            if j == 0:
                axes[i, j].set_ylabel('${}$'.format(obs_varname))
            else:
                axes[i, j].set_ylabel(' ')
    fig.savefig(fname = r'I:\Data\DOC\Result\样点概况\样点_分区_boxplot_20211113.png',
        dpi = 300,
        bbox_inches='tight')
    plt.show()
    return


def box_plot_main():
    fp = r'I:\Data\DOC\Data\All_type_data_mean.xlsx'
    df = pd.read_excel(fp)
    df_doc_dropna = df.dropna(subset=['DOC(mg/L)'])
    df_tn_dropna  = df.dropna(subset=['TN(mg/L)'])
    box_plot(df_tn_dropna, 'TN(mg/L)', plot_type=1)
    return

def difference(obsname='TN(mg/L)'):
    """
    检验差异是否明显
    （1） 检验ice和ice_core, snow和snow_pit两两之间是否存在差异性；
    （2） 检验四种类型是否存在差异性。
    """
    from scipy import stats
    # fp = r'I:\Data\DOC\Data\All_type_data_mean_1.xlsx'
    fp = r'D:\Easy\my_code\Group_321B\AlbertFang\Mark3_GlacierAnalysisDOC\Mean\All_type_data_mean.xlsx'
    df = pd.read_excel(fp)
    # df_grouped_ = df.groupby('Type')
    # print(obsname)
    # for df_grouped in df_grouped_:
    #     sample_name = df_grouped[0]
    #     df_monsoon  = df_grouped[1][df_grouped[1].Regions=='Monsoon'][obsname]
    #     df_westerly = df_grouped[1][df_grouped[1].Regions=='Westerly'][obsname] 
    #     # print(sample_name)
    #     result = stats.mannwhitneyu(df_monsoon, df_westerly)
    #     print(sample_name, ': ', result)
    # df_ice_ice_core  = df[(df.Type=='ice') | (df.Type=='ice_core')][obsname]
    # df_snow_snow_pit = df[(df.Type=='snow') | (df.Type=='snow_pit')][obsname]
    df_ice      = df[df.Type=='ice'][obsname]
    df_snow     = df[df.Type=='snow'][obsname]
    df_ice_core = df[df.Type=='ice_core'][obsname]
    df_snow_pit = df[df.Type=='snow_pit'][obsname]
    four_types_result = stats.kruskal(df_ice, df_snow, df_ice_core, df_snow_pit, nan_policy='omit')
    ice_ice_core  = stats.mannwhitneyu(df_ice, df_ice_core)
    snow_snow_pit = stats.mannwhitneyu(df_snow, df_snow_pit)
    obsname_list = ['DOC(mg/L)', 'TN(mg/L)']
    type_list = ['ice', 'ice_core', 'snow', 'snow_pit', 'runoff']
    for obsname in obsname_list:
        print(obsname)
        for typename in type_list:
            n = df[(df.Type==typename) & (df.N32=='N')][obsname]
            s = df[(df.Type==typename) & (df.N32=='S')][obsname]
            diff = stats.mannwhitneyu(n, s)
            print('\t{}\t: {}'.format(typename, diff))

    # print('Four Types\t: ', four_types_result) 
    # print("ice & ice_core\t: ", ice_ice_core)
    # print("snow & snow_pit\t: ", snow_snow_pit)
    return

    


if __name__ == '__main__':
    # correlation_anlysis(doc_df, 'ice', 'S')
    # box_plot_main()
    
    # box_multiplot()
    # box_multiplot_plt()
    # difference()
    # box_plot_main()
    boxplot_plt()

    # typename_list = ['snow', 'snow_pit', 'ice', 'ice_core']
    # direction_list = ['S', 'N', None]
    # for typename in typename_list:
    #     for direction in direction_list:
    #         correlation_anlysis(tn_df, typename, direction)

    # for direction in direction_list:
    #     message = '@{}'.format(region_dict[direction])
    #     print(message, )
    #     for typename in typename_list:
    #         message = '\t Sample type: {}'.format(typename)
    #         print(message,)
    #         significant_correlation(tn_df, 'TN(mg/L)', typename, direction)