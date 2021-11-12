"""
Create on 2021.06.01

Author = Albert
"""

from numpy import typename
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib.colorbar import Colorbar
import matplotlib.pyplot as plt
import matplotlib as mpl
import geopandas as gpd
import pandas as pd
from matplotlib.offsetbox import AnchoredText


def doc_distribution_2():
    fig = plt.figure(figsize=(12, 10), constrained_layout=True)
    # doc_fp = r'I:\Data\DOC\Data\All_type_runoff_doc_mean_without-nodata.csv'
    # tn_fp =  r'I:\Data\DOC\Data\All_type_runoff_tn_mean_without-nodata.csv'
    # doc_data = pd.read_csv(doc_fp)
    # tn_data = pd.read_csv(tn_fp)
    fp = r'D:\Easy\my_code\Group_321B\AlbertFang\Mark3_GlacierAnalysisDOC\Mean\All_type_data_mean.xlsx'
    df = pd.read_excel(fp)
    doc_data = df.dropna(axis=0, subset=['DOC(mg/L)'])
    tn_data  = df.dropna(axis=0, subset=['TN(mg/L)'])
    sample_type_dict = {
        'ice'     : 'Surface ice',
        'ice_core': 'Ice core',
        'snow'    : "Surface snow",
        'snow_pit': 'Snow pit',
        'runoff'  : 'Runoff',
    }
    ax_i = 1 
    for index, sample_type in enumerate(sample_type_dict.keys()):
        
        for i in range(2):
            ax = fig.add_subplot(5, 2, ax_i, projection=ccrs.PlateCarree())
            ax.set_extent([73, 105, 40, 25.5], crs=ccrs.PlateCarree())

            # Tibetan plateau
            # tp_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile\TP_counties\TP_counties.shp'
            tp_fp = r'I:\Qinghai_Tibet_Plateau\青藏高原范围与界线数据\DBATP\DBATP\DBATP_Polygon.shp'
            line_32 = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile\32N\32N.shp'
            tp_shape_feature = ShapelyFeature(Reader(tp_fp).geometries(), ccrs.PlateCarree(), facecolor="#F6F7FC") # facecolor='#F6F7FC'
            line_32_feature = ShapelyFeature(Reader(line_32).geometries(), ccrs.PlateCarree(), facecolor="#F6F7FC")

            ax.add_feature(cfeature.LAND, facecolor='#E7E2DF', zorder=1)
            ax.add_feature(cfeature.OCEAN, zorder=2)
            ax.add_feature(cfeature.COASTLINE, zorder=3)
            ax.add_feature(cfeature.LAKES, alpha=0.5, zorder=4)
            ax.add_feature(tp_shape_feature, edgecolor='gray', zorder=6)
            ax.add_feature(line_32_feature, edgecolor='black', linestyle='--', alpha=0.5, zorder=7)
            cmap = mpl.cm.RdYlGn_r
            if i % 2 == 0:
                data_type = doc_data[doc_data.Type==sample_type]
                lons, lats = data_type.Lon, data_type.Lat
                text = AnchoredText('DOC '+sample_type_dict[sample_type], loc=3, prop={'size': 12}, frameon=True)
                c_data = data_type['DOC(mg/L)']
                s = ax.scatter(lons, lats, c=data_type['DOC(mg/L)'], s=50, cmap=cmap, vmin=c_data.min(), vmax=c_data.max(), 
                                edgecolors='black',
                                transform=ccrs.PlateCarree(), zorder=7)
            else:
                data_type = tn_data[tn_data.Type==sample_type]
                lons, lats = data_type.Lon, data_type.Lat
                text = AnchoredText('TN '+sample_type_dict[sample_type], loc=3, prop={'size': 12}, frameon=True)
                c_data = data_type['TN(mg/L)']
                s = ax.scatter(lons, lats, c=data_type['TN(mg/L)'], s=50, cmap=cmap, vmin=c_data.min(), vmax=c_data.max(), 
                                edgecolors='black',
                                transform=ccrs.PlateCarree(), zorder=7)
            
            ax.add_artist(text)
            ax.annotate("32°N", xy=(4, 65), xycoords='axes points',
                        fontsize=12,
                        zorder=8)
            
            cb = fig.colorbar(s, ax=ax, extend='both', format='%.2f')
            cb.set_label('$mg/L$', fontsize=12,)

            ax_i += 1
    plt.savefig(r'I:\Data\DOC\Result\样点概况\浓度分布图\pic_con_20211113.png', dpi=300)
    plt.show()
    
    return


def doc_distribution():
    fig = plt.figure(figsize=(12.8, 5.4), constrained_layout=True)
    # subfigs = fig.subfigures(1, 2, wspace=0.07)
    # doc_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\SiteData\观测数据\GlcDOC\GlcDOC.shp'
    doc_fp = r'I:\Data\DOC\Shapefile\GlcDOCMean\GlcDOCMean.shp'
    doc_data = gpd.read_file(doc_fp)
    sample_type_list = ['sonw', 'snow_pit', 'ice', 'ice_core']
    sample_type_dict = {
        'snow'    : "Snow",
        'snow_pit': 'Snow Pit',
        'ice'     : 'Ice',
        'ice_core': 'Ice Core'
    }
    axes = []
    for index, sample_type in enumerate(sample_type_dict.keys()):
        ax = fig.add_subplot(2, 2, index+1, projection=ccrs.PlateCarree())
        axes.append(ax)
        ax.set_extent([73, 105, 40, 25.5], crs=ccrs.PlateCarree())

        # Tibetan plateau
        # tp_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile\TP_counties\TP_counties.shp'
        tp_fp = r'I:\Qinghai_Tibet_Plateau\青藏高原范围与界线数据\DBATP\DBATP\DBATP_Polygon.shp'
        line_32 = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile\32N\32N.shp'
        tp_counties_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile\TP_counties\TP_counties_wgs84.shp'
        tp_shape_feature = ShapelyFeature(Reader(tp_fp).geometries(), ccrs.PlateCarree(), facecolor="#F6F7FC") # facecolor='#F6F7FC'
        tp_counties_shape_feature = ShapelyFeature(Reader(tp_counties_fp).geometries(), ccrs.PlateCarree(), facecolor="#F6F7FC")
        line_32_feature = ShapelyFeature(Reader(line_32).geometries(), ccrs.PlateCarree(), facecolor="#F6F7FC")

        ax.add_feature(cfeature.LAND, facecolor='#E7E2DF', zorder=1)
        ax.add_feature(cfeature.OCEAN, zorder=2)
        ax.add_feature(cfeature.COASTLINE, zorder=3)
        # ax.add_feature(cfeature.BORDERS, linestyle='-')
        ax.add_feature(cfeature.LAKES, alpha=0.5, zorder=4)
        # ax.add_feature(cfeature.RIVERS, zorder=5)
        # ax.add_feature(states_provinces, edgecolor='gray')
        ax.add_feature(tp_shape_feature, edgecolor='gray', zorder=6)
        # ax.add_feature(tp_counties_shape_feature, edgecolor='gray', zorder=6.5)
        ax.add_feature(line_32_feature, edgecolor='black', linestyle='--', alpha=0.5, zorder=7)

        data_type = doc_data[doc_data.Type==sample_type]
        lons, lats = data_type.Lon, data_type.Lat
        cmap = mpl.cm.rainbow
        s = ax.scatter(lons, lats, c=data_type['DOC_mg_L_'], s=50, cmap=cmap, vmin=0.15, vmax=2.7, transform=ccrs.PlateCarree(), zorder=7)
        # ax.annotate(sample_type_dict[sample_type], xy=(10, 10), xycoords='axes points',
        #             fontsize=14,
        #             zorder=8)
        text = AnchoredText(sample_type_dict[sample_type], loc=3, prop={'size': 12}, frameon=True)
        ax.add_artist(text)
        ax.annotate("32°N", xy=(10, 88), xycoords='axes points',
                    fontsize=14,
                    zorder=8)
    # fig.tight_layout(pad=1, w_pad=0.29, h_pad=0.64)
    # plt.subplots_adjust(wspace=0.01, hspace=0.5) # 调整子图间距
    # norm = mpl.colors.Normalize(vmin=0.15, vmax=2.7)
    fig.colorbar(s, ax=axes,  location='right', shrink=0.5, extend='both', pad=0.01)
    # plt.colorbar(cax=data_type)
    plt.show()
    return

def doc_distribution_subplots():
    nr, nc = 2, 2
    fig, axs = plt.subplots(nr, nc)
    doc_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\SiteData\观测数据\GlcDOC\GlcDOC.shp'
    doc_data = gpd.read_file(doc_fp)
    sample_type_list = ['sonw', 'snow_pit', 'ice', 'ice_core']
    sample_type_dict = {
        'snow'    : "Snow",
        'snow_pit': 'Snow Pit',
        'ice'     : 'Ice',
        'ice_core': 'Ice Core'
    }

    scatters = []
    index = 0
    for i in range(nr):
        for j in range(nc):
            sample_type = sample_type_list[index]
            data_type = doc_data[doc_data.Type==sample_type]
            lons, lats, doc = data_type.CorrPt_x, data_type.CorrPt_y, data_type.DOC
            cmap = mpl.cm.seismic
            axs[i, j].scatter(lons, lats, doc, cmap=cmap, vmin=0.15, vmax=2.7, transform=ccrs.PlateCarree(), zorder=7)
            axs[i, j].annotate(sample_type_dict[sample_type], xy=(10, 10), xycoords='axes points',
                               fontsize=14,
                               zorder=8)
            tp_fp = r'I:\Qinghai_Tibet_Plateau\青藏高原范围与界线数据\DBATP\DBATP\DBATP_Polygon.shp'
            tp_shape_feature = ShapelyFeature(Reader(tp_fp).geometries(), ccrs.PlateCarree(), facecolor="#F6F7FC") # facecolor='#F6F7FC'

            axs[i, j].add_feature(cfeature.LAND, zorder=1)
            axs[i, j].add_feature(cfeature.OCEAN, zorder=2)
            axs[i, j].add_feature(cfeature.COASTLINE, zorder=3)
            # ax.add_feature(cfeature.BORDERS, linestyle='-')
            axs[i, j].add_feature(cfeature.LAKES, alpha=0.5, zorder=4)
            axs[i, j].add_feature(cfeature.RIVERS, zorder=5)
            # ax.add_feature(states_provinces, edgecolor='gray')
            axs[i, j].add_feature(tp_shape_feature, edgecolor='gray', zorder=6)
    plt.show()

sample_type_dict = {
        'snow'    : "Snow",
        'snow_pit': 'Snow Pit',
        'ice'     : 'Ice',
        'ice_core': 'Ice Core'
    }

def distribution_geoaxes():
    from cartopy.mpl.geoaxes import GeoAxes
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    from mpl_toolkits.axes_grid1 import AxesGrid

    projection = ccrs.PlateCarree()
    axes_class = (GeoAxes,
                  dict(map_projection=projection)) 
    fig = plt.figure(figsize=(16, 9))
    axgr = AxesGrid(fig, 111, axes_class=axes_class,
                    nrows_ncols=(2, 2),
                    axes_pad=0.2,
                    cbar_location='right',
                    cbar_mode='single',
                    cbar_pad=0.2,
                    cbar_size='2%',
                    label_mode='')  # note the empty label_mode

    doc_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\SiteData\观测数据\GlcDOC\GlcDOC.shp'
    doc_data = gpd.read_file(doc_fp)
    sample_type_list = ['snow', 'snow_pit', 'ice', 'ice_core']
    for i, ax in enumerate(axgr):
        print(sample_type_list[i])
        sample_type = sample_type_list[i]
        data_type = doc_data[doc_data.Type==sample_type_list[i]]
        lons, lats = data_type.CorrPt_x, data_type.CorrPt_y
        
        # Tibetan plateau
        # tp_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile\TP_counties\TP_counties.shp'
        tp_fp = r'I:\Qinghai_Tibet_Plateau\青藏高原范围与界线数据\DBATP\DBATP\DBATP_Polygon.shp'
        tp_counties_fp = r'I:\Qinghai_Tibet_Plateau\GlcAnysis\Shapefile\TP_counties\TP_counties_wgs84.shp'
        tp_shape_feature = ShapelyFeature(Reader(tp_fp).geometries(), ccrs.PlateCarree(), facecolor="#F6F7FC") # facecolor='#F6F7FC'
        tp_counties_shape_feature = ShapelyFeature(Reader(tp_counties_fp).geometries(), ccrs.PlateCarree(), facecolor="#F6F7FC")

        ax.add_feature(cfeature.LAND, facecolor='#E7E2DF',zorder=1)
        ax.add_feature(cfeature.OCEAN, zorder=2)
        ax.add_feature(cfeature.COASTLINE, zorder=3)
        # ax.add_feature(cfeature.BORDERS, linestyle='-')
        ax.add_feature(cfeature.LAKES, alpha=0.5, zorder=4)
        # ax.add_feature(cfeature.RIVERS, zorder=5)
        ax.set_extent([73, 105, 40, 25.5], crs=ccrs.PlateCarree())

        # ax.set_xticks(np.linspace(-180, 180, 5), crs=projection)
        # ax.set_yticks(np.linspace(-90, 90, 5), crs=projection)
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)
        ax.add_feature(tp_shape_feature, edgecolor='gray', zorder=6)
        ax.add_feature(tp_counties_shape_feature, edgecolor='gray', zorder=6.5)
        cmap = mpl.cm.rainbow
        s = ax.scatter(lons, lats, c=data_type.DOC, cmap=cmap, vmin=0.15, vmax=2.7, transform=ccrs.PlateCarree(), zorder=7)
        ax.annotate(sample_type_dict[sample_type], xy=(10, 10), xycoords='axes points',
                    fontsize=14,
                    zorder=8)
    axgr.cbar_axes[0].colorbar(s)
    # fig.colorbar(s, shrink=0.6, location='right', extend='both')
    plt.show()


if __name__ == '__main__':
    # distribution_geoaxes()
    # doc_distribution_subplots()
    doc_distribution_2()
